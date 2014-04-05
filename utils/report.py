import calendar
from datetime import date
import config as cfg
from jira import search_issues
from logger import calc_log_in_secs
from time import time_humanize, days_to_sec
from utils.models import Issue, Holiday, Report
from utils.presenters.text import render as text_render


def calc_total(json_response):
    total_time = 0
    log = []

    for issue in json_response["issues"]:
        summary = issue["fields"]["summary"]
        estimate = issue['fields']['aggregatetimeoriginalestimate']  # in seconds

        log.append(
            Issue(issue["key"], time_humanize(estimate), summary)
        )

        if type(estimate) == int:
            total_time += estimate

    return total_time, log


def calc_national_holidays(month):
    days = 0
    log = []
    for name, info in cfg.HOLIDAYS.items():
        if info["month"] == month:
            if type(info["day"]) == int:
                log.append(Holiday(
                    u"{date:02d}.{month:02d}".format(date=info["day"], month=month),
                    name,
                ))
            else:
                log.append(Holiday(
                    u"{date}.{month:02d}".format(date=",".join(
                        ["{date:02d}".format(date=x) for x in info["day"]]
                    ), month=month),
                    name,
                ))

            if type(info["day"]) == int:
                days += 1
            else:
                days += len(info["day"])

    return days, log


def calc_work_days(for_date):
    """Count work days in date.month"""
    assert type(for_date) == date

    work_days = 0
    calend = calendar.Calendar()
    for day in calend.itermonthdates(for_date.year, for_date.month):
        work_days += int((for_date.month == day.month) and (day.weekday() in xrange(5)))

    return work_days


def calc_efficiency(issues_time_sec, work_days_sec):
    return 1.0 * issues_time_sec / work_days_sec


def calc_total_sec(issues, add, holi, eff):
    return int(issues + add + holi * eff)


def calc_presence(for_date):
    work_days = calc_work_days(for_date)
    work_days_sec = work_days * cfg.HOURS_IN_DAY * 60 * 60

    unpayed_holidays_sec, log = calc_log_in_secs(year=for_date.year, month=for_date.month, except_types=['work', 'vacation', 'ill'])
    return (work_days_sec - unpayed_holidays_sec) / (1.0 * work_days_sec)


def calc_all(for_date):
    issues_secs, issues_log = calc_total(search_issues(for_date))
    additional_work_sec, additional_work_log = calc_log_in_secs(year=for_date.year, month=for_date.month, types=['work'])

    national_holidays, national_holidays_log = calc_national_holidays(for_date.month)
    national_holidays_sec = days_to_sec(national_holidays)

    payed_holidays_sec, payed_holidays_log = calc_log_in_secs(year=for_date.year, month=for_date.month, types=['vacation', 'ill'])
    payed_holidays_sec += national_holidays_sec

    work_days = calc_work_days(for_date)
    work_days_sec = days_to_sec(work_days)

    unpayed_holidays_sec, unpayed_holidays_log = calc_log_in_secs(year=for_date.year, month=for_date.month, except_types=['work', 'vacation', 'ill'])

    presence = calc_presence(for_date)

    efficiency = calc_efficiency(
        issues_secs,
        work_days_sec - payed_holidays_sec,
    )

    total = calc_total_sec(issues_secs, additional_work_sec, national_holidays_sec + payed_holidays_sec, efficiency)

    return Report(
        efficiency=efficiency,
        national_holidays_sec=national_holidays_sec,
        payed_holidays_sec=payed_holidays_sec,
        unpayed_holidays_sec=unpayed_holidays_sec,
        presence=presence,
        total_issues_time=total,
        # logs
        issues_log=issues_log,
        payed_holidays_log=payed_holidays_log,
        unpayed_holidays_log=unpayed_holidays_log,
        national_holidays_log=national_holidays_log,
    )


def report(args):
    for_date = date(args.y, args.m, 1)
    report_data = calc_all(for_date)
    text_render(report_data)
