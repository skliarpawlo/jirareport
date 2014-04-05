import base64
import calendar
from httplib import HTTPSConnection
import json
import urllib
from jirareport import config as cfg


def search_issues(for_date):
    search_api_path = "/rest/api/2/search"

    days_in_month = calendar.monthrange(for_date.year, for_date.month)[1]
    start_date = for_date.replace(day=1)
    end_date = for_date.replace(day=days_in_month)

    jql = "project = {project_id} AND status in (Resolved, Closed) AND resolved >= {start_date} AND resolved <= {end_date} AND assignee in ({user})".format(
        project_id=cfg.PROJECT_ID,
        start_date=start_date.strftime("%Y-%m-%d"),
        end_date=end_date.strftime("%Y-%m-%d"),
        user=cfg.USER,
    )

    params = urllib.urlencode({"jql": jql})

    conn = HTTPSConnection(cfg.JIRA_URL)

    auth_b64 = base64.b64encode(bytes("{user}:{password}".format(user=cfg.USER, password=cfg.PASSWORD)))
    conn.request("GET", search_api_path + "?" + params, headers={"Authorization": "Basic " + auth_b64})

    resp = conn.getresponse()

    json_response = json.loads(resp.read())
    return json_response