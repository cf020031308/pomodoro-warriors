#!/usr/bin/python

import json
import datetime
import commands

import utils
from utils import settings


def main():
    _, entries = utils.format_inputs()
    ret = {
        'status': 'INACTIVE',  # ACTIVE|BURST|INACTIVE|BREAK
        'seconds': 0.0,        # Total tracking seconds in Pomodoro Mode
        'interrupt': 0,        # Times of interruptions
        'aborted': 0,          # The count of aborted pomodoroes
        'achieved': 0,         # The count of achieved pomodoroes
        'combo': 0,            # The count of archieved pomodoroes in combo
        'max_combo': 0         #
    }
    seconds, end, now = 0.0, None, datetime.datetime.now()

    for entry in entries:
        if settings.POMODORO_TAG not in entry['tags']:
            continue

        start = utils.parse_utc(entry['start'])
        if 'end' not in entry:
            if seconds > settings.POMODORO_INTERVAL * 60:
                ret['status'] = 'BURST'
            else:
                for tag in entry['tags']:
                    if not utils.is_uuid[tag]:
                        continue
                    task = json.loads(
                        commands.getoutput('task uuid:%s export' % tag))
                    task = task[0] if task else {}
                    desc = (
                        task
                        .get('annotations', [{}])[-1]
                        .get('description', task['description']))
                    ret['status'] = 'ACTIVE: %s' % desc
                    break
                else:
                    ret['status'] = 'ACTIVE'
            ret['seconds'] += seconds + (now - start).total_seconds()
            return ret

        ret['status'] = 'INACTIVE'

        if end and (
                start - end).total_seconds() > settings.POMODORO_ABORT * 60:
            ret['aborted'] += 1
            ret['seconds'] += seconds
            seconds = 0.0

        end = utils.parse_utc(entry['end'])
        seconds += (end - start).total_seconds()

        if seconds < settings.POMODORO_INTERVAL * 60:
            ret['interrupt'] += 1
            continue

        ret['seconds'] += seconds
        seconds = 0.0
        ret['achieved'] += 1
        ret['combo'] += 1

    if end:
        break2 = end + datetime.timedelta(seconds=60 * (
            settings.POMODORO_SHORT_BREAK
            if ret['combo'] < settings.POMODORO_BURST
            else settings.POMODORO_LONG_BREAK))
        if (now - break2).total_seconds() > settings.POMODORO_COMBO * 60:
            ret['max_combo'] = max(ret['max_combo'], ret['combo'])
            ret['combo'] = 0
        else:
            ret['status'] = break2.strftime('BREAK TO %H:%M:%S')

    print json.dumps(ret, indent=2, sort_keys=True)


main()
