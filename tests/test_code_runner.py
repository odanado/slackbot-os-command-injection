import sys
import unittest
import yaml
from pathlib import Path

sys.path.append('./plugins')
from code_runner import CodeRunner  # NOQA


class TestBashRunner(unittest.TestCase):
    def setUp(self):
        self.code_runner = CodeRunner('odanado/os-command-injection')
        self.source_code = "echo 'Hello World!'"
        self.config = yaml.load(open('./langs/bash/config.yml'))

    def test_run(self):
        stdout, _, _ = self.code_runner.run(self.source_code, **self.config)
        self.assertEqual(stdout, 'Hello World!')


class TestPython3Runner(unittest.TestCase):
    def setUp(self):
        self.code_runner = CodeRunner('odanado/os-command-injection')
        self.config = yaml.load(open('./langs/python3/config.yml'))

    def test_run(self):
        source_code = """
print('Hello World!')
print('stdout')
        """
        stdout, _, _ = \
            self.code_runner.run(source_code, **self.config)
        self.assertEqual(stdout, 'Hello World!\nstdout')

    def test_run_multiline(self):
        source_code = """
import sys
print('Hello World!', file=sys.stdout)
print('stderr', file=sys.stderr)
        """
        stdout, stderr, _ = \
            self.code_runner.run(source_code, **self.config)
        self.assertEqual(stdout, 'Hello World!')


class TestBrainfuckRunner(unittest.TestCase):
    def setUp(self):
        self.code_runner = CodeRunner('odanado/os-command-injection')
        self.source_code = """
+++++++++[>++++++++>+++++++++++>+++++<<<-]>.>++.+++++++..+++.>-.
------------.<++++++++.--------.+++.------.--------.>+.
"""
        self.config = yaml.load(open('./langs/brainfuck/config.yml'))

    def test_run(self):
        stdout, _, _ = \
            self.code_runner.run(self.source_code, **self.config)
        self.assertEqual(stdout, 'Hello, world!')


class TestCsharpShellRunner(unittest.TestCase):
    def setUp(self):
        self.code_runner = CodeRunner('odanado/os-command-injection')
        self.source_code = """
Console.WriteLine("Hello, world!");
        """
        self.config = yaml.load(open('./langs/csharp-shell/config.yml'))

    def test_run(self):
        stdout, _, _ = \
            self.code_runner.run(self.source_code, **self.config)
        self.assertEqual(stdout, 'Hello, world!')


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

    tests = []
    for test_file in test_files:
        setattr(TestCodeRunner, test_file.name, make_test(test_file, config))

    return tests


for lang in Path('./langs').glob('*'):
    register_tests(lang)
