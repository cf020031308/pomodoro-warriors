#!/usr/bin/python

from pomo_stat import stat


pomos = stat()
print '[POMO] ' + {
    'ACTIVE': 'Active: %(desc)s',
    'INTERRUPT': 'Interrupt: %(desc)s',
    'COMPLETE': 'Complete. Achieved: %(achieved)d, Combo: %(combo)d',
    'INACTIVE': 'Inactive. Achieved: %(achieved)d, MaxCombo: %(max_combo)d',
}.get(pomos['status'], '%(status)s') % pomos
