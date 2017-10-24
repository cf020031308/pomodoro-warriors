#!/usr/bin/python

import os
import sys
import json
import commands


RESERVED_TAGS = set('nocolor nonag nocal next'.split())


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


def main():
    inputs = format_inputs()
    args, cmd = inputs['args'], inputs['command']
    if cmd == 'split':
        # task <id> split <mods>
        pre, mods = args.split(cmd, 1)
        _id = int(pre.split()[1])
        mods = (
            (mods + ' ')
            .replace(' project: ', '')
            .replace(' project:', 'project:{}.')
            .strip())
        subid = commands.getoutput(
           r'task _get %s.project | xargs -I{} task add %s | grep -o "\d\+"' %
           (_id, mods))
        if subid:
            print 'Created task %s.' % subid
            os.system('task %s modify depends:%s' % (_id, subid))
        else:
            print 'You can only split a task when it is a project.'
    elif cmd == 'timew':
        # task <id> timew ...
        pre, timew = args.split(cmd, 1)
        _id = int(pre.split()[1])
        tags, proj, desc = commands.getoutput(
            'task _get %s.{tags,project,description}' % _id).split(' ', 2)
        tags = [t for t in tags.split(',') if t not in RESERVED_TAGS]
        while proj:
            tags.append(proj)
            proj = proj.rpartition('.')[0]
        tags.append(desc)
        tags = ' '.join('"%s"' % t for t in tags)
        os.system('timew %s %s' % (timew, tags))
    elif cmd == 'pomodoro':
        # task <id> pomodoro <annotation>
        pre, anno = args.split(cmd, 1)
        if anno.strip():
            _id = int(pre.split()[1])
            os.system(
                'task %(_id)s annotate "Pomodoro:%(anno)s" && '
                'task %(_id)s timew start pomodoro' % locals())
        else:
            os.system('%s timew start pomodoro' % pre)


main()
