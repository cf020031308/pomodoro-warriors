#!/bin/bash


timew get dom.tracked.1.json | python -c "
import json
import sys
for tag in json.load(sys.stdin)['tags']:
    if len(tag) == 36 and tag.count('-') == 4:
        print(tag)
        break
" | xargs -I{} task uuid:{} info
