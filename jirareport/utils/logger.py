import datetime
import os
from jirareport.config import settings
from jirareport.utils.time import str_to_secs, time_humanize
from jirareport.utils.models import LogItem


def get_log_file_path(year, month):
    return os.path.join(settings.LOG_DIR_PATH, u"storage/{month}-{year}.txt".format(month=month, year=year))


def log(args):
    how_long = time_humanize(str_to_secs(args.t))
    description = args.m
    when = datetime.datetime.strptime(args.d, settings.LOG_DATE_FORMAT).date()
    typ = args.type

    try:
        os.makedirs(os.path.join(settings.LOG_DIR_PATH, "storage"))
    except OSError:
        pass

    log_path = get_log_file_path(month=when.month, year=when.year)

    with open(log_path, "a") as f:
        f.write(u"{when}{sep}{how_long}{sep}{typ}{sep}{description}\n".format(
            sep=settings.LOG_SEPARATOR,
            when=when.strftime(settings.LOG_DATE_FORMAT),
            how_long=how_long,
            description=description,
            typ=typ,
        ))


def calc_log_in_secs(year, month, types=None, except_types=[]):
    summary = 0
    log = []

    file_name = get_log_file_path(month=month, year=year)
    if not os.path.exists(file_name):
        return summary, log

    with open(file_name, "r") as f:
        for line in f:
            line = line.strip()
            if len(line) > 0:
                parts = line.split(settings.LOG_SEPARATOR)
                how_long = parts[1]
                typ = parts[2]

                if (types is None or typ in types) and (typ not in except_types):
                    log.append(LogItem(
                        datetime.datetime.strptime(parts[0], settings.LOG_DATE_FORMAT),
                        typ,
                        str_to_secs(how_long),
                        settings.LOG_SEPARATOR.join(parts[3:])
                    ))
                    summary += str_to_secs(how_long)

    return summary, log
