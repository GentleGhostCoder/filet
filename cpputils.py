"""Load C++ utilities."""

from dataclasses import dataclass
import logging
from typing import List, Optional, Union

import pandas as pd

from filet._cpputils import AvroSchemaHandler, FlatJsonHandler, JsonHandler
from filet._cpputils import eval_csv as _eval_csv
from filet._cpputils import eval_datetime, eval_type

logger = logging.getLogger(__name__)


@dataclass
class CsvEvaluationResult:
    """A data structure to hold the results of CSV evaluation.

    :param line_separator: The character used to separate lines in the CSV file.
    :param parsed_line_count: The total number of lines parsed from the CSV data.
    :param column_separator: The character used to separate columns in the CSV file.
    :param has_header: A boolean indicating if the CSV data includes a header row.
    :param column_types: A list of strings describing the inferred types of the columns.
    :param column_count: The number of columns detected in the CSV data.
    :param quoting_character: The character used to quote data in the CSV file.
    :param header: An optional list of header names, if detected.

    Example usage is shown in the documentation of `eval_csv` function.
    """

    line_separator: str
    parsed_line_count: int
    column_separator: str
    has_header: bool
    column_types: List[str]
    column_count: int
    quoting_character: str
    header: Optional[List[str]] = None


def eval_csv(data: Union[bytes, str], disallowed_header_chars: str = "") -> CsvEvaluationResult:
    """Evaluate the structure and content of CSV data.

     It can be used determine its characteristics such as line separator,
     column separator, presence of headers, column types, and more.

    :param data: The CSV data to be evaluated. This can be either a bytes object or a string.
    :param disallowed_header_chars: A string containing characters that are not allowed in the header.
    This parameter can be used to filter out unwanted characters from the header. By default, it includes `"\r\n,;\t|\b"`
    :return: An instance of CsvEvaluationResult containing the evaluation results.

    Example:

    >>> csv_data = "id,name\\n1,Alice\\n2,Bob"
    >>> result = eval_csv(csv_data)
    >>> print(result.column_count)
    2
    >>> print(result.has_header)
    True
    """
    return CsvEvaluationResult(**_eval_csv(data, disallowed_header_chars))


def eval_json(data: Union[bytes, str]) -> dict:
    """Evaluate JSON data to generate an Avro schema.

    If the JSON data represents a list, it is wrapped in a dictionary
    to ensure compatibility with certain data processing frameworks.

    :param data: The JSON data to be evaluated. This can be either a bytes object or a string.
    :return: A dictionary representing the Avro schema generated from the JSON data.

    Example:

    >>> json_data = '[{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]'
    >>> schema = eval_json(json_data)
    >>> print(schema['type'])
    record
    >>> print(schema['fields'][0]['name'])
    root
    """
    schema = AvroSchemaHandler().create_schema(data)
    if (isinstance(data, str) and data.startswith("[")) or (isinstance(data, bytes) and data.startswith(b"[")):
        logger.debug(
            "JSON data is an ARRAY. Wrapping it in a dictionary "
            "to ensure compatibility with certain data processing frameworks."
        )
        schema = {"name": "rootArrayWrapper", "type": "record", "fields": [{"name": "root", "type": schema}]}

    return schema


def eval_flat_json(data: Union[bytes, str]) -> CsvEvaluationResult:
    """Evaluate flat JSON data to generate a CSV schema.

    For larger amount of data, it is recommended to use pandas json_normalize.
    This method can also read broken json chunks.

    :param data: The flat JSON data to be evaluated. This can be either a bytes object or a string.
    :return: An instance of CsvEvaluationResult containing the evaluation results."""
    handler = FlatJsonHandler()
    data = handler.loads(data)
    df = pd.DataFrame(data)

    return eval_csv(df.to_csv(index=False).encode("utf-8"))


__all__ = [
    "eval_csv",
    "eval_json",
    "eval_datetime",
    "eval_type",
    "CsvEvaluationResult",
    "AvroSchemaHandler",
    "FlatJsonHandler",
    "JsonHandler",
]
