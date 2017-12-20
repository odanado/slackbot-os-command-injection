import sys
import unittest
import yaml

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
