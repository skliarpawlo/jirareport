from datetime import date
import config as cfg
from utils.jira import search_issues
from utils.report import calc_total, calc_holidays, calc_work_days, calc_efficiency
from utils.time import time_humanize, str_to_secs


def solve(for_date):
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


if __name__ == "__main__":
    now = date.today()
    if now.month > 1:
        for_prev = now.replace(month=now.month - 1, day=1)
    else:
        for_prev = now.replace(year=now.year - 1, month=12, day=1)

    solve(for_prev)