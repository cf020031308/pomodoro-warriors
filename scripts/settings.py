import os

import yaml


AUTHOR = ''
MAIL_SERVER = ['smtp.163.com', 465]
MAIL_ACCOUNT = ['cf020031308@163.com', '']
MAIL_TO = ['cf020031308@163.com']
MAIL_CC = []

TIMESHEET_HOST = ''
TIMESHEET_ACCOUNT = {'username': '', 'password': ''}
TIMESHEET_PROJECTS = {}


path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'settings.yaml')
if os.path.exists(path):
    with open(path) as f:
        globals().update(yaml.load(f))
