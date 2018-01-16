#!/bin/bash

timew get dom.tracked.1.json | jq '.tags | map(select(length == 36))[0]' | xargs -I{} task uuid:{} info
