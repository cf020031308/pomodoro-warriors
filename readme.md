Fight a loosing battle against endless bullets.

## About

Here's the best practice of my [taskwarrior](https://taskwarrior.org/docs/).

All the effort is made to suit my own work as a programmer, but with as fewer as possible features in addition to the builtin ones.

## Requirements

* [taskwarrior](https://taskwarrior.org/docs/)
* [timewarrior](https://taskwarrior.org/docs/timewarrior/)

## Features

* [x] `task <filter>` or `task <filter> tiny`. Display tasks in tiny spaces like panes in tmux.
* [x] `task <id> split <mods>`. Add a sub-task which blocks the given task.
* [x] `task <id> timew ...`. A shortcut to execute `timew ... <task tags, projects, description>`.
* [x] Tracking with tag `pomodoro` results in Pomodoro Mode.
* [x] `task <id> pomodoro <annotation>`. A shortcut to annotate a task and start a pomodoro.
* [x] Notify the urgest due task.
* [x] Notify when status changed when in Pomodoro Mode.
* [x] Show the total pomodoroes of the day and the combo.
* [ ] A UDA to store an estimate for the costing pomodoroes.
* [ ] A review script to generate structured tasks with spent time.

## Workflow

Mainly it's the combination of GTD Theory and Pomodoro Technology.

### Collect

* [x] `task add <desc>`

### Process

1. [x] Get stuff with `task -PROJECT` and process the pieces one by one.
2. [x] Put the measurable goals in annotation (or description if it's short) and set project, priority, scheduled, due, etc with `task <id> modify ...`.
3. [x] Split the task into detailed subtasks with `task <id> split <mods>`. The more actionable the subtasks are the better.
4. [ ] Estimate the number of pomodoroes every subtask needs. If any one costs more than 8, keep splitting it.

### Arrange

* [x] Every day at the beginning of working, select scheduled tasks which cost no more than 8 pomodoroes in total as must-be-done tasks with `task <id> modify due:eod`.

### Do

* [x] Activate the doing task with `task <id> timew start`.
* [x] Tag the interrupting emergency task with `task <id> modify +next`.
* [x] Being interrupted for more than two minutes, execute `timew stop`.

### Review

* [ ] `python tasksheet.py`
