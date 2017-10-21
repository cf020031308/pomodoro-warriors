#!/usr/bin/python

import os
import commands

import util


@util.feedback
def main():
    inputs = util.get_inputs()
    cmd = inputs['command']
    if cmd == 'continue':
        # task continue <duration>
        last = commands.getoutput(
            'task last limit:1 2>&- | sed -n "3p"').strip()
        cols = last.split()
        _id, desc = cols[0], ' '.join(cols[1:])
        os.system(inputs['args'].replace(cmd, '%s start' % int(_id), 1))
        print 'Continue task %s: %s' % (_id, desc)
    elif cmd == 'split':
        # task <id> split <desc>
        args = inputs['args'].strip().split()[1:]
        args.remove(inputs['command'])
        if len(args) > 1:
            parent_id = int(args.pop(0))
            child_id = commands.getoutput(
                (
                    r'task _get %s.project | '
                    r'xargs -I{} task add project:{} "%s" | '
                    r'grep -o "\d\+"'
                ) % (parent_id, ' '.join(args))
            )
            if child_id:
                print 'Created task %s.' % child_id
                os.system('task %s modify depends:%s' % (parent_id, child_id))


main()
