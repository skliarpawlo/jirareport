import unittest
from make import time_humanize


class TestTimeHumanize(unittest.TestCase):
    def test_basic(self):
        suite = [
            {"days": 1, "hours": 20, "minutes": 0},
            {"days": 5, "hours": 20, "minutes": 23},
            {"days": 20, "hours": 20, "minutes": 59},
            {"days": 0, "hours": 20, "minutes": 50},
            {"days": 0, "hours": 0, "minutes": 45},
            {"days": 0, "hours": 0, "minutes": 0},
        ]

        for test in suite:
            days = test["days"]
            hours = test["hours"]
            minutes = test["minutes"]

            in_secs = days * 24 * 3600 + hours * 3600 + minutes * 60

            res = time_humanize(in_secs)

            waited_res = []
            if days > 0:
                waited_res.append(str(days) + "d")
            if hours > 0:
                waited_res.append(str(hours) + "h")
            if minutes > 0:
                waited_res.append(str(minutes) + "m")

            waited_res = " ".join(waited_res)

            self.assertEqual(res, waited_res)

    def test_overflows(self):
        suite = [
            {"days": 3, "hours": 25, "minutes": 0, "ans": "4d 1h"},
            {"days": 5, "hours": 20, "minutes": 120, "ans": "5d 22h"},
        ]

        for test in suite:
            days = test["days"]
            hours = test["hours"]
            minutes = test["minutes"]

            in_secs = days * 24 * 3600 + hours * 3600 + minutes * 60

            res = time_humanize(in_secs)

            self.assertEqual(res, test["ans"])

