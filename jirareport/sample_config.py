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