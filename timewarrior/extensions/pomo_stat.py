#!/usr/bin/python

'''
ACTIVE: <description>
INACTIVE: <description>
INACTIVE
COMPLETE
BREAK TO <time>
'''

import json
import datetime
import commands

import utils
from utils import settings


def stat():
    _, entries = utils.format_inputs()
    entries = [
        entry for entry in entries if settings.POMODORO_TAG in entry['tags']]
    ret = {
        'status': 'INACTIVE',  # ACTIVE|INTERRUPT|COMPLETE|INACTIVE|BREAK
        'desc': '',            # Description of last tracked task
        'seconds': 0.0,        # Total tracking seconds in Pomodoro Mode
        'interrupt': 0,        # Times of interruptions
        'aborted': 0,          # The count of aborted pomodoroes
        'achieved': 0,         # The count of achieved pomodoroes
        'combo': 0,            # The count of archieved pomodoroes in combo
        'max_combo': 0         #
    }
    if not entries:
        return ret

    ABORT = settings.POMODORO_ABORT * 60
    COMBO = settings.POMODORO_COMBO * 60
    INTV = settings.POMODORO_INTERVAL * 60
    S_BREAK = settings.POMODORO_SHORT_BREAK * 60
    L_BREAK = settings.POMODORO_LONG_BREAK * 60

    seconds, end, now = 0.0, None, datetime.datetime.now()
    for entry in entries + [{}]:
        start = utils.parse_utc(entry['start']) if 'start' in entry else now
        gap = (start - end).total_seconds() if end else 0.0
        if gap == 0.0:
            ret['seconds'] += seconds
            if seconds < INTV:
                ret['status'] = 'ACTIVE'
            else:
                ret['status'] = 'COMPLETE'
                ret['combo'] += 1
                ret['achieved'] += 1
                if ret['max_combo'] < ret['combo']:
                    ret['max_combo'] = ret['combo']
            seconds = 0.0
        elif seconds < INTV:
            ret['interrupt'] += 1
            if gap < ABORT:
                ret['status'] = 'INTERRUPT'
            else:
                ret['status'] = 'INACTIVE'
                ret['aborted'] += 1
                ret['combo'] = 0
                ret['seconds'] += seconds
                seconds = 0
        else:
            ret['seconds'] += seconds
            ret['combo'] += 1
            ret['achieved'] += 1
            if ret['max_combo'] < ret['combo']:
                ret['max_combo'] = ret['combo']
            seconds = 0.0
            break2 = end + datetime.timedelta(seconds=(
                S_BREAK if ret['combo'] < settings.POMODORO_BURST
                else L_BREAK))
            if (start - break2).total_seconds() >= COMBO:
                ret['combo'] = 0
                ret['status'] = 'INACTIVE'
            else:
                ret['status'] = break2.strftime('BREAK TO %H:%M')
        end = utils.parse_utc(entry['end']) if 'end' in entry else now
        seconds += (end - start).total_seconds()
    else:
        ret['seconds'] += seconds

    entry = entries[-1]
    for tag in entry['tags']:
        if not utils.is_uuid(tag):
            continue
        task = json.loads(
            commands.getoutput('task uuid:%s export' % tag))
        task = task[0] if task else {}
        for desc in reversed(task.get('annotations', [])):
            desc = desc['description']
            if desc.startswith('Pomodoro: '):
                ret['desc'] = desc[len('Pomodoro: '):]
                break
        else:
            ret['desc'] = task['description']

    return ret


if __name__ == '__main__':
    print json.dumps(stat(), indent=2, sort_keys=True)
