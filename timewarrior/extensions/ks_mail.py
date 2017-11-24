#!/usr/local/bin/python
# coding: utf8

'''
This script generates report and mails it to my colleagues (of Knownsec).
So it suits only my work alone, but can be an example to others.

The project of every task related to work is named as `ks.*`.
And I always start my work by executing `timew start ks`.

Preview:   `timew ks_mail ks :week`
Real Send: `timew ks_mail ks :week :yes`
'''

import json
import email
import smtplib
import commands
import datetime
import email.message
from collections import OrderedDict

import utils
from utils import settings


def hierachy(task, tasks):
    'Find children according to dependencies'
    ret = OrderedDict()
    depends = task.get('depends')
    if depends:
        for uuid in depends.split(','):
            if uuid in tasks:
                t = tasks.pop(uuid)
                ret.update(hierachy(t, tasks))
    desc = ('! ' if task['status'] == 'active' else '') + task['description']
    return OrderedDict({desc: ret})


def render(gs):
    ret = []
    if isinstance(gs, dict):
        gs = gs.items()
    for p, g in gs:
        ret.append(p)
        if g:
            ret.extend('\t%s' % l for l in render(g).splitlines())
    return '\n'.join(ret)


def renders(tasks):
    tasks = {task['uuid']: task for task in tasks}
    # Group by projects and dependencies
    groups = OrderedDict()
    for uuid in sorted(tasks.keys(), key=lambda i: tasks[i]['modified']):
        if uuid not in tasks:
            continue
        task = tasks.pop(uuid)
        project = task.get('project', '')
        if not project.startswith('ks'):
            continue
        ps = project.split('.')
        gs = groups
        for p in ps[:-1]:
            gs = gs.setdefault(p, OrderedDict())
        gs.setdefault(ps[-1], OrderedDict()).update(hierachy(task, tasks))
    return render(groups)


# Get tracked entries
configs, entries = utils.format_inputs()
assert entries, 'No filtered data found in the range %s - %s.' % tuple(map(
    utils.utc2tz, map(configs['temp']['report'].get, ['start', 'end'])))
if 'end' not in entries[-1]:
    entries[-1]['end'] = datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
start = utils.parse_utc(max(
    entries[0]['start'], configs['temp']['report']['start']))
end = utils.parse_utc(min(
    entries[-1]['end'], configs['temp']['report']['end']))
uuids = set(
    'uuid:%s' % tag
    for entry in entries if 'ks' in entry['tags']
    for tag in entry['tags'] if utils.is_uuid(tag))

# Prepare mail title and content
title = u'[周报][%s]%s~%s' % (
    settings.MAIL_AUTHOR, start.strftime('%Y%m%d'), end.strftime('%Y%m%d'))
payload = '\n\n'.join([
    # Dones
    (
        renders(json.loads(commands.getoutput(
            'task "( %s )" export' % ' or '.join(uuids))))
        if uuids else 'ks'
    ).replace('ks', u'本周工作：', 1),
    # Todos
    (
        renders(json.loads(commands.getoutput(
            'task '
            'project:ks "( +ACTIVE or ( +PENDING scheduled.before:%sday ) )" '
            'export' %
            max(1, (end - start).days))))
        or 'ks'
    ).replace('ks', u'下周计划：', 1),
    u'jjyy:\n\t无',
]).replace('\t', '    ')

# Send Mail
msg = email.message.Message()
msg['From'] = settings.MAIL_ACCOUNT[0]
msg['To'] = email.utils.COMMASPACE.join(settings.MAIL_TO)
if settings.MAIL_CC:
    msg['Cc'] = email.utils.COMMASPACE.join(settings.MAIL_CC)
msg['Date'] = email.utils.formatdate(localtime=True)
msg['Subject'] = title.encode('utf8')
msg.set_payload(payload.encode('utf8'))
if configs['confirmation'] == 'off':
    smtp = smtplib.SMTP_SSL(*settings.MAIL_SERVER)
    smtp.login(*settings.MAIL_ACCOUNT)
    smtp.sendmail(
        msg['From'],
        [
            addr.rstrip(email.utils.COMMASPACE)
            for field in ('To', 'Cc') if msg[field]
            for addr in msg[field].split() if addr],
        msg.as_string())
    smtp.quit()
print(msg.as_string())
