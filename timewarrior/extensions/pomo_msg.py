#!/usr/local/bin/python

from pomo_stat import stat


pomos = stat()
content = '[POMO] ' + {
    'ACTIVE': 'Active-%(combo)s: %(desc)s',
    'INTERRUPT': 'Interrupt-%(combo)s: %(desc)s',
    'COMPLETE': 'Complete. Achieved: %(achieved)d, Combo: %(combo)d',
    'INACTIVE': 'Inactive. Achieved: %(achieved)d, MaxCombo: %(max_combo)d',
}.get(pomos['status'], '%(status)s') % pomos
print content.encode('utf8')[:50]
