import unittest
import os
import json
from base import ShellCommand, FortiConfig


class TestShellCommand(unittest.TestCase):

    def test_shellcommand_init(self):
        self.assertIsInstance(ShellCommand(), ShellCommand)

    def test_shellcommand_hasattr(self):
        sc = ShellCommand()
        self.assertTrue(hasattr(sc, 'phrases'))
        self.assertTrue(hasattr(sc, 'command'))

    def test_shellcommand_attrs_readonly(self):
        with self.assertRaises(AttributeError):
            s = "    set service HTTP HTTPS 'service tcp 8080-8080 udp 0-0'\n"
            sc = ShellCommand(s)
            sc.quote_char = '"'


class TestFortiConfig(unittest.TestCase):

    def test_forticonfig_init(self):
        self.assertIsInstance(FortiConfig(), FortiConfig)

    def test_use_comment_field_as_json_field1(self):
        current_dir = os.path.dirname(__file__)
        conf_file = os.path.join(current_dir, 'conf', 'firewall_policy.conf')
        with open(file=conf_file, mode='r', encoding='utf-8') as f:
            lines = f.read().splitlines()
        fc = FortiConfig(lines)
        a = fc.data['config firewall policy']['edit 168']['set comments'].phrases
        dct = {'customer': 'Jimmy Lin', 'remark': 'this comment contains json'}
        b = [json.dumps(dct)]
        self.assertEqual(a, b)

    def test_use_comment_field_as_json_field2(self):
        current_dir = os.path.dirname(__file__)
        conf_file = os.path.join(current_dir, 'conf', 'firewall_policy.conf')
        with open(file=conf_file, mode='r', encoding='utf-8') as f:
            lines = f.read().splitlines()
        fc = FortiConfig(lines)
        a = fc.data['config firewall policy']['edit 168']['set comments'].phrases
        dct = {'customer': 'Jimmy Lin', 'remark': 'this comment contains json', 'another field': 'another value'}
        b = [json.dumps(dct)]
        self.assertNotEqual(a, b)


if __name__ == '__main__':
    unittest.main()
