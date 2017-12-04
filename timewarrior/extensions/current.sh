#!/bin/bash

timew get dom.active.json | jq '.tags[0]' | xargs -I{} task uuid:{} info
