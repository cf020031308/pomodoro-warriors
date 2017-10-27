import re
import os
import sys
import json
import time
import datetime


basedir = os.path.realpath(__file__)
for i in range(3):
    basedir = os.path.dirname(basedir)
if basedir not in sys.path:
    sys.path.append(basedir)
import settings


DURATION_PATTERN = re.compile(
    r'^P(\d+Y)?(\d+M)?(\d+D)?(?:T(\d+H)?(\d+M)?(\d+S)?)?$')


def parse_duration(duration):
    ds = DURATION_PATTERN.findall(duration)[0]
    assert ds, 'not a duration compliant with ISO-8601: %s' % duration
    y, m, d, H, M, S = [int(d[:-1]) if d else 0 for d in ds]
    s = (((y * 365 + m * 30 + d) * 24 + H) * 60 + M) * 60 + S
    return datetime.timedelta(seconds=s)


def parse_utc(utcdate):
    return (
        datetime.datetime.strptime(utcdate, '%Y%m%dT%H%M%SZ') -
        datetime.timedelta(seconds=time.timezone))


def utc2tz(utcdate):
    return parse_utc(utcdate).strftime('%Y-%m-%dT%H:%M:%S')


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


def is_uuid(s):
    '269795eb-57a4-46d0-b636-4d2ff5ad5c49'
    return len(s) == 36 and s.count('-') == 4
