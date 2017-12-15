#!/bin/bash

timew get dom.tracked.1.json | jq '.tags[0]' | xargs -I{} task uuid:{} info
