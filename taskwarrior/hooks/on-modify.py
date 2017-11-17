#!/usr/local/bin/python

import json
import commands

import utils


def main():
    inputs = utils.format_inputs()
    task = inputs['task']
    ret = [json.dumps(task)]
    if 'end' in task and 'end' not in inputs['prior']:
        timew = json.loads(commands.getoutput('timew get dom.tracked.1.json'))
        cmd = 'timew duration "%(uuid)s" from %(entry)s - %(end)s' % task
        if 'end' not in timew and task['uuid'] in timew['tags']:
            cmd = 'timew stop :quiet && ' + cmd
        if 'estimate' in task:
            ret.append(
                'Estimate Duration: %s' %
                utils.parse_duration(task['estimate']))
        ret.append('Total Duration: %s' % commands.getoutput(cmd))
    if len(ret) == 1:
        ret.append('')
    print('\n'.join(ret))


main()
