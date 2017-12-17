import sys
import unittest

sys.path.append('./plugins')
from os_command_injection import get_config  # NOQA


class TestOSCommandInjection(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_config(self):
        config = get_config('c')
        self.assertIsNotNone(config)
