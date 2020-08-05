import re
from shlex import shlex


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


def shlex_join(split_command, whitespace=' ', using_single_quotes=True):
    """
    Re-define the join function in shlex to make it possible to specify custom
    whitespace and quotes when we call it.
    """
    return whitespace.join(quote(arg, using_single_quotes=using_single_quotes) for arg in split_command)


_find_unsafe = re.compile(r'[^\w@%+=:,./-]', re.ASCII).search


def quote(s, using_single_quotes=True):
    """
    Re-define the quote function in shlex to make it possible to specify custom
    quote when we call it.
    """
    if not s:
        return "''"
    if _find_unsafe(s) is None:
        return s

    if using_single_quotes:
        return "'" + s.replace("'", "'\"'\"'") + "'"
    else:
        return '"' + s.replace('"', '"\'"\'"') + '"'


class ShellCommand():
    """
    A class describing a single line shell-like command.
    """

    def __init__(self, raw='', lstrip_chars=' \t\r\n', rstrip_chars=' \t\r\n', split_chars=' \t\r\n',
                 join_char=' ', check_consistency_silently=False, using_single_quotes=True):

        self._raw = raw
        self._lstrip_chars = lstrip_chars
        self._rstrip_chars = rstrip_chars
        self._split_chars = split_chars
        self._join_char = join_char
        self._using_single_quotes = using_single_quotes
        if check_consistency_silently and not self.is_consistent():
            self._print_consitency_warning()

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.raw.__repr__()}>'

    @property
    def raw(self):
        return self._raw

    @property
    def lstrip_chars(self):
        return self._lstrip_chars

    @property
    def rstrip_chars(self):
        return self._rstrip_chars

    @property
    def split_chars(self):
        return self._split_chars

    @property
    def join_char(self):
        return self._join_char

    @property
    def using_single_quotes(self):
        return self._using_single_quotes

    @property
    def leading(self):
        return self._raw[:-len(self._raw.lstrip(self._lstrip_chars))]

    @leading.setter
    def leading(self, value):
        self._raw = value + self._raw.lstrip(self._lstrip_chars)

    @property
    def trailing(self):
        return self._raw[len(self._raw.rstrip(self._rstrip_chars)):]

    @trailing.setter
    def trailing(self, value):
        self._raw = self._raw.rstrip(self._rstrip_chars) + value

    @property
    def command(self):
        return self._raw.lstrip(self._lstrip_chars).rstrip(self._rstrip_chars)

    @command.setter
    def command(self, value):
        self._raw = self.leading + value + self.trailing

    @property
    def split_command(self):
        return shlex_split(
            self.command, whitespace=self._split_chars
        )

    @split_command.setter
    def split_command(self, value):
        self.command = shlex_join(
            value, whitespace=self._join_char, using_single_quotes=self._using_single_quotes
        )

    def is_consistent(self):
        joined_command = shlex_join(
            self.split_command, whitespace=self._join_char, using_single_quotes=self._using_single_quotes
        )
        return self.leading + joined_command + self.trailing == self._raw

    def _print_consitency_warning():
        consistency_warning = (
            'Warning: The raw command and its concatenation of '
            'leading + split_command + trailing are not consistent. '
            'You may consider the following common reason:\n\n'
            '1. There are consecutive/trailing whitespaces.\n'
            '2. There are inconsistent whitespaces between join_char '
            'and the original one/ones.\n'
            '3. There are quotes around no-whitespace text.\n'
            '4. There are double quotes.'
        )
        print(consistency_warning)
