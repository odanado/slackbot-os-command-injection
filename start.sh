#!/bin/sh

set -eu

cat << EOF > rtmbot.conf
DEBUG: True
SLACK_TOKEN: $SLACK_TOKEN
LOGFILE: logs/rtmbot.log
ACTIVE_PLUGINS:
    - plugins.OSCommandInjection
EOF

rtmbot
