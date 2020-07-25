import re
from shlex import shlex


def shlex_split(s, comments=False, posix=True, whitespace=' \t\r\n'):
    """
    Re-define the split function in shlex to make it possible to
    specify custom whitespace characters when we call this function.
    When not provided, it act like the original one.
    """
    lex = shlex(s, posix=posix)
    lex.whitespace = whitespace
    lex.whitespace_split = True
    if not comments:
        lex.commenters = ''
    return list(lex)


class Parser():

    def get_leading_spaces(self, s, space=' '):
        leading_spaces = (
            len(s) - len(s.lstrip(space))
        ) * space
        return leading_spaces

    def get_formatted_lines(self, lines):
        formatted_lines = [
            [
                self.get_leading_spaces(s=line)
            ] + shlex.split(line)
            for line in lines
        ]
        return formatted_lines

    def get_formatted_dct(self, formatted_lines):
        current_config = ''
        current_edit = ''
        formatted_dct = {}
        for index, line in enumerate(formatted_lines):
            if len(line) < 2:
                raise Exception(f'An invalid line exsits in config file, index = {index}, line = {line}.')
            indent, *values = line
            prefix = values[0]
            if prefix not in ['config', 'end', 'edit', 'next', 'set']:
                raise Exception(f'A line with unknown prefix exsits in config file, index = {index}, line = {line}.')
            if prefix == 'config':
                current_config = ' '.join(values)
                formatted_dct[current_config] = {}
                continue
            if prefix == 'edit':
                current_edit = ' '.join(values)
                formatted_dct[current_config][current_edit] = {}
                continue
            if prefix in ['next', 'end']:
                continue
            # Here, it should be true that prefix == 'set'
            current_set = ' '.join(values[0:2])
            formatted_dct[current_config][current_edit][current_set] = ' '.join(values[2:])
        return formatted_dct

    def get_reorganize_lines(self, formatted_lines):
        return [line[0] + shlex.join(line[1:]) for line in formatted_lines]


class IndentShellLine():
    """
    A single line should not include any line feed, or in fact it's two lines.
    """

    whitespace = ' '
    line_feed_chars = ['\r', '\n', ]

    def __init__(self, raw, space='', lfs=()):
        self.raw = raw
        self.leading_whitespace = self.raw[:-len(self.raw.lstrip(self.whitespace))]
        self.trailing_whitespace = self.raw[len(self.raw.rstrip(self.whitespace)):]
        self.space = space or ' '
        self.lfs = lfs or ('\n', )
        for lf in self.lfs:
            if lf in self.raw[:-1]:
                raise ValueError('A line feed exists in the line.')
        self.indent = self.get_indent()
        self.lf = self.raw[-1] if self.raw.endswith(self.lfs) else ''
        self.formatted = self.get_formatted()

    def __str__(self):
        return self.raw

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self}>'

    def get_indent(self):
        indent = (
            len(self.raw) - len(self.raw.lstrip(self.space))
        ) * self.space
        return indent

    def get_formatted(self):
        formatted = shlex_split(self.raw, posix=False, whitespace=self.whitespace)
        return formatted

    def rebuild(self):
        self.raw = self.indent + ' '.join(self.formatted) + self.lf
