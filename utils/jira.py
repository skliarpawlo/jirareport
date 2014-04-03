import base64
from httplib import HTTPSConnection
import json
import urllib
import config as cfg


def search_issues():
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