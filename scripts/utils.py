import json
import time
import datetime
import commands


UDA_TRACKED = 'tracked'


def utc2time(date):
    return int(
        time.mktime(
            datetime.datetime.strptime(date, '%Y%m%dT%H%M%SZ').timetuple()) -
        time.timezone)


def get_modified_tasks(starttime, endtime=0, filter=''):
    endtime = endtime or int(time.time())
    output = commands.getoutput(
        'task %s "( +COMPLETED or +PENDING )" modified.after:%s export' % (
            filter,
            datetime.datetime.fromtimestamp(starttime).strftime(
                '%Y-%m-%dT%H:%M:%S')))
    tasks = []
    for task in json.loads(output):
        tracked = task.get(UDA_TRACKED, '')
        assert not(len(tracked) % 6), 'wrong UDA format: %s' % str(task)
        tics = [
            min(max(int(tracked[i:i + 6], 36), starttime), endtime)
            for i in range(0, len(tracked), 6)]
        if len(tics) % 2:
            tics.append(endtime)
        itics = iter(tics)
        task[UDA_TRACKED] = [
            (tic, tac) for tic, tac in zip(itics, itics) if tic < tac]
        if not task[UDA_TRACKED]:
            if task['status'] == 'pending':
                continue
            if utc2time(task['modified']) > endtime:
                continue
        task['active_duration'] = sum((y - x) for x, y in task[UDA_TRACKED])
        tasks.append(task)
    return tasks
