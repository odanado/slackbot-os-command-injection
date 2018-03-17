import sys
import unittest
import yaml
from pathlib import Path

sys.path.append('./plugins')
from code_runner import CodeRunner  # NOQA


class TestCodeRunner(unittest.TestCase):
    def setUp(self):
        self.code_runner = CodeRunner('odanado/os-command-injection')


def make_test(test_file, config):

    def test(self):
        stdout_file = test_file.with_suffix('.stdout')
        stderr_file = test_file.with_suffix('.stderr')

        source_code = test_file.read_text()

        stdout, stderr, _ = self.code_runner.run(source_code, **config)

        self.assertTrue(stdout_file.exists())

        self.assertEqual(stdout, stdout_file.read_text().strip())

        if stderr_file.exists():
            self.assertEqual(stderr, stderr_file.read_text().strip())

    return test


def register_tests(path):
    tests_path = path / 'tests'
    config = yaml.load((path / 'config.yml').read_text())
    suffix = Path(config['filename']).suffix

    test_files = tests_path.glob('*' + suffix)

    for test_file in test_files:
        setattr(TestCodeRunner, test_file.name, make_test(test_file, config))


for lang in Path('./langs').glob('*'):
    register_tests(lang)
