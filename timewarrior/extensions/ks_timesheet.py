#!/usr/local/bin/python
# coding: utf8

'''
This script fills a timesheet on the server of my company (Knownsec),
reporting what I have done and how long it took.
So it suits only my work alone, but can be an example to others.

The project of every task related to work is named as `ks.*`.
And I always start my work by executing `timew start ks`.

Preview:     `timew ks_timesheet ks :day`
Real Upload: `timew ks_timesheet ks :day :yes`
'''

import json
import commands
import datetime

import jinja2
import requests

import utils
from utils import settings


HOUR_UNIT = 0.25
TAGS = {'dev': u'开发', 'ops': u'运维', 'bug': u'排查'}
template = jinja2.Template(u'''
{%- macro fmt(f) %}
{%- if f %}{{ f }}h{% else %}-{% endif %}
{%- endmacro %}

{%- if tasks %}
{%- for task in tasks | sort(attribute='modified') %}
- {{ task.description }} [{{ fmt(task.estimate) }}/{{ fmt(task.duration) }}]
{%- endfor %}

* 时间格式：[预估工时/实际工时]
{%- endif %}
{%- if tags %}

分类统计：
{%- for tag, duration in tags.items() %}
    - {{ tag }} [{{ (100 * duration / total) | round(1) }}%]
{%- endfor %}
{%- endif %}
''', lstrip_blocks=True)


def dumps(ret):
    return json.dumps(
        ret, indent=2, sort_keys=True, ensure_ascii=False).encode('utf8')


class timesheet(object):
    'Knownsec Timesheet API'
    _TOKEN = None
    _PROJECTS = None

    def API(self, method, uri, **kwargs):
        url = 'http://%s%s' % (settings.TIMESHEET_HOST, uri)
        headers = kwargs.setdefault('headers', {})
        if 'Authorization' not in headers:
            headers['Authorization'] = 'Bearer %s' % self.token
        return requests.request(method.lower(), url, **kwargs)

    @property
    def token(self):
        if not self.__class__._TOKEN:
            self.__class__._TOKEN = self.API(
                'POST',
                '/auth/login',
                data=settings.TIMESHEET_ACCOUNT,
                headers={'Authorization': ''}
            ).json()['token']
            assert self.__class__._TOKEN
        return self.__class__._TOKEN

    @property
    def projects(self):
        if not self.__class__._PROJECTS:
            self.__class__._PROJECTS = {
                project[field]: project
                for project in self.API('GET', '/project').json()
                for field in ('projectId', 'projectName')}
        return self.__class__._PROJECTS

    def put(self, date, project, hours, content):
        assert not (float(hours) % 0.25), (
            'value of working hours should be times of 0.25')
        resp = self.API('POST', '/daily', data={
            'project': None,
            'date': date,
            'hours': str(hours),
            'projectId': self.projects.get(
                project, {}).get('projectId', 'self_define_project_id'),
            'projectName': self.projects.get(
                project, {}).get('projectName', project or 'miscellaneous'),
            'content': content or 'miscellaneous'})
        assert 200 <= resp.status_code < 300, (
            resp.status_code, resp.headers, resp.content)
        return resp

    def get(self, start, end=None):
        return json.loads(filter(None, [
            line.strip()
            for line in self.API(
                    'GET',
                    '/daily',
                    params={
                        'startTime': start,
                        'endTime': end or start
                    }).content.splitlines()])[0])


# Get tracked entries
configs, entries = utils.format_inputs()
assert entries, 'No filtered data found in the range %s - %s.' % tuple(map(
    utils.utc2tz, map(configs['temp']['report'].get, ['start', 'end'])))
if 'end' not in entries[-1]:
    entries[-1]['end'] = datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
start = utils.utc2tz(max(
    entries[0]['start'], configs['temp']['report']['start']))
end = utils.utc2tz(min(entries[-1]['end'], configs['temp']['report']['end']))
day = start.split('T', 1)[0]
assert end.startswith(day), 'Only intervals within one day are supported.'

# Sum up
groups = {}
for entry in entries:
    if 'ks' not in entry['tags']:
        continue
    start = utils.parse_utc(entry['start'])
    end = utils.parse_utc(entry['end'])
    duration = (end - start).total_seconds()
    tags, projects, uuid = [], [], ''
    for tag in entry['tags']:
        if tag == 'ks' or tag.startswith('ks.'):
            projects.append(tag)
        elif utils.is_uuid(tag):
            uuid = tag
        elif tag in TAGS:
            tags.append(TAGS[tag])
    for project in sorted(projects, reverse=True):
        project = project[3:]
        if project in settings.TIMESHEET_MAP:
            project = settings.TIMESHEET_MAP[project]
            break
    else:
        project = None
    group = groups.setdefault(project, [0.0, {}, {}])
    group[0] += duration
    group[1][uuid] = group[1].get(uuid, 0.0) + duration
    for tag in tags:
        group[2][tag] = group[2].get(tag, 0.0) + duration / len(tags)

# Get related tasks
for project, group in groups.iteritems():
    group[0] /= 3600
    tasks = json.loads(commands.getoutput(
        'task "( %s )" export' % ' or '.join(
            'uuid:%s' % uuid for uuid in group[1].keys())))
    for task in tasks:
        estimate = (
            utils.parse_duration(task['estimate']).total_seconds()
            if 'estimate' in task
            else 0.0)
        task['estimate'] = round(estimate / 3600.0 / HOUR_UNIT) * HOUR_UNIT
        task['duration'] = round(
            group[1][task['uuid']] / 3600.0 / HOUR_UNIT) * HOUR_UNIT
    group[1] = tasks

# Render
n, r = len(groups), 0.0
for i, (project, (hour, tasks, tags)) in enumerate(sorted(
        groups.items(), key=lambda item: item[1][0])):
    h = hour + r / (n - i)
    hour, r = round(h / HOUR_UNIT) * HOUR_UNIT, r + hour
    r -= hour
    groups[project] = (
        hour,
        template.render(
            tasks=tasks, tags=tags, total=h * 3600).encode('utf8'))

# Upload

if not groups:
    print('Empty Timesheet')
elif configs['confirmation'] == 'off':
    timesheet = timesheet()
    if not timesheet.get(day).get('data'):
        for project, (hour, content) in groups.iteritems():
            timesheet.put(day, project, hour, content)
    print(dumps(timesheet.get(day)))
else:
    timesheet = timesheet()
    print('\n\n'.join(
        '%s [%s]%s' % (
            timesheet.projects[project]['projectName'].encode('utf8')
            if project in timesheet.projects else None,
            hour,
            content)
        for project, (hour, content) in groups.iteritems()))
