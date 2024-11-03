from dataclasses import MISSING, is_dataclass, fields
from functools import wraps
from inspect import Parameter, isclass, signature
from typing import Any, Callable, List

import click
from pydantic import BaseModel
import typer
from typer.models import CommandFunctionType, DefaultPlaceholder, ParamMeta
from aiapy.patches.utils.check_type import check_type

MISSING_TYPE = type(MISSING)


def default(field):
    """Method to get the default value of the dataclass."""
    return (
        field.default_factory() if not isinstance(field.default_factory, (MISSING_TYPE, type(None))) else field.default
    )


# TODO: watch this github issue (params / types): https://github.com/tiangolo/typer/issues/111
# TODO: watch this github issue (global option): https://github.com/tiangolo/typer/issues/153


class Typer(typer.Typer):
    base_callback: Callable[..., Callable[[CommandFunctionType], CommandFunctionType]] = typer.Typer.callback
    base_command: Callable[..., Callable[[CommandFunctionType], CommandFunctionType]] = typer.Typer.command
    base_add_typer: Callable[..., None] = typer.Typer.add_typer

    def _check_option_types(self, options_types=None):
        if not options_types:
            if not getattr(self, "options_types", None):
                return
            options_types = self.options_types
        for option_type in options_types:
            if not is_dataclass(option_type):
                raise ValueError(f"'{option_type.__class__.__name__}' is not a dataclass!")
        return options_types

    def __init__(self, *options_types, **kwargs):
        super().__init__(**kwargs)
        self.options_types = self._check_option_types(options_types)
        self.info.callback = self.callback()(self.info.callback)

    def add_typer(self, typer_instance, **kwargs):
        typer_instance.options_types = self.options_types
        if "callback" in kwargs:
            kwargs["callback"] = self.callback()(kwargs["callback"])
            typer_instance.info.callback = kwargs["callback"]
        if isinstance(typer_instance.info.callback, DefaultPlaceholder):
            typer_instance.info.callback = typer_instance.callback(*typer_instance.options_types)(
                lambda: ...
            )  # fix common options between subcommands
        self.base_add_typer(typer_instance, **kwargs)

    def callback(self, *options_types, **kwargs) -> Callable[[CommandFunctionType], CommandFunctionType]:
        if not (options_types := self._check_option_types(options_types)):
            return self.base_callback(**kwargs)

        def decorator(__f):

            if isinstance(__f, DefaultPlaceholder):
                return __f

            passed_args = signature(__f).parameters.keys()

            @wraps(__f)
            def wrapper(*__args, **__kwargs):
                if len(__args) > 0:
                    raise RuntimeError("Positional arguments are not supported")

                for option in options_types:
                    __kwargs = self._patch_wrapper_kwargs(option, **__kwargs)
                    __kwargs = {key: value for key, value in __kwargs.items() if key in passed_args}

                return __f(*__args, **__kwargs)

            for o_option in options_types:
                self._patch_command_sig(wrapper, o_option)

            return self.base_callback(**kwargs)(wrapper)

        return decorator

    def command(self, *options_types, **kwargs) -> Callable[[CommandFunctionType], CommandFunctionType]:
        if not (options_types := self._check_option_types(options_types)):
            return self.base_command(**kwargs)

        def decorator(__f):

            if isinstance(__f, DefaultPlaceholder):
                return __f

            passed_args = list(signature(__f).parameters.keys())

            @wraps(__f)
            def wrapper(*__args, **__kwargs):
                if len(__args) > 0:
                    raise RuntimeError("Positional arguments are not supported")
                for option in options_types:
                    __kwargs = self._patch_wrapper_kwargs(option, **__kwargs)
                    __kwargs = {key: value for key, value in __kwargs.items() if key in passed_args}
                return __f(*__args, **__kwargs)

            for o_option in options_types:
                self._patch_command_sig(wrapper, o_option)
            return self.base_command(**kwargs)(wrapper)

        return decorator

    @staticmethod
    def _patch_wrapper_kwargs(options_type, **kwargs):
        if (ctx := kwargs.get("ctx")) is None:
            raise RuntimeError("Context should be provided")

        common_opts_params: dict = {}

        if options_type.instance is not None:
            common_opts_params.update(options_type.instance.__dict__)

        for field in fields(options_type):
            if field.metadata.get("ignore", False):
                continue

            value = kwargs.get(field.name)

            if value == field.default:
                continue

            common_opts_params[field.name] = value

        options_type(**common_opts_params)
        setattr(ctx, "common_params", common_opts_params)
        return {**kwargs}

    @staticmethod
    def _patch_command_sig(__w, options_type) -> None:
        sig = signature(__w)
        new_parameters = sig.parameters.copy()

        options_type_fields = fields(options_type) if is_dataclass(options_type) else options_type.model_fields.values()

        for field in options_type_fields:
            if field.metadata.get("ignore", False):
                continue

            new_parameters[field.name] = Parameter(
                name=field.name,
                kind=Parameter.KEYWORD_ONLY,  # type: ignore
                default=field.default,
                annotation=field.type,
            )
        for kwarg in sig.parameters.values():
            if kwarg.kind == Parameter.KEYWORD_ONLY and kwarg.name != "ctx":
                if kwarg.name not in new_parameters:
                    new_parameters[kwarg.name] = kwarg.replace(default=kwarg.default)

        # Sort parameters in the correct order
        sorted_parameters = sorted(new_parameters.values(), key=lambda p: (p.kind, p.name))

        new_sig = sig.replace(parameters=sorted_parameters)
        setattr(__w, "__signature__", new_sig)


def get_custom_param_type(annotation):  # noqa: C901 TODO: reduce complexity
    extra_params = []
    if hasattr(annotation, "model_config"):
        if "env_file" in annotation.model_config and "env_file" not in annotation.model_fields:
            extra_params.append("env_file")
        if "profile" in annotation.model_config and "profile" not in annotation.model_fields:
            extra_params.append("profile")

    class CustomParamType(click.ParamType):
        name = annotation.__name__
        command = None

        def get_metavar(self, param):
            model_fields = [key for key, value in annotation.model_fields.items() if value.repr]
            return f"{self.name} ({', '.join([*extra_params, *model_fields])})"

        def convert(self, value, param, ctx: typer.Context):
            # Check if it's the second command in a chain
            try:
                # Parse the string of the format 'key=value' into a dictionary
                values = value.split("=") if isinstance(value, str) else value
                if len(values) < 2:
                    raise AttributeError(f"Can´t parse value `{value}`.")

                # Retrieve the existing Boto3ClientConfig instance or create a new one
                config = ctx.params.get(param.name, {})
                key, value = values

                if key not in annotation.model_fields:
                    if key in extra_params:
                        config[key] = value
                        ctx.params[param.name] = config
                        annotation.model_config[key] = value
                        return config
                    raise ValueError(f"Invalid key '{key}' for type '{self.name}'.")

                if not isinstance(config, dict):
                    return {}

                # Update the dictionary with the new key/value pair
                config[key] = check_type(annotation.model_fields[key].annotation, value, key)
                ctx.params[param.name] = config
                return config
            except (ValueError, AttributeError) as e:
                self.fail(f"Invalid value for '--{param.name}': {e} " f"Expected syntax --{param.name} <attr>=<value>.")

    return CustomParamType()


_get_click_type = typer.main.get_click_type
_get_click_param = typer.main.get_click_param


def get_click_type(*, annotation: Any, parameter_info: typer.main.ParameterInfo):
    if isclass(annotation) and issubclass(annotation, BaseModel):
        return get_custom_param_type(annotation)
    else:
        return _get_click_type(annotation=annotation, parameter_info=parameter_info)


def get_click_param(
    param: ParamMeta,
):
    if isclass(param.annotation) and issubclass(param.annotation, BaseModel):  # type: ignore
        if param.default and not isinstance(param.default.default, type(Ellipsis)):
            # model_confgi params -> env_file and profile
            extra_fields = [
                (key, param.annotation.model_config[key])
                for key in ["env_file", "profile"]
                if key in param.annotation.model_config
            ]
            if not param.default.default or isinstance(param.default.default, MISSING_TYPE):
                default_instance = param.annotation()
                param.default.default = [
                    (name, getattr(default_instance, name, None) or default(field)) for name, field in param.annotation.model_fields.items()
                ]
            if param.default.default:
                param.default.default = [
                    *extra_fields,
                    *[(key, value) for key, value in param.default.default],
                ]

        base_annotation = param.annotation
        param.annotation = List[base_annotation]  # type: ignore

        new_param = _get_click_param(param)

        def pydantic_func(value):
            if not value:
                return []
            param_value = base_annotation(**value[0]).model_copy(update=value[0])
            return param_value

        return new_param[0], pydantic_func

    return _get_click_param(param)
