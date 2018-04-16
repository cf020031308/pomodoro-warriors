import os

import yaml


# With configured tag `pomodoro` timewarrior tracks time in Pomodoro Mode.
# Concentrating for 25 minutes achieves a pomodoro.
# Have a break for 5 or 30 minutes every time completing 1 or 4 pomodoro(es).
# An interrupt longer than 2 minutes makes the active pomodoro aborted.
# Reset Pomodoro Combo if a break is longer than 12 minutes.
POMODORO_TAG = 'pomodoro'
POMODORO_DURATION = 1500
POMODORO_SHORT_BREAK = 300
POMODORO_LONG_BREAK = 1500
POMODORO_SET_COUNT = 4
POMODORO_ABORT_GAP = 120
POMODORO_COMBO_GAP = 300

# load settings from settings.yaml, which is ignoed in git
ypath = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'settings.yaml')
if os.path.isfile(ypath):
    with open(ypath) as yfile:
        globals().update(yaml.load(yfile))
