from datetime import datetime, timedelta, timezone
from ipaddress import ip_address
import sys
import unittest
from uuid import UUID

import filet.cpputils as utils


class TestEvalType(unittest.TestCase):
    """Tests for eval_type."""

    def test_py_str_conversation(self):
        self.assertEqual(
            str(utils.eval_type(str(utils.eval_type("2006-03-17 13:27:54.123+00:00")))),
            "2006-03-17 13:27:54.123000+00:00",
        )
        self.assertEqual(
            str(utils.eval_type(str(utils.eval_type("13:27:54.123+00:00")))),
            "13:27:54.123000+00:00",
        )

    def test_none(self):
        [self.assertEqual(utils.eval_type(str(x)), None) for x in ["''", '""', ""]]

    def test_dot(self):
        self.assertEqual(utils.eval_type("'.'"), ".")

    def test_integer(self):
        [self.assertEqual(utils.eval_type(str(x)), x) for x in [*range(10), sys.maxsize, -sys.maxsize]]

    def test_float(self):
        [self.assertEqual(utils.eval_type(str(x)), x) for x in [0.1, 1.0, 0.0, -0.1, 0.00000000000000000012312301]]

    def test_ipv4(self):
        [self.assertEqual(utils.eval_type(x), ip_address(x)) for x in ["1.1.1.1", "1:1:1:1:1:1:1:1"]]
        # wrong
        [
            self.assertEqual(utils.eval_type(x), x)
            for x in ["1.1.1.01", "1:1:1:1:1:1:1:x", "0.0.0.256", "::1", ":::::::", "..."]
        ]

    def test_ipv6(self):
        [
            self.assertEqual(utils.eval_type(x), ip_address(x))
            for x in [
                "2001:db8:85a3::8a2e:370:7334",
                "1:2:3:4:5:6:7:8",
                "0:0:0:0:0:0:0:2",
                "1:2:3:4:5:6::7",
                "::1:2:3:4:5:6:7",
                "1:2:3:4:5:6:7::",
            ]
        ]
        # bad
        [
            self.assertEqual(utils.eval_type(x), x)
            for x in [
                "::5000",  # valid but in eval_type ony with min 6 of `:`
                "5000::",
                "0:1:2:3:4:5:6::7",
                "0::1:2:3:4:5:6:7",
                "0:1:2::3:4:5:6:7",
                "::1:2:3:4:5:6:7:8",
                "1:2:3:4:5:6:7:8::",
                "0:1:2:3:4:5:6:7:8:9",
                "::5000::",
                "5::3::4",
                "::5::4::",
                "::5::4",
                "4::5::",
                "1::2:3::4",
                "1:2",
                "2:::5",
                "1::2::5",
                ":4:",
                ":7",
                "7:",
                ":5:2",
                "5:2:",
                "1:2:3:4:5:6:7",
                ":::::",
                ":::",
                "::n::",
                "0::1",
                "::0:0000:0",
                "::",
                "::1",
                "2001:db8:85a3::8a2e:370:7334:",
                ":2001:db8:85a3::8a2e:370:7334",
                "20012:db8:85a3::8a2e:370:7334",
                "20012:20012:20012:20012:20012:20012:20012:20012",
            ]
        ]

    def test_timestamp_formats(self):
        [
            self.assertTrue(type(utils.eval_type(str(x))) in [datetime])
            for x in [
                "20060317 13:27:54.123",
                "2006/03/17 13:27:54.123",
                "17/03/2006 13:27:54.123",
                "20060317 13:27:54",
                "2006/03/17 13:27:54",
                "17/03/2006 13:27:54",
                "2006-03-17 13:27:54.123",
                "17-03-2006 13:27:54.123",
                "2006-03-17 13:27:54",
                "17-03-2006 13:27:54",
                "2006-03-17T13:27:54",
                "2006-03-17T13:27:54.123",
                "20060317T13:27:54",
                "20060317T13:27:54.123",
                "17-03-2006T13:27:54.123",
                "17-03-2006T13:27:54",
                "2006-03-17T13:27:54Z",
                "2006-03-17T13:27:54+03:45",
                "2006-03-17T13:27:54-05:37",
                "2006-03-17T13:27Z",
                "2006-03-17T13:27+03:45",
                "2006-03-17T13:27-05:37",
                "17/Mar/2006:13:27:54 -0537",
                "17/Mar/2006:13:27:54 +0537",
                "Sat, 17 Mar 2006 13:27:54 GMT",
                "Sat, 17 Mar 2006 13:27:54 EST",
                "Sat, 17 Mar 2006 13:27:54 UT",
                "Sat, 17 Mar 2006 13:27:54 M",
                "Sat, 17 Mar 2006 13:27:54 -0234",
                "Sat, 17 Mar 2006 13:27:54 +0325",
                "2006-03-17 13:27:54.123123+10:00",
                "2006-03-17 13:27:54.123+10:00",
            ]
        ]

    def test_timestamp_values(self):
        self.assertEqual(
            str(utils.eval_type("Sat, 17 Mar 2006 13:27:54 +0325")),
            "2006-03-17 13:27:54+03:25",
        )
        self.assertEqual(str(utils.eval_type("20060317 13:27:54.123")), "2006-03-17 13:27:54.123000+00:00")
        self.assertEqual(str(utils.eval_type("Sat, 17 Mar 2006 13:27:54 EST")), "2006-03-17 13:27:54-05:00")
        self.assertEqual(utils.eval_type("Sat, 17 Mar 2006 13:27:54 -0234").year, 2006)
        self.assertEqual(utils.eval_type("Sat, 17 Mar 2006 13:27:54 -0234").day, 17)
        self.assertEqual(utils.eval_type("Sat, 17 Mar 2006 13:27:54 -0234").month, 3)
        self.assertEqual(utils.eval_type("Sat, 17 Mar 2006 13:27:54 -0234").hour, 13)
        self.assertEqual(utils.eval_type("Sat, 17 Mar 2006 13:27:54 -0234").minute, 27)
        self.assertEqual(utils.eval_type("Sat, 17 Mar 2006 13:27:54 -0234").second, 54)
        self.assertEqual(utils.eval_type("Sat, 17 Mar 2006 13:27:54 -0234").microsecond, 0)
        days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
        self.assertEqual(days[utils.eval_type("Sat, 17 Mar 2006 13:27:54 -0234").isoweekday()], "Saturday")
        self.assertEqual(
            utils.eval_type("Sat, 17 Mar 2006 13:27:54 -0234").tzinfo,
            timezone(timedelta(-1, 77160)),
        )

    def test_wrong_timestamp_values(self):
        self.assertEqual(
            utils.eval_type("2017-01-01 24:23:23"),
            "2017-01-01 24:23:23",
        )

    def test_uuid(self):
        self.assertEqual(
            utils.eval_type("123e4567-e89b-12d3-a456-426655440000"),
            UUID("123e4567-e89b-12d3-a456-426655440000"),
        )

    def test_hex(self):
        self.assertEqual(
            utils.eval_type("0xa"),
            10,
        )
        self.assertEqual(
            utils.eval_type("0xFF"),
            255,
        )

    def test_json(self):
        [self.assertEqual(utils.eval_type(x), eval(x)) for x in ['{"test": 1}', "[1, 2, 3]"]]
