#!/usr/bin/python

import os
import json
import time
import string
import commands
import datetime

import util


Tracked = 'tracked'
StopAt = 'stopat'
DATA = util.get_inputs()


START = 1
STOP = 0
OTHER = -1
utcnow = ''


def stamp(n=0):
    n = n or int(time.time())
    s = string.digits + string.ascii_letters
    r = []
    while n:
        r.append(s[n % 36])
        n /= 36
    return ''.join(reversed(r)) or '000000'


@util.feedback
def _get_command():
    prior = DATA.get('prior', {})
    if 'start' not in prior and 'start' in DATA['task']:
        return START
    if 'start' in prior and 'start' not in DATA['task']:
        return STOP
    if 'start' in DATA['task'] and StopAt in DATA['task']:
        global utcnow
        utcnow = DATA['task'].pop(StopAt)
        DATA.setdefault('prior', {})['start'] = DATA['task'].pop('start')
        return STOP
    return OTHER


COMMAND = _get_command()
DATA['task'].pop(StopAt, None)


@util.feedback
def check_active_tasks():
    if COMMAND != START:
        return
    actives = [
        ('task %s is active: %s' % tuple(id_desc.split(':', 1)))
        for id_desc in commands.getoutput('task +ACTIVE _zshids').splitlines()
    ]
    assert not actives, (
        '\n'.join(actives) +
        'stop %s before start a new one' %
        ('it' if len(actives) == 1 else 'them'))


@util.feedback
def toggle_tmux_status_line():
    if COMMAND == START:
        return os.system(
            'tmux set-option status-bg black && '
            'tmux set-option status-fg black')
    if COMMAND == STOP:
        return os.system(
            'tmux set-option status-bg white && '
            'tmux set-option status-fg black')


@util.feedback
def timew():
    '''
    useage:
        task 1 start
        task 1 stop
    corrections:
        task 1 modify start:2017-01-27T01:46:12
        task 1 modify stopat:2017-01-27T02:29:13
    '''
    task = DATA['task']
    tags = set(task.get('tags') or []).difference([
        'nocolor', 'nonag', 'nocal', 'next'])
    if 'notimew' in tags:
        return

    if COMMAND == STOP:
        cmd = 'stop %s' % utcnow
    elif COMMAND == START and task.get('project'):
        cmd = 'start %s "%s"' % (task['start'], task['project'])
    else:
        return

    return commands.getoutput('timew ' + cmd)


@util.feedback
def backdate():
    task = DATA['task']
    if COMMAND not in (START, STOP):
        return

    output = []
    time_logs = task.get(Tracked, '')
    assert not(len(time_logs) % 6), 'wrong UDA format: %s' % Tracked
    times = [int(time_logs[i:i + 6], 36) for i in range(0, len(time_logs), 6)]
    assert len(times) % 2 != COMMAND, (
        'timestamps in UDA %s are not in pairs' % Tracked)

    if COMMAND == START:
        task[Tracked] = time_logs + stamp(util.utc2time(task['start']))
    else:
        stop_time = util.utc2time(utcnow) if utcnow else int(time.time())
        output.append(
            'tracked duration this time: %s' %
            datetime.timedelta(seconds=stop_time - times[-1]))
        task[Tracked] = time_logs + stamp(stop_time)
        times.append(stop_time)

    output.append(
        'total tracked duration of this task: %s' %
        datetime.timedelta(seconds=sum(
            times[i] - times[i - 1] for i in range(1, len(times), 2))))
    return '\n'.join(output)


check_active_tasks()
toggle_tmux_status_line()
ret = [backdate()]
ret.insert(0, timew())
ret.insert(0, json.dumps(DATA['task']))
print '\n'.join(filter(None, ret))
