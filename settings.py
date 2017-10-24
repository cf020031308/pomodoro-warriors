import os
import yaml


# With configured tag `pomodoro` timewarrior tracks time in Pomodoro Mode.
# Concentrating for 25 minutes achieves a pomodoro.
# Have a break for 5 or 30 minutes every time completing 1 or 4 pomodoro(es).
# An interrupt longer than 2 minutes makes the active pomodoro aborted.
# Reset Pomodoro Combo if a break is longer than 12 minutes.
POMODORO_TAG = 'pomodoro'
POMODORO_INTERVAL = 25
POMODORO_SHORT_BREAK = 5
POMODORO_LONG_BREAK = 30
POMODORO_BURST = 4
POMODORO_ABORT = 2
POMODORO_COMBO = 12


# load settings from yaml
ypath = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'settings.yaml')
if os.path.isfile(ypath):
    with open(ypath) as yfile:
        globals().update(yaml.load(yfile))
