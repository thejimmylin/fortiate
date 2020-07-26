import re
from shlex import shlex


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


class IndentShellCommand():
    """
    A class describing a single line shell-like command with indentations,
    generating formatted data with module shlex and preserve the indentation
    part of it.
    """

    def __init__(self, raw, indentation_char=' ', whitespace=' '):
        self._raw = raw
        self._indentation_char = indentation_char
        self._whitespace = whitespace
        self._indentation = self.raw[
            :-len(self.raw.lstrip(self._indentation_char))
        ]
        self._command = self.raw.lstrip(self._indentation_char)
        self._split_command = shlex_split(
            self._command, posix=False, whitespace=self._whitespace
        )
        if not self.is_consistent():
            print(
                'Warning: The raw command and its concatenation of '
                'indentation and split command are not consistent. Maybe '
                'there are trailing spaces?'
            )

    def __str__(self):
        return self.raw

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self}>'

    @property
    def raw(self):
        return self._raw

    @property
    def indentation_char(self):
        return self._indentation_char

    @property
    def whitespace(self):
        return self._whitespace

    @property
    def indentation(self):
        return self._indentation

    @property
    def command(self):
        return self._command

    @property
    def split_command(self):
        return self._split_command

    @property
    def cleaned(self):
        if hasattr(self, '_cleaned'):
            return self._cleaned
        else:
            print(
                'Warning: The raw command and its concatenation of '
                'indentation and split command are not consistent. Maybe '
                'there are trailing spaces?'
            )

    def is_consistent(self):
        concatenation = self._indentation + self._whitespace.join(self._split_command)
        if concatenation == self._raw:
            self._cleaned = self._raw
            return True
        else:
            self._cleaned = None
            return False
