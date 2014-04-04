import datetime
import os
from utils.time import str_to_secs, time_humanize

SEPARATOR = u" - "


def log(args):
    how_long = time_humanize(str_to_secs(args.t))
    description = args.m
    when = datetime.date.today()
    typ = args.type

    with open(u"storage/{month}-{year}.txt".format(month=when.month, year=when.year), "a") as f:
        f.write(u"{when}{sep}{how_long}{sep}{typ}{sep}{description}".format(
            sep=SEPARATOR,
            when=when.strftime("%Y/%m/%d"),
            how_long=how_long,
            description=description,
            typ=typ,
        ))


def calc_log_in_secs(year, month):
    summary = 0

    file_name = u"storage/{month}-{year}.txt".format(month=month, year=year)
    if not os.path.exists(file_name):
        return 0

    with open(file_name, "r") as f:
        line = f.readline().strip()
        if len(line) > 0:
            parts = line.split(SEPARATOR)
            how_long = parts[1]
            typ = parts[2]

            print line

            if typ in ["work", "ill", "vacation"]:
                summary += str_to_secs(how_long)

    return summary
