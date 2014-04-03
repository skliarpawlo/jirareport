import unittest
import utils.time


class TestTimeHumanize(unittest.TestCase):
    def test_time_humanize_basic(self):
        suite = [
            {"days": 1, "hours": 3, "minutes": 0},
            {"days": 4, "hours": 4, "minutes": 23},
            {"days": 0, "hours": 7, "minutes": 50},
            {"days": 0, "hours": 0, "minutes": 45},
            {"days": 0, "hours": 0, "minutes": 0},
        ]

        for test in suite:
            days = test["days"]
            hours = test["hours"]
            minutes = test["minutes"]

            in_secs = days * utils.time.cfg.HOURS_IN_DAY * 3600 + hours * 3600 + minutes * 60

            res = utils.time.time_humanize(in_secs)

            waited_res = []
            if days > 0:
                waited_res.append(str(days) + "d")
            if hours > 0:
                waited_res.append(str(hours) + "h")
            if minutes > 0:
                waited_res.append(str(minutes) + "m")

            waited_res = " ".join(waited_res)

            self.assertEqual(res, waited_res)

    def test_time_humanize_overflows(self):
        suite = [
            {"days": 3, "hours": 9, "minutes": 0, "ans": "4d 1h"},
            {"days": 2, "hours": 0, "minutes": 120, "ans": "2d 2h"},
        ]

        for test in suite:
            days = test["days"]
            hours = test["hours"]
            minutes = test["minutes"]

            in_secs = days * utils.time.cfg.HOURS_IN_DAY * 3600 + hours * 3600 + minutes * 60

            res = utils.time.time_humanize(in_secs)

            self.assertEqual(res, test["ans"])


class TestStrToSecs(unittest.TestCase):
    def test_str_to_secs_basic(self):
        tests = [
            {"input": "1d 1h 1m", "output": 1 * utils.time.cfg.HOURS_IN_DAY * 60 * 60 + 1 * 60 * 60 + 1 * 60},
        ]

        for test in tests:
            self.assertEqual(utils.time.str_to_secs(test["input"]), test["output"])