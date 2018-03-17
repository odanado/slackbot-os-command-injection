import time
import tarfile

from io import BytesIO

import docker


class CodeRunner(object):
    def __init__(self, docker_image):
        self.docker_image = docker_image
        self.docker_client = docker.from_env()
        self.create_kwargs = {
            'network': 'none',
            'cpuset_cpus': '0',
            'mem_limit': '128m',
            'memswap_limit': '128m',
            'hostname': 'os-command-injection',
            'pids_limit': 30,
            'ulimits': [{'name': 'fsize', 'soft': 1000000, 'hard': 1000000}]
        }

    def _put_source_code(self, container, filename, source_code):
        file_data = source_code.encode('utf8')
        pw_tarstream = BytesIO()
        pw_tar = tarfile.TarFile(fileobj=pw_tarstream, mode='w')
        tarinfo = tarfile.TarInfo(name=filename)
        tarinfo.size = len(file_data)
        tarinfo.mtime = time.time()
        # tarinfo.mode = 0600
        pw_tar.addfile(tarinfo, BytesIO(file_data))
        pw_tar.close()
        pw_tarstream.seek(0)

        with pw_tarstream as archive:
            container.put_archive('/tmp/workspace', archive)

    def _get_results(self, container):
        stream, _ = container.get_archive('/tmp/dist')
        raw_data = next(stream)
        with tarfile.open(fileobj=BytesIO(raw_data), mode='r') as tf:
            stdout = tf.extractfile('dist/stdout.txt').readlines()
            stderr = tf.extractfile('dist/stderr.txt').readlines()
            running_time = tf.extractfile('dist/time.txt').readline().strip()

        stdout = '\n'.join([x.decode('utf8').strip() for x in stdout]).strip()
        stderr = '\n'.join([x.decode('utf8').strip() for x in stderr]).strip()
        running_time = running_time.decode('utf8')

        return stdout, stderr, running_time

    def run(self, source_code, docker_tag, filename,
            compile_cmd, run_cmd, **kwargs):
        client = self.docker_client
        cmd = ('{} && {} > /tmp/dist/stdout.txt '
               '2> /tmp/dist/stderr.txt').format(compile_cmd, run_cmd)

        docker_image = '{}:{}'.format(self.docker_image, docker_tag)
        container = client.containers.create(
            docker_image, '"{}"'.format(cmd), **self.create_kwargs)

        self._put_source_code(container, filename, source_code)

        container.start()
        container.wait()

        results = self._get_results(container)

        return results


if __name__ == '__main__':
    code_runner = CodeRunner('odanado/os-command-injection')
    src_code = """
    echo hoge
    """

    results = code_runner.run(
        src_code, 'bash',
        'Main.sh', "cat Main.sh | tr -d '\\r' > a.out", "bash a.out")

    print(results)
