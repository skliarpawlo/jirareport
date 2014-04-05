class Issue(object):
    def __init__(self, key, estimate, summary):
        self.key = key
        self.estimate = estimate
        self.summary = summary


class Holiday(object):
    def __init__(self, date, name):
        self.date = date
        self.name = name


class Report(object):
    def __init__(self, efficiency, national_holidays_sec, payed_holidays_sec, unpayed_holidays_sec,
                 presence, issues_log, payed_holidays_log, unpayed_holidays_log, national_holidays_log,
                 total_issues_time):
        self.efficiency = efficiency
        self.national_holidays_sec = national_holidays_sec
        self.payed_holidays_sec = payed_holidays_sec
        self.unpayed_holidays_sec = unpayed_holidays_sec
        self.presence = presence
        self.total_issues_time = total_issues_time

        self.issues_log = issues_log
        self.payed_holidays_log = payed_holidays_log
        self.unpayed_holidays_log = unpayed_holidays_log
        self.national_holidays_log = national_holidays_log


class LogItem(object):
    def __init__(self, when, kind, how_long, description):
        self.when = when
        self.kind = kind
        self.how_long = how_long
        self.description = description