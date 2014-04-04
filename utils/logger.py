import datetime
import os
from time import str_to_secs, time_humanize

SEPARATOR = u" - "


def log(args):
    how_long = time_humanize(str_to_secs(args.t))
    description = args.m
    when = datetime.datetime.strptime(args.d, u"%Y/%m/%d").date()
    typ = args.type

    with open(u"storage/{month}-{year}.txt".format(month=when.month, year=when.year), "a") as f:
        f.write(u"{when}{sep}{how_long}{sep}{typ}{sep}{description}\n".format(
            sep=SEPARATOR,
            when=when.strftime("%Y/%m/%d"),
            how_long=how_long,
            description=description,
            typ=typ,
        ))


def calc_log_in_secs(year, month, types=None, except_types=[]):
    summary = 0

    file_name = u"storage/{month}-{year}.txt".format(month=month, year=year)
    if not os.path.exists(file_name):
        return 0

    with open(file_name, "r") as f:
        for line in f:
            line = line.strip()
            if len(line) > 0:
                parts = line.split(SEPARATOR)
                how_long = parts[1]
                typ = parts[2]

                if (types is None or typ in types) and (typ not in except_types):
                    print line
                    summary += str_to_secs(how_long)

    return summary
