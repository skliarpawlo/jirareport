from utils.time import time_humanize


def calc_total(json_response):
    total_time = 0

    for issue in json_response["issues"]:
        summary = issue["fields"]["summary"]
        estimate = issue['fields']['aggregatetimeoriginalestimate']  # in seconds

        print issue["key"] + " | " + time_humanize(estimate) + " | " + summary

        if type(estimate) == int:
            total_time += estimate

    return total_time