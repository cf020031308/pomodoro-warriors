# Pomodoro-warriors

## About

Pomodoro-warriors is the integration of [taskwarrior](https://taskwarrior.org/docs/) and [timewarrior](https://taskwarrior.org/docs/timewarrior/) which helps you to:

1. Split tasks into smaller ones;
2. Track tasks conveniently;
3. Doing in Pomodoro Mode;
4. Review and report in various ways.

## Status

This repo is in debugging.

## Features

* [x] `task <filter>` or `task <filter> tiny`. Display tasks in tiny spaces like panes in tmux.
* [x] `task <id> split <mods>`. Add a sub-task which blocks the given task.
* [x] `task <id> timew ...`. A shortcut to execute `timew ... <task tags, projects, uuid>`.
* [x] Tracking with tag `pomodoro` results in Pomodoro Mode.
* [x] `task <id> pomodoro <annotation>`. A shortcut to annotate a task and start a pomodoro.
* [x] Notify the urgest due task.
* [x] Notify the status changing when in Pomodoro Mode.
* [x] Pomodoro Report with the total count of the day and the combo.
* [x] A UDA to store an estimate for the costing duration.
* [x] When a task is done, output the estimate time and actual duration.
* [x] Timesheet Report Example.
* [x] Mail Report Example.
* [x] A script `scripts/recover.py` to recover data.

## Usage

### task <id> split <mods>

Add a new task with `task add <mods>` which blocks the task with given id.

If a project name is given to the new task. The project name of the parent task is prepended to it to make it in hierarchy.  
Else, the project name of the new task is simply inherited from the parent task.

For example.

```bash
>>> task add project:test "I'm a parent task"
Created task 1.
>>> task 1 split +next "I'm a child task"
Created task 2.
>>> task 1 split project:sub "I'm another child task"
Created task 3.
>>> task _get 1.depends
b4eb87e6-54f5-422e-939a-f03c673de23e,8dd2e258-525f-4ff0-a7dc-b80fbca8387c
>>> task _get {2,3}.project
test test.sub
```

Therefor, a task with no project cannot be splitted.

### task <id> timew ...

This is a shortcut to execute `timew ... <task tags, projects, uuid>`. It makes the tracking and reporting of tasks much more convenient by simple commands like `task 1 timew start`.

### Pomodoro Mode

Tracking with a special tag `pomodoro` can tell the timewarrior that you are in Pomodoro Mode. With a notifier you can get notified as the Pomodoro Technology requires.

So you can get into Pomodoro Mode when tracking a specific task in two ways:

1. Tag in timewarrior directly and temporarily, `task <id> timew start pomodoro`.
2. Tag the task first, `task <id> modify +pomodoro`, then `task <id> timew start`.

And a shortcut is made for this: `task <id> pomodoro <annotation>`. It annotates the task and activates Pomodoro Mode.

You can also get your stat data by `timew pomos [<interval>] [<tag> ...]`

### Integrate with tmux or powerline

- [tmux](https://github.com/tmux/tmux)
- [powerline](https://github.com/powerline/powerline)

See `scripts/message.py`.

## Example Workflow

Mainly it's the combination of the GTD Theory and the Pomodoro Technology.

### Collect

* `task add <desc>`

### Process

1. Get stuff with `task -PROJECT` and process the pieces one by one.
2. Put the measurable goals in annotation (or description if it's short) and set project, priority, scheduled, due, etc with `task <id> modify ...`.
3. Split the task into detailed subtasks with `task <id> split <mods>`. The more actionable the subtasks are the better.
4. Estimate the number of pomodoros every subtask needs. If any one costs more than 8, keep splitting it. Else, mark it with `task <id> modify estimate:<duration>`.

### Arrange

* Every day at the beginning of working, run `timew start ks` to track my working time. (ks stands for Knownsec, I'm working for it. See timew reports to get details.)
* Select ready tasks which cost no more than 8 pomodoros in total as must-be-done tasks with `task <id> start`.
* If any task your do not want to do at the day and it it active, deactivate it with `task <id> stop`.

### Do

* Tracking the doing task. `task <id> timew start` or `task <id> pomodoro <annotation>`.
* Tag the interrupting emergency task with `task <id> modify +next`.
* Stop with `timew stop` or `timew stop pomodoro`.

### Review

* Daily: `timew day` and `timew ks_timesheet :day ks`.
* Weekly: `timew week` and `timew ks_mail :week ks`.
