#!/usr/local/bin/python

import os
import sys
import shutil


def mkdir(d):
    try:
        os.makedirs(d)
    except Exception:
        pass


home = os.path.expanduser('~')
taskd = os.path.join(home, '.task')
taskrc = os.path.join(home, '.taskrc')
timed = os.path.join(home, '.timewarrior')
timecfg = os.path.join(timed, 'timewarrior.cfg')

# Keep data in a target folder like cloud-disk
if len(sys.argv) > 1:
    dst = os.path.realpath(sys.argv[1])
    dtaskd = os.path.join(dst, 'taskwarrior')
    dtimed = os.path.join(dst, 'timewarrior')
    map(mkdir, (dtaskd, dtimed))

    # # Migrate existing data of taskwarrior
    if os.path.isdir(taskd):
        for fn in os.listdir(taskd):
            if fn.endswith('.data'):
                shutil.copy(os.path.join(taskd, fn), dtaskd)
    with open(taskrc, 'a') as file:
        file.write('\ndata.location=%s' % dtaskd)

    # # Migrate existing data of timewarrior
    timedd = os.path.join(timed, 'data')
    dtimedd = os.path.join(dtimed, 'data')
    if os.path.isdir(timedd):
        shutil.move(timedd, dtimed)
    else:
        mkdir(dtimedd)
    os.path.isdir(timed) or mkdir(timed)
    os.symlink(dtimedd, timed)

    taskd = dtaskd
    timed = dtimed

map(mkdir, (taskd, timed))

# Install hooks and extensions of Pomodoro-Warriors
base = os.path.dirname(os.path.realpath(sys.argv[0]))
btaskd = os.path.join(base, 'taskwarrior')
btimed = os.path.join(base, 'timewarrior')
btimecfg = os.path.join(btimed, 'timewarrior.cfg')

# # Backup and setup hooks of taskwarrior
hooks = os.path.join(taskd, 'hooks')
os.path.isdir(hooks) and shutil.move(hooks, hooks + '.bak')
os.symlink(os.path.join(btaskd, 'hooks'), hooks)
with open(taskrc, 'a') as file:
    file.write('\ninclude %s/taskrc' % btaskd)

# # Backup and setup extensions of timewarrior
exts = os.path.join(timed, 'extensions')
os.path.isdir(exts) and shutil.move(exts, exts + '.bak')
os.symlink(os.path.join(btimed, 'extensions'), exts)
with open(timecfg, 'a') as file:
    file.write('\n%s' % open(btimecfg).read())
