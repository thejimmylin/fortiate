from shlex import shlex
from shlex import quote


def shlex_split(s, comments=False, posix=True, whitespace=' \t\r\n', whitespace_split=True):
    """
    Re-define the split function in shlex to make it possible to specify
    custom whitespace and whitespace_split when we call it.
    """
    lex = shlex(s, posix=posix)
    lex.whitespace = whitespace
    lex.whitespace_split = whitespace_split
    if not comments:
        lex.commenters = ''
    return list(lex)


def shlex_join(split_command, whitespace=' '):
    """
    Re-define the join function in shlex to make it possible to specify custom
    whitespace when we call it.
    """
    return whitespace.join(quote(arg) for arg in split_command)


class IndentedShellCommand():
    """
    A class describing a single line shell-like command with indentation,
    generating formatted data using module shlex and preserve the indentation
    part of it.
    """

    _warning_of_inconsistency = (
        'Warning: The raw command and its concatenation of '
        'indentation and split command are not consistent. You may consider'
        'the following possibility:\n\n'
        '1. There are consecutive/trailing whitespaces.\n'
        '2. There are quotes around no-whitespace text.\n'
        '3. There are double quotes.'
    )

    def __init__(self, raw='', indented_with=' ', whitespace=' ', fail_silently=True):
        self._raw = raw
        self._indented_with = indented_with
        self._whitespace = whitespace
        if not self.is_consistent() and not fail_silently:
            print(self._warning_of_inconsistency)

    def __str__(self):
        return self.raw

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self}>'

    @property
    def raw(self):
        return self._raw

    @property
    def indented_with(self):
        return self._indented_with

    @property
    def whitespace(self):
        return self._whitespace

    @property
    def indentation(self):
        return self._raw[:-len(self._raw.lstrip(self._indented_with))]

    @indentation.setter
    def indentation(self, value):
        self._raw = value + self._raw.lstrip(self._indented_with)

    @property
    def command(self):
        return self._raw.lstrip(self._indented_with)

    @command.setter
    def command(self, value):
        self._raw = (
            self._raw[:-len(self._raw.lstrip(self._indented_with))] +
            value
        )

    @property
    def split_command(self):
        return shlex_split(
            self.command, whitespace=self._whitespace
        )

    @split_command.setter
    def split_command(self, value):
        self.command = shlex_join(value, whitespace=self._whitespace)

    def is_consistent(self):
        joined_command = shlex_join(
            self.split_command, whitespace=self._whitespace
        )
        return self.indentation + joined_command == self._raw
