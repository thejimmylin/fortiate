import unittest
from base import ShellCommand


class TestStringMethods(unittest.TestCase):

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
            s = 'hello ShellCommand'
            sc = ShellCommand(s)
            sc.raw = 'abc'


if __name__ == '__main__':
    unittest.main()
