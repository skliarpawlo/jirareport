import os
import imp
import jirareport.default_config as settings


config_path = os.environ.get("JIRA_REPORT_CONFIG")

if config_path is None:
    raise ValueError("Please specify settings file as JIRA_REPORT_CONFIG environment variable")

custom_config = imp.load_source("custom_config", config_path)

for key in dir(custom_config):
    if hasattr(settings, key):
        setattr(settings, key, getattr(custom_config, key))
