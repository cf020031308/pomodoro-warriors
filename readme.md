# Pomodoro-warriors

## About

Pomodoro-warriors is the integration of [taskwarrior](https://taskwarrior.org/docs/) and [timewarrior](https://taskwarrior.org/docs/timewarrior/) which helps you to:

* Split tasks into smaller ones.
* Track the time spent on every task.
* Do in Pomodoro Mode.
* Review and report in various ways.

## Features

* [x] `task <filter>` or `task <filter> tiny`. Display tasks in tiny spaces like panes in tmux.
* [x] `task <id> split <mods>`. Add a sub-task which blocks the given task.
* [x] `task <id> timew ...`. A shortcut to execute `timew ... <task tags, projects, uuid>`.
* [x] Tracking with tag `pomodoro` results in Pomodoro Mode.
* [x] `task <id> pomodoro <annotation>`. A shortcut to annotate a task and start a pomodoro.
* [x] Notify the status changing when in Pomodoro Mode.
* [x] Pomodoro Report with the total count of the day and the combo.
* [x] A UDA to store an estimate for the costing duration.
* [x] When a task is done, output the estimate time and actual duration.
* [x] Timesheet Report Example.
* [x] Mail Report Example.
* [x] A script `scripts/recover.py` to recover data.
* [x] A cloud-storage cooperative script `bootstrap.sh`.

## Usage

### Prerequisite

Since pomodoro-warriors is the integration of [taskwarrior](https://taskwarrior.org/docs/) and [timewarrior](https://taskwarrior.org/docs/timewarrior/), the following usage goes with the hypothesis that the readers are skilled at both of them.

### `task <id> split <mods>`

Add a new task (child) with `<mods>` which blocks the former one (parent).

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

### `task <id> timew ...`

This is a shortcut to execute `timew ... <task tags, projects, uuid>`.   
It makes the tracking and reporting of tasks much more convenient.

E.g. `task 1 timew start`.

### Pomodoro Mode

Tracking with a special tag `pomodoro` tells timewarrior that you are in Pomodoro Mode.

So you can get into Pomodoro Mode when tracking a specific task in two ways:

1. Tag with timewarrior directly and temporarily: `task <id> timew start pomodoro`.
2. Tag the task first: `task <id> modify +pomodoro`. Then start tracking: `task <id> timew start`.

And a shortcut is made for this: `task <id> pomodoro <annotation>`.  
It annotates the task and activates Pomodoro Mode.

You can also get your stat data by `timew pomos [<interval>] [<tag> ...]`.

### Integrate with tmux or powerline

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

### Sync data with cloud storage

Take OneDrive as an example.

```bash
./bootstrap.sh ~/OneDrive/task
```

### 关于网盘

对于国内用户，我非常推荐使用[坚果云](https://www.jianguoyun.com)。对比 OneDrive 等大厂产品的优势如下：

* 全平台：我因此几个不同系统的电脑有相同的开发环境和数据。
* 国内网络：速度快，不用翻墙。
* 数据有多个版本供回滚：`taskwarrior` 有时候数据会出问题，我因此还写了 `scripts/recover.py`，有了坚果云就用不到了。
* 配置灵活：不需要像 `bootstrap.sh` 里那样把数据放到同步文件夹里，而是配置哪些文件（夹）是要同步的。

## Example Workflow

Mainly it's the combination of the GTD Theory and the Pomodoro Technology.

### Collect

* `task add <desc>`

### Process

1. Get stuff with `task -PROJECT` and process the pieces one by one;
2. Put the measurable goals in annotation (or description if it's short) and set project, priority, scheduled, due, etc with `task <id> modify <mods>`;
3. Split the task into detailed subtasks with `task <id> split <mods>`. The more actionable the subtasks are the better;
4. Estimate the number of pomodoros every subtask would take. If any one is going to cost more than 8, keep splitting it. Else, mark it with `task <id> modify estimate:<duration>`.

### Arrange

* Run `timew start ks` to start a day's work. (ks stands for the company which I'm currently working for.)
* Select ready tasks which cost no more than 8 pomodoros in total as must-be-done-today tasks with `task <id> start`.
* If any task your do not want to do in the day is active, deactivate it with `task <id> stop`.

### Do

* Track the doing task: `task <id> timew start` or `task <id> pomodoro <annotation>`.
* Tag the interrupting emergency task with `task <id> modify +next`.
* Take a rest in Pomodoro Mode with `timew stop pomodoro` or `task <id> timew start` if you want the tracker keeps tracking.
* Stop tracking: `timew stop`.

### Review

* Daily: `timew day` and `timew ks_timesheet :day`.
* Weekly: `timew week` and `timew ks_mail :week`.
