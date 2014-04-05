import re
from jirareport.config import settings


def str_to_secs(time):
    rege = r"[0-9]* *[wdhms]"
    parts = [item.replace(u" ", u"") for item in re.findall(rege, time)]

    in_secs = 0
    for part in parts:
        unit = part[-1]
        amount = int(part[:-1])

        if unit == "w":
            in_secs += amount * settings.DAYS_IN_WEEK * settings.HOURS_IN_DAY * 60 * 60
        elif unit == "d":
            in_secs += amount * settings.HOURS_IN_DAY * 60 * 60
        elif unit == "h":
            in_secs += amount * 60 * 60
        elif unit == "m":
            in_secs += amount * 60
        elif unit == "s":
            in_secs += amount

    return in_secs


def time_humanize(time_in_sec, hours_only=False):
    if not type(time_in_sec) == int:
        return " - "

    days = time_in_sec / (3600 * settings.HOURS_IN_DAY)
    weeks = days / settings.DAYS_IN_WEEK
    days = days % settings.DAYS_IN_WEEK
    hours = time_in_sec % (3600 * settings.HOURS_IN_DAY) / 3600
    mins = time_in_sec % (3600 * settings.HOURS_IN_DAY) % 3600 / 60

    res = []

    if not hours_only:
        if weeks > 0:
            res.append("{weeks}w".format(weeks=weeks))

        if days > 0:
            res.append("{days}d".format(days=days))

        if hours > 0:
            res.append("{hours}h".format(hours=hours))

        if mins > 0:
            res.append("{mins}m".format(mins=mins))
    else:
        hours = weeks * settings.DAYS_IN_WEEK * settings.HOURS_IN_DAY + days * settings.HOURS_IN_DAY + hours + mins / 60.0
        if hours > 0:
            res.append("{hours:.1f}h".format(hours=hours))

    return " ".join(res)


def days_to_sec(days):
    return days * settings.HOURS_IN_DAY * 60 * 60