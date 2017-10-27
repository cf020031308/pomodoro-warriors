# Power-warriors

## About

Power-warriors is the integration of [taskwarrior](https://taskwarrior.org/docs/), [timewarrior](https://taskwarrior.org/docs/timewarrior/), and [powerline](https://github.com/powerline/powerline) which helps you to split tasks into pomodoros and squash them into ketchup.

## Status

This repo is in rapid development and it's not stable. So do not use.

## Features

* [x] `task <filter>` or `task <filter> tiny`. Display tasks in tiny spaces like panes in tmux.
* [x] `task <id> split <mods>`. Add a sub-task which blocks the given task.
* [x] `task <id> timew ...`. A shortcut to execute `timew ... <task tags, projects, uuid>`.
* [x] Tracking with tag `pomodoro` results in Pomodoro Mode.
* [x] `task <id> pomodoro <annotation>`. A shortcut to annotate a task and start a pomodoro.
* [x] Notify the urgest due task.
* [x] Notify when status changed when in Pomodoro Mode.
* [x] Show the total pomodoros of the day and the combo.
* [ ] A UDA to store an estimate for the costing duration.
* [ ] When a task is done, output the estimate time and actual cost.
* [ ] A review script to generate structured tasks with spent time.

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

You can also get your stat data by `timew pomostat [<interval>] [<tag> ...]`

## Workflow

Mainly it's the combination of the GTD Theory and the Pomodoro Technology.

### Collect

* [x] `task add <desc>`

### Process

1. [x] Get stuff with `task -PROJECT` and process the pieces one by one.
2. [x] Put the measurable goals in annotation (or description if it's short) and set project, priority, scheduled, due, etc with `task <id> modify ...`.
3. [x] Split the task into detailed subtasks with `task <id> split <mods>`. The more actionable the subtasks are the better.
4. [ ] Estimate the number of pomodoros every subtask needs. If any one costs more than 8, keep splitting it.

### Arrange

* Every day at the beginning of working, select ready tasks which cost no more than 8 pomodoros in total as must-be-done tasks with `task <id> start`.

### Do

* Tracking the doing task. `task <id> pomodoro <annotation>`
* Tag the interrupting emergency task with `task <id> modify +next`.
* Being interrupted for more than two minutes, execute `timew stop`.

### Review

* [ ] `python tasksheet.py`
