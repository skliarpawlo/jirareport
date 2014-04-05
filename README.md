Jira Report
===========
Small util to make monthly work reports. Written in pure python.

Usage:
======

Create report:

    make.py report [-h] [-m month] [-y year] [--format format]

    subcommand for makeing monthly reports

    optional arguments:
      -h, --help       show this help message and exit
      -m month         for what month to make report
      -y year          for what year to make report
      --format format  text | html


    *html is not supported yet

Log work:

    make.py log [-h] -m message -t time [-d y/m/d] [--type type]

    subcommand for logging additional activities such as long time meetings

    optional arguments:
      -h, --help   show this help message and exit
      -m message   activity description
      -t time      time (like 1d 3h)
      -d y/m/d     when (y/m/d)
      --type type  Payed: work | ill | vacation, Not payed: any other


Installation:
=============

pip:

    pip install {git_repo}

manual:

    git clone {git_repo}


Configuration:
==============

Set env variable JIRA_REPORT_CONFIG value to config file path. Config file should be a pure python module.
Sample configuration file:

    import os

    JIRA_URL = ""
    USER = ""
    PASSWORD = ""
    PROJECT_ID = ""
    DAYS_IN_WEEK = 5
    HOURS_IN_DAY = 8
    LOG_DIR_PATH = os.path.join("jirareport", "storage")

    HOLIDAYS = {
        u"New Year": { "month": 1, "day": 1 },
        u"Christmas": { "month": 1, "day": 7 },
        u"Woman day": { "month": 3, "day": 8 },
        u"Easter": { "month": 4, "day": 20 },
        u"Days of International Solidarity": { "month": 5, "day": [1, 2] },
        u"Glory day": { "month": 5, "day": 9 },
        u"Whit Sunday": { "month": 7, "day": 8 },
        u"Day of Ukrainian Constitution": { "month": 7, "day": 28 },
        u"Ukraine Independance Day": { "month": 8, "day": 24 },
    }
