#!/usr/bin/python

import json
import datetime

import utils
from utils import settings


def pomos(entries):
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
            ret['status'] = (
                'BURST' if seconds > settings.POMODORO_INTERVAL * 60
                else 'ACTIVE')
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
        if now > break2:
            ret['status'] = break2.strftime('BREAK TO %H:%M:%S')
            if (now - break2).total_seconds() > settings.POMODORO_COMBO * 60:
                ret['max_combo'] = max(ret['max_combo'], ret['combo'])
                ret['combo'] = 0

    return ret


if __name__ == '__main__':
    print json.dumps(pomos(utils.format_inputs()[1]), indent=2, sort_keys=True)
