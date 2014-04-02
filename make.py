import base64
from httplib import HTTPSConnection
import json
import urllib
import config


def time_humanize(time_in_sec):
    if not type(time_in_sec) == int:
        return " - "

    days = time_in_sec / (3600 * 24)
    hours = time_in_sec % (3600 * 24) / 3600
    mins = time_in_sec % (3600 * 24) % 3600 / 60
    res = []
    if days > 0:
        res.append("{days}d".format(days=days))

    if hours > 0:
        res.append("{hours}h".format(hours=hours))

    if mins > 0:
        res.append("{mins}m".format(mins=mins))

    return " ".join(res)


def search_issues(cfg):
    search_api_path = "/rest/api/2/search"
    jql = "project = {project_id} AND status in (Resolved, Closed) AND resolved >= {start_date} AND resolved <= {end_date} AND assignee in ({user})".format(
        project_id=cfg.PROJECT_ID,
        start_date="2014-03-01",
        end_date="2014-03-31",
        user=cfg.USER,
    )

    params = urllib.urlencode({"jql": jql})

    conn = HTTPSConnection(cfg.JIRA_URL)

    auth_b64 = base64.b64encode(bytes("{user}:{password}".format(user=cfg.USER, password=cfg.PASSWORD)))
    conn.request("GET", search_api_path + "?" + params, headers={"Authorization": "Basic " + auth_b64})

    resp = conn.getresponse()

    json_response = json.loads(resp.read())
    return json_response


def calc_total(json_response):
    total_time = 0

    for issue in json_response["issues"]:
        summary = issue["fields"]["summary"]
        estimate = issue['fields']['aggregatetimeoriginalestimate']  # in seconds

        print time_humanize(estimate) + " | " + summary

        if type(estimate) == int:
            total_time += estimate

    return total_time


def solve():
    total_secs = calc_total(search_issues(config))
    print("TOTAL = " + time_humanize(total_secs))


if __name__ == "__main__":
    solve()