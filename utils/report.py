import calendar
from datetime import date
import config as cfg
from utils.time import time_humanize


def calc_total(json_response):
    total_time = 0

    for issue in json_response["issues"]:
        summary = issue["fields"]["summary"]
        estimate = issue['fields']['aggregatetimeoriginalestimate']  # in seconds

        print issue["key"] + " | " + time_humanize(estimate) + " | " + summary

        if type(estimate) == int:
            total_time += estimate

    return total_time


def calc_holidays(month):
    days = 0
    for name, info in cfg.HOLIDAYS.items():
        if info["month"] == month:
            if type(info["day"]) == int:
                print "{date:02d}.{month:02d} - {name}".format(date=info["day"], month=month, name=name)
            else:
                print "{date}.{month:02d} - {name}".format(
                    date=",".join(
                        ["{date:02d}".format(date=x) for x in info["day"]]
                    ),
                    month=month,
                    name=name
                )

            if type(info["day"]) == int:
                days += 1
            else:
                days += len(info["day"])

    return days


def calc_work_days(for_date):
    """Count work days in date.month"""
    assert type(for_date) == date

    work_days = 0
    calend = calendar.Calendar()
    for day in calend.itermonthdates(for_date.year, for_date.month):
        work_days += int((for_date.month == day.month) and (day.weekday() in xrange(5)))

    return work_days


def calc_efficiency(issues_time_sec, work_days_sec, holidays_sec=0):
    return 1.0 * issues_time_sec / (work_days_sec - holidays_sec)