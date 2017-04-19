#!/usr/bin/python

import os
import commands

import util


inputs = util.get_inputs()


@util.feedback
def main():
    if inputs['command'] == 'continue':
        last = commands.getoutput(
            'task last limit:1 2>&- | sed -n "3p"').strip()
        cols = last.split()
        _id, desc = cols[0], ' '.join(cols[1:])
        os.system('task %s start' % int(_id))
        print 'task %s continued: %s' % (_id, desc)


main()
