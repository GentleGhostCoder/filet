import logging
import sys
from typing import Annotated, Optional, Set

import boto3
from prompt_toolkit import prompt
from rich import print
from sqlalchemy import create_engine, text

from filet.boto3.fetch_s3_sources import fetch_s3_sources
from filet.boto3.schema import Encryption, Format, ListBucketsResult, ListObjectsV2Result, S3Source, S3SourceExtra
from filet.boto3.types import S3Client
from filet.boto3.utils import extract_file_meta
from filet.cli.global_options import ProcessOptions
from filet.cli.utils.loading_animation import LoadingAnimation
from filet.cli.utils.prompt_toolkit_selection import PromptSelection
from filet.cli.utils.to_ansi import to_ansi
from filet.config.boto3_client import Boto3ClientConfig
from filet.config.cache_db import store
from filet.config.objects_pattern import ObjectsPattern
from filet.config.trino_client import TrinoDwhConfig
from filet.core.create_schema import create_schema
from filet.core.csv.raw_csv import stage_csv
from filet.core.json.flat import stage_flat_json
from filet.core.json.txt import stage_json
from filet.core.type_mapping import JsonFormat
import filet.patches.typer as typer

logger = logging.getLogger(__name__)

add_group = typer.Typer(name="stage", help="Stage data from S3 to Trino.")


def init_config(s3cfg, objects_pattern, trino_dwh_config, s3_source):
    """Initialize the stage command."""
    logger.debug("S3cfg: %s", s3cfg)
    logger.debug("S3cfg Model Config: %s", s3cfg.model_config)
    logger.debug("ObjectsPattern: %s", objects_pattern)
    logger.debug("TrinoDwhConfig: %s", trino_dwh_config)
    logger.debug("TrinoDwhConfig Model Config: %s", trino_dwh_config.model_config)
    logger.debug("S3 Source: %s", s3_source)
    s3_client: S3Client = boto3.client(**s3cfg.model_dump())
    logger.debug("Boto3 Client: %s", s3_client)
    return s3_client


@add_group.command(ProcessOptions)  # type: ignore
def add(  # noqa: C901
    s3_source: Annotated[S3Source, typer.Option(..., "--s3source", help="S3 Source to stage.")] = S3Source(),
    json_format: Optional[
        Annotated[
            JsonFormat,
            typer.Option(
                ..., "--json-format", help="Stage JSON data with predefined format [txt (recommended), flat]."
            ),
        ]
    ] = "txt",
    s3cfg: Boto3ClientConfig = Boto3ClientConfig(),
    objects_pattern: ObjectsPattern = ObjectsPattern(),
    trino_dwh_config: TrinoDwhConfig = TrinoDwhConfig(),
    silent: bool = False,
):
    """Add new stage."""
    loading_animation = None
    prompt_selection = PromptSelection("dummy")
    try:
        s3_client = init_config(s3cfg, objects_pattern, trino_dwh_config, s3_source)
        if not s3_source.Bucket:
            loading_animation = LoadingAnimation(
                f"Reading Buckets from [magenta]{s3cfg.endpoint_url}[/magenta]", total_width=5, silent=silent
            )
            loading_animation.start()
            bucket_result = ListBucketsResult(**s3_client.list_buckets())

            prompt_selection = PromptSelection(
                "Bucket Selection",
                description="Select the bucket you want to stage.",
                selection=[bucket.Name for bucket in bucket_result.Buckets],
            )
            loading_animation.stop()

            prompt_selection.run()

            if not prompt_selection.selected_obj:
                print("[red bold]No bucket selected. Exiting.")
                sys.exit(1)

            s3_source.Bucket = prompt_selection.selected_obj

        logger.debug("Reading Objects from Bucket.")

        if not s3_source.Key:
            objects: list = []
            all_objects: Set[str] = set()
            all_prefixes: Set[str] = set()
            selection_list: list = []
            while not prompt_selection or prompt_selection.selected_obj not in all_objects:
                loading_animation = LoadingAnimation(
                    f"Reading Objects from [magenta]{s3_source.Prefix}[/magenta]", total_width=5, silent=silent
                )
                loading_animation.start()
                if not prompt_selection or not any(
                    [prompt_selection.selected_obj in obj for obj in all_prefixes if s3_source.Prefix != obj]
                ):
                    prefixes = ListObjectsV2Result(
                        **s3_client.list_objects_v2(
                            Bucket=s3_source.Bucket, Prefix=s3_source.Prefix, Delimiter="/", MaxKeys=100
                        )
                    )
                    for prefix in prefixes.CommonPrefixes:
                        if prefix not in list(all_prefixes):
                            all_prefixes.add(prefix.Prefix)

                    objects = extract_file_meta(prefixes, objects_pattern)
                    for obj in objects:
                        if obj.KeyPattern not in list(all_objects):
                            all_objects.add(obj.KeyPattern)

                prompt_selection = PromptSelection(
                    f"Object Selection - [magenta]{s3_source.Bucket}[/magenta] - [green]{s3_source.Prefix or '/'}[/green]",
                    description="Select the object you want to stage.",
                    selection=[
                        obj
                        for obj in [*all_objects, *all_prefixes]
                        if s3_source.Prefix in obj and s3_source.Prefix != obj
                    ],
                )

                loading_animation.stop()
                prompt_selection.run()

                if not prompt_selection.selected_obj:
                    if not selection_list:
                        print("[red bold]No object selected. Exiting.")
                        sys.exit(1)
                    s3_source.Prefix = selection_list.pop()
                    continue

                selection_list.append(prompt_selection.selected_obj)
                s3_source.Prefix = prompt_selection.selected_obj

            previous_chunk_size = s3_source.ChunkSize
            new_s3_source = next((obj for obj in objects if obj.KeyPattern == prompt_selection.selected_obj), None)
            if not new_s3_source:
                raise ValueError(f"Object not found: {prompt_selection.selected_obj}")
            s3_source = new_s3_source
            s3_source.ChunkSize = previous_chunk_size

        logger.debug("Selected S3 Source: %s", s3_source)
        loading_animation = LoadingAnimation(
            f"Reading Object Meta from [magenta]{s3_source.Bucket}[/magenta] - [green]{s3_source.Key}[/green]",
            total_width=5,
            silent=silent,
        )
        if s3_source.ObjectEncryption != Encryption.none:
            # Create input prompt for s3_sourceExtra
            gpg_home = prompt(to_ansi("[magenta]GPG Home: "), default="~/.gnupg")
            keyring_file_path = prompt(to_ansi("[magenta]Keyring File Path: "), default="")
            passphrase = prompt(to_ansi("[magenta]Passphrase: "), default="", is_password=True)
            s3_source.Extra = S3SourceExtra(GPGHome=gpg_home, KeyringFilePath=keyring_file_path, Passphrase=passphrase)

        # create_schema(trino_dwh_config, s3_source.Bucket)
        if s3_source.ObjectFormat == Format.json:
            if not json_format:
                prompt_selection = PromptSelection(
                    f"Choose Format - [green]{prompt_selection.selected_obj}[/green]",
                    description="Select the object you want to stage.",
                    selection=[f.value for f in JsonFormat],  # "avro",
                )
                prompt_selection.run()
                if prompt_selection.selected_obj not in JsonFormat:
                    print("[red bold]No object selected. Exiting.")
                    sys.exit(1)
                json_format = JsonFormat(prompt_selection.selected_obj)
            logger.debug("Selected JSON Format: %s", json_format)
            if json_format == JsonFormat.txt:
                loading_animation.start()
                stage_json(s3_client, s3_source, trino_dwh_config)
            if json_format == JsonFormat.flat:
                loading_animation.start()
                stage_flat_json(s3_client, s3_source, trino_dwh_config)

        if s3_source.ObjectFormat == Format.csv:
            loading_animation.start()
            stage_csv(s3_client, s3_source, trino_dwh_config)

        loading_animation.stop()

        print("\r")

        current_stage = store.stages[s3_source.Prefix.rsplit("/")[-1].replace("-", "_").lower()]
        # create_table_sql, create_stage_view_sql, create_target_table_sql, insert_into_target_table_sql):
        for sql in (
            current_stage.sql.create_table,
            current_stage.sql.select,
            current_stage.sql.create_target_table,
            current_stage.sql.insert,
        ):
            print(sql)

    except KeyboardInterrupt:
        if loading_animation and isinstance(loading_animation, LoadingAnimation):
            loading_animation.stop()
        print("[red bold]Interrupted. Exiting.")
        sys.exit(1)
    except Exception as e:
        if loading_animation and isinstance(loading_animation, LoadingAnimation):
            loading_animation.stop()
        print("[red bold]An error occurred. Exiting.")
        logger.exception(e)
        sys.exit(1)


@add_group.command(ProcessOptions)  # type: ignore
def ingest(  # noqa: C901
    s3_source: Annotated[S3Source, typer.Option(..., "--s3source", help="S3 Source to stage.")] = S3Source(),
    objects_pattern: ObjectsPattern = ObjectsPattern(),
    s3cfg: Boto3ClientConfig = Boto3ClientConfig(),
    trino_dwh_config: TrinoDwhConfig = TrinoDwhConfig(),
    # silent: bool = False,
):
    """Add new stage."""
    loading_animation = None
    prompt_selection = None
    try:
        s3_client = init_config(s3cfg, objects_pattern, trino_dwh_config, s3_source)

        prompt_selection = PromptSelection(
            "Stages",
            description="Select the stage to ingest",
            selection=list(store.stages.keys()),
        )

        prompt_selection.run(force_selection=True)

        current_stage = store.stages[prompt_selection.selected_obj]

        if not current_stage.s3_source:
            raise ValueError(f"Stage {prompt_selection.selected_obj} has no S3 Source.")

        objects = fetch_s3_sources(
            s3_client,
            current_stage.s3_source.Bucket,
            max_keys_per_prefix=100,
            prefix=current_stage.s3_source.Prefix,
            objects_pattern=objects_pattern,
        )

        trino_engine = create_engine(**trino_dwh_config.client_config.model_dump())
        trino_connection = trino_engine.connect()
        logger.debug("Trino Connection: %s", trino_connection)
        for obj in objects:
            execute_sql = str(current_stage.sql.insert)
            execute_sql = execute_sql.replace("?", f"'s3a://{obj.Bucket}/{obj.Key}'")
            logger.debug("Ingest SQL Statement: %s", execute_sql)
            trino_connection.execute(text(execute_sql))

    except KeyboardInterrupt:
        if loading_animation and isinstance(loading_animation, LoadingAnimation):
            loading_animation.stop()
        print("[red bold]Interrupted. Exiting.")
        sys.exit(1)
    except Exception as e:
        if loading_animation and isinstance(loading_animation, LoadingAnimation):
            loading_animation.stop()
        print("[red bold]An error occurred. Exiting.")
        logger.exception(e)
        sys.exit(1)
