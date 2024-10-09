import unittest

from tests.generate_data import generate_complex_csv_data, generate_simple_csv_data
import filet.cpputils as utils


class TestEvalDatetime(unittest.TestCase):
    """Tests for eval_csv."""

    def test_simple_csv_data(self):
        self.assertEqual(
            utils.eval_csv(generate_simple_csv_data().to_csv(index=False).encode("utf-8")),
            utils.CsvEvaluationResult(
                line_separator="\n",
                parsed_line_count=4,
                column_separator=",",
                has_header=True,
                column_types=["int", "str", "int", "str", "float", "bool", "date", "float"],
                column_count=8,
                quoting_character="",
                header=["ID", "Name", "Age", "Email", "Salary", "FullTime", "JoinDate", "Rating"],
            ),
        )

    def test_complex_csv_data(self):
        self.assertEqual(
            utils.eval_csv(generate_complex_csv_data().to_csv(index=False).encode("utf-8")),
            utils.CsvEvaluationResult(
                line_separator="\n",
                parsed_line_count=4,
                column_separator=",",
                has_header=True,
                column_types=["int", "str", "int", "str", "float", "bool", "date", "float", "str", "str"],
                column_count=10,
                quoting_character='"',
                header=["ID", "Name", "Age", "Email", "Salary", "FullTime", "JoinDate", "Rating", "Address", "Skills"],
            ),
        )

    def test_csv_bytes_types(self):
        self.assertEqual(
            utils.eval_csv(
                "int_col,bool_col,datetime_ms_col,datetime_col,"
                "time_col,text_with_quoted_seperator_col,None\n"
                "1,TRUE,'20060317 13:27:54.123','20060317 13:27:54.123456',"
                "'13:27:54.123','blabla ,blublub',NA\n"
            ),
            utils.CsvEvaluationResult(
                line_separator="\n",
                parsed_line_count=2,
                column_separator=",",
                has_header=True,
                header=[
                    "int_col",
                    "bool_col",
                    "datetime_ms_col",
                    "datetime_col",
                    "time_col",
                    "text_with_quoted_seperator_col",
                    "None",
                ],
                column_types=["int", "bool", "datetime", "datetime", "time", "str", "NoneType"],
                column_count=7,
                quoting_character="'",
            ),
        )

    def test_csv_bytes_col_names(self):
        self.assertEqual(
            utils.eval_csv("invalid_column,,123,'bla,blub'\n", ".!@#$%^&*()+?=<>/\\ "),
            utils.CsvEvaluationResult(
                line_separator="\n",
                parsed_line_count=1,
                column_separator=",",
                has_header=False,
                column_types=["str", "NoneType", "int", "str"],
                column_count=4,
                quoting_character="'",
                header=None,
            ),
        )
