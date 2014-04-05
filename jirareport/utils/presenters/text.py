from jirareport import config as cfg
from jirareport.utils.models import Issue, Report, Holiday, LogItem
from jirareport.utils.time import time_humanize


def render_holiday_log(log):
    for holi in log:
        assert isinstance(holi, Holiday)
        print u"{date} | {descr}".format(
            date=holi.date,
            descr=holi.name,
        )


def render_logged_holiday_log(log):
    for item in log:
        assert isinstance(item, LogItem)
        print u"{date} | {how_long} ({how_long_hours}) | {typ} | {descr}".format(
            date=item.when.strftime(cfg.LOG_DATE_FORMAT),
            how_long=time_humanize(item.how_long, True),
            how_long_hours=time_humanize(item.how_long, True),
            typ=item.kind,
            descr=item.description,
        )


def render_issues_log(log):
    for issue in log:
        assert isinstance(issue, Issue)
        print(u"{key} | {estimate} | {summary}".format(
            key=issue.key, estimate=issue.estimate, summary=issue.summary
        ))


def render(report):

    if len(report.issues_log) > 0:
        assert isinstance(report, Report)
        print u"############## ISSUES ({hours}) ################".format(
            hours=time_humanize(report.issues_secs, True)
        )
        render_issues_log(report.issues_log)

    if len(report.additional_work_log) > 0:
        print u""
        print u"######### ADDITIONAL WORK ({hours}) ############".format(
            hours=time_humanize(report.additional_work_sec, True)
        )
        render_logged_holiday_log(report.additional_work_log)

    if len(report.national_holidays_log) > 0 or \
       len(report.payed_holidays_log) > 0 or \
       len(report.unpayed_holidays_log) > 0:
        print u""
        print u"############# HOLIDAYS ###############"
        if len(report.national_holidays_log) > 0:
            print u"National:"
            render_holiday_log(report.national_holidays_log)

        if len(report.payed_holidays_log) > 0:
            print u"Payed:"
            render_logged_holiday_log(report.payed_holidays_log)

        if len(report.unpayed_holidays_log) > 0:
            print u"Not payed:"
            render_logged_holiday_log(report.unpayed_holidays_log)

    print u""
    print u"#####################################"
    print(u"PRESENCE IN OFFICE = {presence:.2f}%".format(
        presence=100.0 * report.presence
    ))
    print(u"EFFICIENCY = {x:.2f}%".format(x=100.0 * report.efficiency))
    print(u"TOTAL_ISSUES_TIME = {time} ({time_hours})".format(
        time=time_humanize(report.total_issues_time),
        time_hours=time_humanize(report.total_issues_time, True),
    ))
