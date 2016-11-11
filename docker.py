import os
import subprocess

from constant import DockerImage
from constant import Command
from constant import StartArgs
from utils import init_logger


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

        self.logger = init_logger(__name__)

    def _logging_cmd(self, cmd):
        self.logger.info(cmd)

    def _logging_docker_cmd(self, cmd):
        self._logging_cmd("command run: {}".format(cmd))

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

        self._logging_docker_cmd(' '.join(cmds))

        p = subprocess.Popen(' '.join(cmds), shell=True,
                             stdout=subprocess.PIPE)
        self.container_id, _ = p.communicate()
        self.container_id = self.container_id.decode('utf8').strip()
        self._logging_cmd('container id: {}'.format(self.container_id))

    def copy(self):
        cmd = "docker cp /tmp/workspace {}:/".format(self.container_id)
        self._logging_docker_cmd(cmd)
        os.system(cmd)

    def remove(self):
        cmd = "docker rm {}".format(self.container_id)
        self._logging_docker_cmd(cmd)
        os.system(cmd)

    def _get_time(self):
        cmd = "docker cp {}:/time.txt /tmp/workspace/time.txt".format(
            self.container_id)
        self._logging_docker_cmd(cmd)
        os.system(cmd)
        with open('/tmp/workspace/time.txt') as f:
            time = f.readline()

        return time

    def start(self):
        cmd = "docker start -i {}".format(self.container_id)
        self._logging_docker_cmd(cmd)
        p = subprocess.Popen(cmd, shell=True,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()

        return stdout, stderr, self._get_time()


if __name__ == '__main__':
    pass
