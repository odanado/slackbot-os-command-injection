#!/bin/sh
echo -e "DEBUG: False\n\nSLACK_TOKEN: $SLACK_TOKEN" > rtmbot.conf
./rtmbot.py > out.log 2> err.log
