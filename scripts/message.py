'Append in ~/.tmux.conf: set-option -g status-left "#(python <path/to/this>)"'

import json
import commands


msgs = []


# Pomodoro
pomos = json.loads(commands.getoutput('timew pomos :day'))
if pomos['status'] == 'BURST':
    msgs.append('POMO: Complete')
elif pomos['status'] == 'INACTIVE':
    msgs.append('POMO: Achieved - %(achieved)d, Combo - %(combo)d' % pomos)
elif pomos['status'] != 'BREAK':
    msgs.append('POMO: %(status)s' % pomos)


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
