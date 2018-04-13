#!/usr/local/bin/python

import json

import jira
import utils


task = utils.format_inputs()['task']
jret = jira.sync()
ret = [json.dumps(task)]
if jret:
    ret.append(jret)
if len(ret) == 1:
    ret.append('')
print('\n'.join(ret))
