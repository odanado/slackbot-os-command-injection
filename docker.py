import os
import sys
import subprocess
from constant import DockerImage
from constant import Command
from constant import StartArgs


def _conv_args(kwargs):
    args = []
    for k, v in kwargs.items():
        if isinstance(v, str):
            args.append("{} {}".format(k, v))
        if isinstance(v, list):
            for x in v:
                args.append("{} {}".format(k, x))
    return ' '.join(args)


class Docker(object):

    def __init__(self, lang):
        self.lang = lang

    def create(self):
        cmd = Command[self.lang]
        compile_cmd = cmd['compile']
        run_cmd = cmd['run']
        exec_cmd = "{} && {}".format(compile_cmd, run_cmd)
        args = _conv_args(StartArgs)
        cmds = []
        cmds.append("docker create -i")
        cmds.append(args)
        cmds.append("{}:{}".format(DockerImage, self.lang))
        cmds.append('/usr/bin/time -q -f "%e" -o /time.txt')
        cmds.append('timeout 3')
        cmds.append('su nobody -s /bin/bash -c "{}"'.format(exec_cmd))

        sys.stderr.write(
            'create docker container: {}\n'.format(' '.join(cmds)))
        sys.stderr.flush()

        self.container_id = subprocess.getoutput(' '.join(cmds))

    def copy(self):
        cmd = "docker cp /tmp/workspace {}:/".format(self.container_id)
        os.system(cmd)
        sys.stderr.write('copy workspace: {}\n'.format(cmd))
        sys.stderr.flush()

    def remove(self):
        cmd = "docker rm {}".format(self.container_id)
        os.system(cmd)
        sys.stderr.write('remove container: {}\n'.format(cmd))
        sys.stderr.flush()

    def _get_time(self):
        cmd = "docker cp {}:/time.txt /tmp/workspace/time.txt".format(
            self.container_id)
        os.system(cmd)
        with open('/tmp/workspace/time.txt') as f:
            time = f.readline()

        return time

    def start(self):
        cmd = "docker start -i {}".format(self.container_id)
        sys.stderr.write('start container: {}\n'.format(cmd))
        sys.stderr.flush()
        p = subprocess.Popen(cmd, shell=True,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()

        return stdout, stderr, self._get_time()


if __name__ == '__main__':
    pass
