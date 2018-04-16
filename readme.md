# Pomodoro-warriors

[中文文档](./读我.md)

## About

Pomodoro-warriors is the integration of [taskwarrior](https://taskwarrior.org/docs/) and [timewarrior](https://taskwarrior.org/docs/timewarrior/) which helps you to:

* Split tasks into smaller ones.
* Track the time spent on every task.
* Do in Pomodoro Mode.
* Review and report in various ways.

## Installation

### Install to local path

1. Run `./bootstrap.sh`;
2. Install [taskwarrior](https://taskwarrior.org/download/);
3. Install [timewarrior](https://taskwarrior.org/docs/timewarrior/download.html).

### Install with cloud storage services

Take OneDrive as an example and suppose you've already installed both taskwarrior and timewarrior:

```bash
./bootstrap.sh ~/OneDrive/task
```

## Usage

Since pomodoro-warriors is the integration of [taskwarrior](https://taskwarrior.org/docs/) and [timewarrior](https://taskwarrior.org/docs/timewarrior/), the following usages go with the hypothesis that the readers are skilled at both of them.

### 1. `task <id> split <mods>`

Create a new subtask with `<mods>` which blocks the former one.

If a project name is given to the subtask. The project name of the parent task is prepended to it to make it in hierarchy.  
Else, the project name of the subtask is simply inherited from the parent task.

Therefor, a task with no project cannot be splitted.

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

### 2. `task <id> timew ...`

This is a shortcut to execute `timew ... <task tags, projects, uuid>` which makes the tracking and reporting of tasks much more convenient.

E.g. `task <id> timew start`.

### 3. Pomodoro Mode

Tracking with a special tag `pomodoro` tells timewarrior that you are in Pomodoro Mode.

So you can start a Pomodoro when doing a specific task by executing `task <id> timew start pomodoro`.

### 4. Reports

* `timew last`. Show info of current tracking or last tracked task.
* When a task is done or deleted, show it's tracked time.
* `timew pomo_stat`. Export statistics on Pomodoro Mode.
* `timew pomo_msg`. Show current state in Pomodoro Mode. Can be integrated with `tmux` or `powerline`.
* `timew duration`. Output the total duration.

If you are using [tmux](https://github.com/tmux/tmux) you can append the following line to `~/.tmux.conf`:

```bash
set-option -g status-left "#(timew pomo_msg.py :day)"
```

If you are using [powerline](https://github.com/powerline/powerline) you can add this to the segments:

```json
{
    "function": "powerline.lib.shell.run_cmd",
    "priority": 80,
    "args": {
        "cmd": ["timew", "pomo_msg.py", ":day"]
    }
}
```

See branch [ks](https://github.com/cf020031308/pomodoro-warriors/tree/ks) to view my personal reports as examples.

### 5. Other improvements

* `task <filter> tiny`. Display tasks in tiny spaces like panes in tmux.
* A User Defined Attribute `estimate` to store an estimate for the costing duration of a task.
* `timew toggle [<tag> ...]`. Start a new track with tags appended to / removed from the tags of current track.

## Example Workflow

Mainly it's the combination of the GTD Theory and the Pomodoro Technology.

### Collect

* `task add <desc>`

### Process

1. Get stuff with `task -PROJECT` and process the pieces one by one;
2. Put the measurable goals in annotation by `task <id> annotate <anno>` (or description if it's short) and set project, priority, scheduled, due, etc with `task <id> modify <mods>`;
3. Split the task into detailed subtasks with `task <id> split <mods>`. The more actionable the subtasks are the better;
4. Estimate the number of pomodoros every subtask would take. If any one is going to cost more than 8, keep splitting it. Else, record it with `task <id> modify estimate:<duration>`.

### Arrange

* Plan what you want to do at the beginning of a day. Use `task <id> start` or add due dates to make the tasks obvious in your task list.

### Do

* normal way
    + `task <id> timew start`. Start a task and track it.
    + `timew stop`. Stop tracking a task.
    + `task <id> done`. Complete a task and stop tracking it.
* Pomodoro Mode
    + `task <id> timew start pomodoro`. Start a pomodoro on a task.
    + `timew toggle pomodoro` or `timew stop pomodoro`. Stop a pomodoro and keep tracking the task.
    + If something important interrupts, use `task <id> modify +next` to boost its urgency. After the current pomodoro, handle it.
    + With the integration of tmux or powerline, the state of Pomodoro Mode is displayed in the status-line.

### Review

* Daily: `timew day`
* Weekly: `timew week`
