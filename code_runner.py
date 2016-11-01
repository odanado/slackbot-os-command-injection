import os
from html import unescape

from constant import Command
from docker import Docker


def _write_workspace(filename, source):
    os.system('rm -rf /tmp/workspace')
    os.system('mkdir /tmp/workspace')
    os.system('chmod 777 /tmp/workspace')
    with open('/tmp/workspace/{}'.format(filename), 'w') as f:
        f.write(source)


def code_runner(lang, source):
    docker = Docker(lang)
    source = unescape(source)
    _write_workspace(Command[lang]['filename'], source)
    docker.create()
    docker.copy()
    stdout, stderr, time = docker.start()
    docker.remove()

    return stdout, stderr, time
