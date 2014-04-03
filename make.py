from utils.jira import search_issues
from utils.report import calc_total
from utils.time import time_humanize


def solve():
    total_secs = calc_total(search_issues())
    print("TOTAL = " + time_humanize(total_secs) + " (" + time_humanize(total_secs, True) + ")")


if __name__ == "__main__":
    solve()