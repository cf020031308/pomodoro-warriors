import sys
import time
import datetime

import jinja2

import utils
from settings import TIMESHEET_PROJECTS
from timesheet import TimeSheet


ts = TimeSheet()


def daily_report(date=None, scale_to=0):
    date = (
        datetime.datetime.strptime(date, '%Y%m%d') if date
        else datetime.date.today())
    starttime = int(time.mktime(date.timetuple()))
    tasks = utils.get_modified_tasks(
        starttime, starttime + 86399, filter='+work')
    if scale_to:
        ratio = scale_to * 3600.0 / sum(
            task['active_duration'] for task in tasks)
        if ratio > 1:
            for task in tasks:
                task['active_duration'] *= ratio
    print jinja2.Template('''
{%- macro to_hour(time) %}
{%- if time > 0 %} [{{ (time / 3600.0) | round(precision=2) }}h]{% endif %}
{%- endmacro %}

{%- for project, ts in tasks | groupby(attribute='project') %}
  {{ project }}{{ to_hour(ts | sum(attribute='active_duration')) }}
  {%- if (ts | length) == 1 %}
    {{ ts[0].description }}
  {%- else %}
    {%- for task in ts %}
    {{ loop.index }}. {{ task.description }}{{ to_hour(task.active_duration) }}
    {%- endfor %}
  {%- endif -%}
{% endfor %}''').render({'tasks': tasks})
    projects = {}
    for task in tasks:
        project = projects.setdefault(
            TIMESHEET_PROJECTS.get(task['project'], ''),
            [0, []])
        project[0] += task['active_duration']
        project[1].append(task['description'])

    for project, (duration, contents) in projects.iteritems():
        ts.put(
            date,
            project,
            int(0.5 + duration / 36.0) / 100.0,
            '\n'.join(contents).encode('utf8'))


if __name__ == '__main__':
    print daily_report((sys.argv + [None])[1], 8)
