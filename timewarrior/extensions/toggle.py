#!/usr/local/bin/python

import os
import json
import commands

import utils


tracked = json.loads(commands.getoutput('timew get dom.tracked.1.json'))
if 'end' in tracked:
    print 'There is no active time tracking.'
    exit()

tags = tracked['tags']
for tag in utils.format_inputs()[0]['temp']['report']['tags']:
    while tag[0] == tag[-1] and tag[0] in '\'"':
        tag = tag[1:-1]
    (tags.remove if tag in tags else tags.append)(tag)

os.system('timew start %s' % ' '.join('"%s"' % tag for tag in tags))
