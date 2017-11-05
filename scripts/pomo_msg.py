'Append in ~/.tmux.conf: set-option -g status-left "#(python <path/to/this>)"'

import json
import commands


pomos = json.loads(commands.getoutput('timew pomos :day'))
if pomos['status'] == 'BURST':
    print '[POMO] Complete. Achieved: %(achieved)d, Combo: %(combo)d' % pomos
elif pomos['status'] == 'INACTIVE':
    print '[POMO] Achieved: %(achieved)d, MaxCombo: %(max_combo)d' % pomos
else:
    print '[POMO] %(status)s' % pomos
