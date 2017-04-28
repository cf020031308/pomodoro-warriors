import sys
import time
import json
import datetime
import operator
import itertools

import utils
from settings import DAILY_FILTER, TIMESHEET_MAP
from timesheet import TimeSheet


def daily_report(date=None, scale_to=8, hours_unit=0.25):
    date = (
        datetime.datetime.strptime(date, '%Y%m%d') if date
        else datetime.date.today())
    starttime = int(time.mktime(date.timetuple()))
    tasks = utils.get_modified_tasks(
        starttime, starttime + 86399, filter=DAILY_FILTER)
    timesheet = TimeSheet()

    h = 'active_duration'
    # scale to 8 hours :)
    if scale_to:
        scale_to -= sum(
            task[h] for task in tasks
            if task['project'] not in TIMESHEET_MAP)
        ratio = scale_to * 3600.0 / sum(
            task[h] for task in tasks
            if task['project'] in TIMESHEET_MAP)
        if ratio > 1:
            for task in tasks:
                if task['project'] in TIMESHEET_MAP:
                    task[h] *= ratio

    # put to timesheet
    logs = []
    for project, ts in itertools.groupby(
            tasks,
            key=lambda task: TIMESHEET_MAP.get(
                task['project'], task['project'])):
        ts = list(ts)
        logs.append((
            project,
            sum(task[h] for task in ts) / 3600.0,
            '\n'.join(task['description'] for task in ts)))

    n, remainder = len(logs), 0.0
    for i, (project, hours, content) in enumerate(
            sorted(logs, key=operator.itemgetter(1))):
        # round to 0.25
        _hours = round((hours + remainder / (n - i)) / hours_unit) * hours_unit
        remainder += (hours - _hours)
        if _hours:
            timesheet.put(date, project, _hours, content)

    # check back
    print json.dumps(
        timesheet.get(date), indent=2, sort_keys=True, ensure_ascii=False)


if __name__ == '__main__':
    daily_report((sys.argv + [None])[1], 8)
