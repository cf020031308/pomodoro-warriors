#!/usr/bin/python

import datetime

import utils


def main():
    _, entries = utils.format_inputs()
    now = datetime.datetime.now()
    duration = datetime.timedelta()
    for entry in entries:
        start = utils.parse_utc(entry['start'])
        end = utils.parse_utc(entry['end']) if 'end' in entry else now
        duration += (end - start)
    print duration


main()
