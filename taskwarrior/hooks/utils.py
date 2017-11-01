#!/usr/bin/python

import re
import os
import sys
import json
import datetime


DURATION_PATTERN = re.compile(
    r'^P(\d+Y)?(\d+M)?(\d+D)?(?:T(\d+H)?(\d+M)?(\d+S)?)?$')


def parse_duration(duration):
    ds = DURATION_PATTERN.findall(duration)[0]
    assert ds, 'not a duration compliant with ISO-8601: %s' % duration
    y, m, d, H, M, S = [int(d[:-1]) if d else 0 for d in ds]
    s = (((y * 365 + m * 30 + d) * 24 + H) * 60 + M) * 60 + S
    return datetime.timedelta(seconds=s)


def format_inputs():
    '''
    // returned inputs example

    {
        "version": "2.5.1",
        "api": "2",
        "rc": "~/.taskrc",
        "data": "~/.task/work",
        "filename": "on-exit_print.py",
        "command": "undo",
        "args": "task undo",
        "prior": {},  // exists only in on-modify scripts
        "task": {}  // exists only in on-add/on-modify scripts
    }
    '''
    inputs = dict(arg.split(':', 1) for arg in sys.argv[1:])
    assert inputs['api'] == '2', 'API: %s is not supported' % inputs['api']

    filename = os.path.split(sys.argv[0])[-1]
    inputs['filename'] = filename

    if filename.startswith('on-add'):
        inputs['task'] = json.load(sys.stdin)
    elif filename.startswith('on-modify'):
        inputs['prior'] = json.loads(sys.stdin.readline())
        inputs['task'] = json.loads(sys.stdin.readline())

    return inputs
