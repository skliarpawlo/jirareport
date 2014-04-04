import argparse
from utils.logger import log
from utils.report import report

subcommand_parser = argparse.ArgumentParser(description=u"Util for making monthly reports. Includes:"
                                                        u"searching JIRA tasks for period,"
                                                        u"logging additional activities")

subparsers = subcommand_parser.add_subparsers(help=u"sub-commands")

report_parser = subparsers.add_parser(u'report', description=u"subcommand for makeing monthly reports")
report_parser.add_argument(u'-m', metavar=u'month', help=u'for what month to make report', required=False)
report_parser.add_argument(u'-y', metavar=u'year', help=u'for what year to make report', required=False)
report_parser.set_defaults(func=report)

log_parser = subparsers.add_parser(u'log', description=u"subcommand for logging additional activities such as long time meetings")
log_parser.add_argument(u'-m', metavar=u'message', help=u'activity description', required=True)
log_parser.add_argument(u'-t', metavar=u'time', help=u'time (like 1d 3h)', required=True)
log_parser.add_argument(u'--type', metavar=u'type', help=u'Payed: work | ill | vacation, Not payed: any other', required=False)
log_parser.set_defaults(func=log, type=u"work")


if __name__ == "__main__":
    args = subcommand_parser.parse_args()