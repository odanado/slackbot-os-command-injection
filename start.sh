#!/bin/sh

set -eu

echo "DEBUG: False" > rtmbot.conf
echo "SLACK_TOKEN: $SLACK_TOKEN" >> rtmbot.conf
echo "LOGFILE: logs/rtmbot.log" >> rtmbot.conf
rtmbot
