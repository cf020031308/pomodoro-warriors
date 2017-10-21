Fight a loosing battle against endless bullets.

## About

Here's the best practice of my [taskwarrior](https://taskwarrior.org/docs/).

All the effort is made to suit my own work as a programmer, but with as fewer as possible features in addition to the builtin ones.

## Requirements

* [taskwarrior](https://taskwarrior.org/docs/)
* [timewarrior](https://taskwarrior.org/docs/timewarrior/)
* [tmux](https://github.com/tmux/tmux)

## Features

* [x] `task <filter> last`. Display tasks in modified order from latest on.
* [x] `task continue <duration>`. A shortcut to start the last modified task.
* [x] `task <filter>` or `task <filter> tiny`. Display tasks in tiny spaces of panes in tmux.
* [x] Notify the urgest due task in the status bar of tmux.
* [x] `task <id> split <desc>`. Add a blocking task with inherited project from the task and given description.
* [ ] `task <id> start <duration>`. Track the time in timewarrior with tags and seperated projects as tags. In tmux it hides the tmux status bar to help to concentrate until stop tracking. With given `<duration>` such as `25min` for `<duration>` it automatically stops tracking after `<duration>` and output the total achieved units of pomodoro that day.
* [ ] `task <id> stop <date>`. Stop tracking the task.
* [ ] A python script to generate structured tasks with spent time.

## Workflow

Mainly it's the combination of GTD Theory and Pomodoro Technology.

### Collect

[x] `task add <desc>`

### Process

1. [x] Get stuff with `task -PROJECT` and process the pieces one by one.
2. [x] Put the measurable goals in annotation (or description if it's short) and set project, priority, scheduled, due, etc with `task <id> modify ...`.
3. [x] Split the task into detailed subtasks with `task <id> split <desc>`. The more actionable the subtasks are the better.
4. [ ] Estimate the amount of pomodoro units every subtask needs. If any one costs more than 8, keep splitting it.

### Arrange

[x] Every day at the beginning of working, select scheduled tasks which cost no more than 8 pomodoro units in total as must-be-done tasks with `task <id> modify due:eod`.

### Do

* [x] Activate the doing task with `task <id> start` or `task <id> start <duration>`.
* [x] Tag the interrupting emergency task with `task <id> modify +next`.

### Review

[ ] `python tasksheet.py`
