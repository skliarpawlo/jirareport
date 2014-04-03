import datetime
from utils.time import str_to_secs, time_humanize


def log(args):
    how_long = time_humanize(str_to_secs(args.t))
    description = args.m
    when = datetime.date.today()

    print "{date} - {time} : {description}".format(
        date=when.strftime("%Y/%m/%d"),
        time=how_long,
        description=description
    )