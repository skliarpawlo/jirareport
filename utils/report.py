import calendar
from datetime import date
import config as cfg
from jira import search_issues
from logger import calc_log_in_secs
from time import time_humanize


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


def calc_efficiency(issues_time_sec, work_days_sec):
    return 1.0 * issues_time_sec / work_days_sec


def calc_total_sec(issues, add, holi, eff):
    return int(issues + add + holi * eff)


def report(args):

    for_date = date(args.y, args.m, 1)

    print ""
    print "############### JIRA ISSUES ##############"

    issues_secs = calc_total(search_issues(for_date))

    print ""
    print "############ ADDITIONAL LOG ##############"
    additional_work_sec = calc_log_in_secs(year=for_date.year, month=for_date.month, types=['work'])

    print ""
    print "############### HOLIDAYS ##################"
    print "############### PAYED ####################"
    print "National:"
    national_holidays = calc_holidays(for_date.month)
    national_holidays_sec = national_holidays * cfg.HOURS_IN_DAY * 60 * 60

    print "Own:"
    payed_holidays_sec = national_holidays_sec + calc_log_in_secs(year=for_date.year, month=for_date.month, types=['vacation', 'ill'])

    print "############### NOT PAYED ####################"
    unpayed_holidays_sec = calc_log_in_secs(year=for_date.year, month=for_date.month, except_types=['work', 'vacation', 'ill'])

    print ""
    print "##############################################"

    work_days = calc_work_days(for_date)
    work_days_sec = work_days * cfg.HOURS_IN_DAY * 60 * 60
    print("WORK DAYS = {work_days}d ({work_days_hours})".format(
        work_days=work_days,
        work_days_hours=time_humanize(work_days_sec, True)
    ))

    print("SUMMARY PRESENCE IN OFFICE = PRESENCE_DAYS({present_days}) + PAYED_VACATION({vacation}) / WORK_DAYS({work_days}) = {percent:.1f}%".format(
        present_days=time_humanize(work_days_sec - unpayed_holidays_sec - payed_holidays_sec, True),
        vacation=time_humanize(payed_holidays_sec, True),
        work_days=time_humanize(work_days_sec, True),
        percent=100.0 * (work_days_sec - unpayed_holidays_sec) / work_days_sec,
    ))

    print("ISSUES TIME = {issues_time} ({issues_time_hours})".format(
        issues_time=time_humanize(issues_secs),
        issues_time_hours=time_humanize(issues_secs, True)
    ))

    if additional_work_sec > 0:
        print("ADDITIONAL LOG = {additional_work} ({additional_work_hours})".format(
            additional_work=time_humanize(additional_work_sec),
            additional_work_hours=time_humanize(additional_work_sec, True),
        ))

    if national_holidays_sec > 0:
        print("HOLIDAY DAYS = {holidays}d ({holidays_hours})".format(
            holidays=national_holidays,
            holidays_hours=time_humanize(national_holidays_sec, True)
        ))

    efficiency = calc_efficiency(
        issues_secs,
        work_days_sec - payed_holidays_sec,
    )
    print "EFFICIENCY = {efficiency:.2f}%".format(efficiency=100.0 * efficiency)

    total = calc_total_sec(issues_secs, additional_work_sec, national_holidays_sec + payed_holidays_sec, efficiency)
    print "TOTAL ISSUES TIME = ISSUES_TIME + ADDITIONAL_LOG + HOLIDAYS * EFFICIENCY = {total}".format(
        total=time_humanize(total, True)
    )
