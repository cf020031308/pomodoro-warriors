这个分支是我在 ks 工作使用的。请先阅读 master 分支文档。

## jira

配置 `settings.py` 中的 JIRA 为 `https://user:passwd@jira`

`t <id> modify jira:<projectKey> @:JohnSmith` 会在 jira 上创建一个 `<projectKey>-<number>`（如 MYPROJECT-11） 的 issue 并分配给 JohnSmith（默认分配给自己），并加到相应的 sprint 中。

也可以 `t <id> modify jira:<projectKey>-<number>` 配置一个已有 issue。

每次修改会同步至 jira。

## 工时系统

`timew ks_timesheet :day :yes`

需要配置 `settings.py` 中 TIMESHEET 相关。

不带 `:yes` 时只在本地预览。

## 周报

`timew ks_mail :week :yes`

需要配置 `settings.py` 中 MAIL 相关。

不带 `:yes` 时只在本地预览。
