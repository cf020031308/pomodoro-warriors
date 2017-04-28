# coding: utf8
# generate weekly report by the use of taskwarrior

import os
import sys
import time
import json
import email
import email.message
import smtplib
import datetime
import commands
import traceback
import subprocess

import jinja2

import utils
from settings import (
    WEEKLY_FILTER,
    AUTHOR, MAIL_SERVER, MAIL_ACCOUNT, MAIL_TO, MAIL_CC)


UDA_TRACKED = 'tracked'
MAIL_DATE_FMT = '%Y%m%d'
FILTER_DATE_FMT = '%Y-%m-%d'

now = int(time.time())
today = datetime.date.today()

# dones: doing/done tasks from ((last_report_day + 1) or this_monday) on
dirname = os.path.dirname(os.path.realpath(__file__))
mail_path = os.path.join(dirname, '.report.eml')
mail_swp_path = os.path.join(dirname, '.report_tmp.eml')
if len(sys.argv) > 1:
    filter_startdate = datetime.datetime.strptime(sys.argv[1], MAIL_DATE_FMT)
elif os.path.exists(mail_path):
    with open(mail_path) as f:
        filter_startdate = datetime.datetime.strptime(
            email.message_from_file(f)['Subject'].strip().rsplit('~', 1)[-1],
            MAIL_DATE_FMT) + datetime.timedelta(days=1)
else:
    filter_startdate = today - datetime.timedelta(days=today.weekday())
filter_starttime = int(time.mktime(filter_startdate.timetuple()))

dones = utils.get_modified_tasks(filter_starttime, filter=WEEKLY_FILTER)

# todos: scheduled tasks before next weekend by projects
_filter = '+PENDING scheduled.before:%s' % (
    today + datetime.timedelta(days=14 - today.weekday())
).strftime(FILTER_DATE_FMT)
todos = json.loads(commands.getoutput(
    'task %s %s export' % (WEEKLY_FILTER, _filter)))


# generate mail subject and content
msg = email.message.Message()
msg['From'] = MAIL_ACCOUNT[0]
msg['To'] = email.utils.COMMASPACE.join(MAIL_TO)
if MAIL_CC:
    msg['Cc'] = email.utils.COMMASPACE.join(MAIL_CC)
msg['Date'] = email.utils.formatdate(localtime=True)
msg['Subject'] = (
    u'[周报][%s]%s~%s' % (
        AUTHOR,
        datetime.datetime.fromtimestamp(
            min(task[UDA_TRACKED][0][0] for task in dones if task[UDA_TRACKED])
        ).strftime(MAIL_DATE_FMT),
        datetime.datetime.fromtimestamp(
            max(task[UDA_TRACKED][-1][1]
                for task in dones if task[UDA_TRACKED])
        ).strftime(MAIL_DATE_FMT))
).encode('utf8')
msg.set_payload(jinja2.Template(u'''
本周工作:
  {%- for project, tasks in dones | groupby(attribute='project') %}
  * {{ project }}
    {%- for task in tasks | sort(attribute='modified') %}
    - {{ task.description }}
    {%- endfor %}
  {%- endfor %}

下周计划:
  {%- for project, tasks in todos | groupby(attribute='project') %}
  * {{ project }}
    {%- for task in tasks | sort(attribute='scheduled') %}
    - {{ task.description }}
    {%- endfor %}
  {%- endfor %}

jjyy:
  无''').render({'dones': dones, 'todos': todos}).encode('utf8'))
with open(mail_swp_path, 'w') as f:
    f.write(msg.as_string())

# edit mail with vim and then confirm to send
subprocess.check_call(['vim', '-n', mail_swp_path])
with open(mail_swp_path) as f:
    msg = email.message_from_file(f)


try:
    assert 'y' == raw_input(
        '%s\n##########\ninput "y" to send\n' % msg.as_string()), 'abort'
    smtp = smtplib.SMTP_SSL(*MAIL_SERVER)
    smtp.login(*MAIL_ACCOUNT)
    smtp.sendmail(
        msg['From'],
        [
            addr.rstrip(email.utils.COMMASPACE)
            for field in ('To', 'Cc')
            for addr in msg[field].split()],
        msg.as_string())
    smtp.quit()
    os.rename(mail_swp_path, mail_path)
except:
    traceback.print_exc()
    os.remove(mail_swp_path)
