import os

import yaml


WEEKLY_FILTER = '+work project.not:miscellaneous'

AUTHOR = ''
MAIL_SERVER = ['smtp.163.com', 465]
MAIL_ACCOUNT = ['cf020031308@163.com', '']
MAIL_TO = ['cf020031308@163.com']
MAIL_CC = []

DAILY_FILTER = '+work'
TIMESHEET_HOST = ''
TIMESHEET_ACCOUNT = {'username': '', 'password': ''}
TIMESHEET_MAP = {}


path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'settings.yaml')
if os.path.exists(path):
    with open(path) as f:
        globals().update(yaml.load(f))
