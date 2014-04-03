import unittest
import datetime
from utils.report import calc_work_days


class TestCalcWorkDays(unittest.TestCase):
    def test_calc_work_days_basic(self):
        self.assertEqual(
            calc_work_days(datetime.date(2014, 3, 1)),
            21
        )
        self.assertEqual(
            calc_work_days(datetime.date(2014, 2, 1)),
            20
        )