import sys
import unittest

sys.path.append('./plugins')
from os_command_injection import get_config, get_lang  # NOQA


class TestOSCommandInjection(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_config(self):
        config = get_config('c')
        self.assertIsNotNone(config)

    def test_get_lang(self):
        self.assertEqual('bash', get_lang('mention'))
        self.assertEqual('c', get_lang('mention\nc'))
        self.assertEqual('java', get_lang('mention\nJava'))
