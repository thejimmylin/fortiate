import unittest
import os
from base import ShellCommand, FortiConfig


class TestShellCommand(unittest.TestCase):

    def test_shellcommand(self):
        self.assertIsInstance(ShellCommand(), ShellCommand)

    def test_shellcommand_hasattr(self):
        sc = ShellCommand()
        self.assertTrue(hasattr(sc, 'leading'))
        self.assertTrue(hasattr(sc, 'trailing'))
        self.assertTrue(hasattr(sc, 'mid'))
        self.assertTrue(hasattr(sc, 'midset'))

    def test_shellcommand_midset(self):
        s = "    set service HTTP HTTPS 'service tcp 8080-8080 udp 0-0'\n"
        sc = ShellCommand(s)
        self.assertEqual(
            sc.midset,
            ['set', 'service', 'HTTP', 'HTTPS', 'service tcp 8080-8080 udp 0-0']
        )

    def test_shellcommand_attr_raw_readonly(self):
        with self.assertRaises(AttributeError):
            s = "    set service HTTP HTTPS 'service tcp 8080-8080 udp 0-0'\n"
            sc = ShellCommand(s)
            sc.raw = 'abc'

    def test_shellcommand_invalid_input_should_fail(self):
        with self.assertRaises(ValueError):
            s = "    set service 'HTTP' HTTPS 'service tcp 8080-8080 udp 0-0'\n"
            ShellCommand(s)


class TestFortiConfig(unittest.TestCase):

    def test_forticonfig(self):
        current_dir = os.path.dirname(__file__)
        conf_file = os.path.join(current_dir, 'conf', 'firewall_policy.conf')
        with open(file=conf_file, mode='r', encoding='utf-8') as f:
            lines = f.read().splitlines()
        fc = FortiConfig(lines)
        print(fc.context)


if __name__ == '__main__':
    unittest.main()
