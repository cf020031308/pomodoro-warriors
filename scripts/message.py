'Append in ~/.tmux.conf: set-option -g status-left "#(python <path/to/this>)"'

import json
import commands


msgs = []


# Pomodoro
pomo = json.loads(commands.getoutput('timew pomostat'))
if pomo['status'] == 'BURST':
    msgs.append('POMO: Complete')
elif pomo['status'] == 'INACTIVE':
    msgs.append('POMO: Achieved - %(achieved)d, Combo - %(combo)d' % pomo)
elif pomo['status'] == 'BREAK':
    msgs.append('NEXT POMO: %ds' % int(pomo['rest']))


# Due
due = commands.getoutput(
    'task due.before.tomorrow limit:1 2>&- | '
    'sed -n "3p" | '
    'cut -d" " -f 1 |'
    'xargs -I{} "task _get {}.{due,description,id}"'
)
if due:
    msgs.append('DUE: %s [%s]' % tuple(due.rsplit(' ', 1)))


print ' | '.join(msgs)
