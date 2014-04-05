import datetime
import os
import config as cfg
from time import str_to_secs, time_humanize
from utils.models import LogItem


def log(args):
    how_long = time_humanize(str_to_secs(args.t))
    description = args.m
    when = datetime.datetime.strptime(args.d, cfg.LOG_DATE_FORMAT).date()
    typ = args.type

    with open(u"storage/{month}-{year}.txt".format(month=when.month, year=when.year), "a") as f:
        f.write(u"{when}{sep}{how_long}{sep}{typ}{sep}{description}\n".format(
            sep=cfg.LOG_SEPARATOR,
            when=when.strftime(cfg.LOG_DATE_FORMAT),
            how_long=how_long,
            description=description,
            typ=typ,
        ))


def calc_log_in_secs(year, month, types=None, except_types=[]):
    summary = 0
    log = []

    file_name = u"storage/{month}-{year}.txt".format(month=month, year=year)
    if not os.path.exists(file_name):
        return summary, log

    with open(file_name, "r") as f:
        for line in f:
            line = line.strip()
            if len(line) > 0:
                parts = line.split(cfg.LOG_SEPARATOR)
                how_long = parts[1]
                typ = parts[2]

                if (types is None or typ in types) and (typ not in except_types):
                    log.append(LogItem(
                        datetime.datetime.strptime(parts[0], cfg.LOG_DATE_FORMAT),
                        typ,
                        str_to_secs(how_long),
                        cfg.LOG_SEPARATOR.join(parts[3:])
                    ))
                    summary += str_to_secs(how_long)

    return summary, log
