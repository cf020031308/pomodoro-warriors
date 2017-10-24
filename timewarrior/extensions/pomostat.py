#!/usr/bin/python

import os
import sys
import json
import datetime


basedir = os.path.realpath(__file__)
for i in range(3):
    basedir = os.path.dirname(basedir)
if basedir not in sys.path:
    sys.path.append(basedir)


import settings


def format_inputs():
    configs = {}
    while 1:
        line = sys.stdin.readline()
        if line == '\n':
            break
        ks, v = line.split(':', 1)
        c, ks = configs, ks.strip().split('.')
        for k in ks[:-1]:
            c = c.setdefault(k, {})
        c[ks[-1]] = v.strip()
    return configs, json.load(sys.stdin)


def format_date(s):
    return datetime.datetime.strptime(s, '%Y%m%dT%H%M%SZ')


def stat():
    ret = {
        'status': 'INACTIVE',  # ACTIVE|BURST|INACTIVE|BREAK
        'rest': 0.0,           # Available in BREAK
        'seconds': 0.0,        # Total tracking seconds in Pomodoro Mode
        'interrupt': 0,        # Times of interruptions
        'aborted': 0,          # The count of aborted pomodoroes
        'achieved': 0,         # The count of achieved pomodoroes
        'combo': 0,            # The count of archieved pomodoroes in combo
        'max_combo': 0         #
    }
    end = datetime.datetime.fromtimestamp(0)
    now = datetime.datetime.utcnow()
    seconds = 0.0
    for tracked in format_inputs()[1]:
        if settings.POMODORO_TAG not in tracked['tags']:
            continue

        start = format_date(tracked['start'])
        if (start - end).total_seconds() > settings.POMODORO_ABORT * 60:
            ret['aborted'] += 1
            ret['seconds'] += seconds
            seconds = 0.0
        end = format_date(tracked.get('end', now))
        seconds += (end - start).total_seconds()

        if 'end' not in tracked:
            ret['status'] = (
                'BURST' if seconds > settings.POMODORO_INTERVAL * 60
                else 'ACTIVE')
            ret['seconds'] += seconds
            return ret

        ret['status'] = 'INACTIVE'

        if seconds < settings.POMODORO_INTERVAL * 60:
            ret['interrupt'] += 1
            continue

        ret['seconds'] += seconds
        seconds = 0.0
        ret['achieved'] += 1
        ret['combo'] += 1

        elapsed = (now - end).total_seconds()
        rest = (
            (
                settings.POMODORO_SHORT_BREAK
                if ret['combo'] < settings.POMODORO_BURST
                else settings.POMODORO_LONG_BREAK) * 60 - elapsed)
        if rest > 0:
            ret['status'] = 'BREAK'
            ret['rest'] = rest

        if elapsed > settings.POMODORO_COMBO * 60:
            ret['max_combo'] = max(ret['max_combo'], ret['combo'])
            ret['combo'] = 0

    return ret


def main():
    print json.dumps(stat(), indent=2, sort_keys=True)


main()
