import calendar
from datetime import date
import config as cfg
from utils.jira import search_issues
from utils.time import time_humanize, str_to_secs


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


def report(args):
    now = date.today()
    if now.month > 1:
        for_date = now.replace(month=now.month - 1, day=1)
    else:
        for_date = now.replace(year=now.year - 1, month=12, day=1)

    print "################# ISSUES ##################"

    issues_secs = calc_total(search_issues(for_date))

    print("ISSUES TIME = {issues_time} ({issues_time_hours})".format(
        issues_time=time_humanize(issues_secs),
        issues_time_hours=time_humanize(issues_secs, True)
    ))

    print ""
    print "############### HOLIDAYS ##################"

    work_days = calc_work_days(for_date)
    work_days_sec = work_days * cfg.HOURS_IN_DAY * 60 * 60

    holidays = calc_holidays(for_date.month)
    holidays_sec = holidays * cfg.HOURS_IN_DAY * 60 * 60

    print ""
    print "################# OVERALL ##################"
    # TODO: should be interactively requested
    additional_work = str_to_secs("3d 4h 30m")

    efficiency = calc_efficiency(issues_secs + additional_work, work_days_sec, holidays_sec)

    print("WORK DAYS = {work_days}d ({work_days_hours})".format(
        work_days=work_days,
        work_days_hours=time_humanize(work_days_sec, True)
    ))

    print("HOLIDAY DAYS = {holidays}d ({holidays_hours})".format(
        holidays=holidays,
        holidays_hours=time_humanize(holidays_sec, True)
    ))

    print "EFFICIENCY = {efficiency}".format(efficiency=efficiency)