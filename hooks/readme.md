## the triggered hooks and inputs/outputs when adding/modifying task(s)

```
# [1] task task1,task2 modify ...
# [2] task add task3
# [3] task next
# 
#                                +---------------------+
#                                |       on-add        |
#                                | [stdin]             |
#                                | added task3 json    |
#                                | [stdout]            |
#                                | added task3 json    |
#                                | feedback text       | ---------+
#                                +---------------------+          |
#                                  ^                              |
#                                  | [2]                          |
#                                  |                              |
# +---------------------+        +---------------------+          |
# |      on-modify      |        |                     |          |
# | [stdin]             |        |                     |          |
# | original task2 json |        |      on-launch      |          |
# | modified task2 json |        | [stdout]            |          |
# | [stdout]            |        | feedback text       |          |
# | modified task2 json |  [1]   |                     |          |
# | feedback text       | <----- |                     | -+       |
# +---------------------+        +---------------------+  |       |
#   |                              |                      |       |
#   |                              | [1]                  |       |
#   |                              v                      |       |
#   |                            +---------------------+  |       |
#   |                            |      on-modify      |  |       |
#   |                            | [stdin]             |  |       |
#   |                            | original task1 json |  |       |
#   |                            | modified task1 json |  |       |
#   |                            | [stdout]            |  |       |
#   |                            | modified task1 json |  |       |
#   |                            | feedback text       |  |       |
#   |                            +---------------------+  |       |
#   |                              |                      |       |
#   |                              | [1]                  | [3]   | [2]
#   |                              v                      v       v
#   |                            +-------------------------------------+
#   |                            |               on-exit               |
#   |                     [1]    | [stdout]                            |
#   +--------------------------> | feedback text                       |
#                                +-------------------------------------+
```
