import sys
import time
import json
import datetime
import itertools

import utils
from settings import DAILY_FILTER, PROJECTS2TIMESHEET_IDS
from timesheet import TimeSheet


def daily_report(date=None, scale_to=0):
    date = (
        datetime.datetime.strptime(date, '%Y%m%d') if date
        else datetime.date.today())
    starttime = int(time.mktime(date.timetuple()))
    tasks = utils.get_modified_tasks(
        starttime, starttime + 86399, filter=DAILY_FILTER)

    # scale to 8 hours :)
    if scale_to:
        ratio = scale_to * 3600.0 / sum(
            task['active_duration'] for task in tasks)
        if ratio > 1:
            for task in tasks:
                task['active_duration'] *= ratio

    # put to timesheet
    timesheet = TimeSheet()
    for projectId, ts in itertools.groupby(
            tasks,
            key=lambda task: PROJECTS2TIMESHEET_IDS.get(
                task['project'], '')):
        ts = list(ts)
        hours = round(sum(task['active_duration'] for task in ts) / 3600.0, 2)
        content = '\n'.join(task['description'] for task in ts)
        timesheet.put(date, projectId, hours, content)

    # check back
    print json.dumps(
        timesheet.get(date), indent=2, sort_keys=True, ensure_ascii=False)


if __name__ == '__main__':
    daily_report((sys.argv + [None])[1], 8)
