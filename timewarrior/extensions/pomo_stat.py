#!/usr/local/bin/python

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

    seconds, end, now = 0.0, None, datetime.datetime.now()
    for entry in entries + [{}]:
        start = utils.parse_utc(entry['start']) if 'start' in entry else now
        gap = (start - end).total_seconds() if end else 0.0
        if start == end:
            ret['seconds'] += seconds
            if seconds < settings.POMODORO_DURATION:
                ret['status'] = 'ACTIVE'
            else:
                ret['status'] = 'COMPLETE'
                ret['combo'] += 1
                ret['achieved'] += 1
                if ret['max_combo'] < ret['combo']:
                    ret['max_combo'] = ret['combo']
            seconds = 0.0
        elif seconds < settings.POMODORO_DURATION:
            ret['interrupt'] += 1
            if gap < settings.POMODORO_ABORT_GAP:
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
                settings.POMODORO_SHORT_BREAK
                if ret['combo'] % settings.POMODORO_SET_COUNT
                else settings.POMODORO_LONG_BREAK))
            if (start - break2).total_seconds() >= settings.POMODORO_COMBO_GAP:
                ret['combo'] = 0
                ret['status'] = 'INACTIVE'
            else:
                ret['status'] = break2.strftime('BREAK TO %H:%M')
        end = utils.parse_utc(entry['end']) if 'end' in entry else now
        seconds += (end - start).total_seconds()
    else:
        ret['seconds'] += seconds

    for tag in entries[-1]['tags']:
        if utils.is_uuid(tag):
            ret['desc'] = commands.getoutput('task _get %s.description' % tag)
            break

    return ret


if __name__ == '__main__':
    print(json.dumps(stat(), indent=2, sort_keys=True))
