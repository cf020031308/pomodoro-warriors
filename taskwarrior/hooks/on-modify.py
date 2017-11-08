#!/usr/bin/python

import json
import commands

import utils


def main():
    inputs = utils.format_inputs()
    task = inputs['task']
    ret = [json.dumps(task)]
    if 'end' in task and 'end' not in inputs['prior']:
        if 'estimate' in task:
            ret.append(
                'Estimate Duration: %s' %
                utils.parse_duration(task['estimate']))
        ret.append(
            'Total Duration: %s' % commands.getoutput(
                'timew duration "%(uuid)s" from %(entry)s to %(end)s' % task))
    if len(ret) == 1:
        ret.append('')
    print '\n'.join(ret)


main()
