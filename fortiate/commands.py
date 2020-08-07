import re
from shlex import shlex


__all__ = ['shlex_split', 'shlex_join', 'quote', 'ShellCommand',
           'FortiConfigCommand', 'FortiEditCommand', 'FortiSetCommand']


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


def shlex_join(split_command, whitespace=' ', quote_char="'"):
    """
    Re-define the join function in shlex to make it possible to specify custom
    whitespace and quote_char when we call it.
    """
    return whitespace.join(quote(arg, quote_char=quote_char) for arg in split_command)


_find_unsafe = re.compile(r'[^\w@%+=:,./-]', re.ASCII).search


def quote(s, quote_char="'"):
    """
    Re-define the quote function in shlex to make it possible to specify custom
    quote_char when we call it.
    """
    if not s:
        return "''"
    if _find_unsafe(s) is None:
        return s

    the_other_quote_char = '"' if quote_char == "'" else "'"
    q1 = quote_char
    q2 = the_other_quote_char
    return q1 + s.replace(q1, q1 + q2 + q1 + q2 + q1) + q1


class ShellCommand():
    """
    A class describing a single line shell-like command.
    """

    def __init__(self, raw='', lstrip_chars=' \t\r\n', rstrip_chars=' \t\r\n',
                 split_chars=' \t\r\n', join_char=' ', quote_char="'"):
        self._raw = raw
        self._lstrip_chars = lstrip_chars
        self._rstrip_chars = rstrip_chars
        self._split_chars = split_chars
        self._join_char = join_char
        self._quote_char = quote_char

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self._raw.__repr__()}>'

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
    def quote_char(self):
        return self._quote_char

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
    def mid(self):
        return self._raw.lstrip(self._lstrip_chars).rstrip(self._rstrip_chars)

    @mid.setter
    def mid(self, value):
        self._raw = self.leading + value + self.trailing

    @property
    def midset(self):
        return shlex_split(
            self.mid, whitespace=self._split_chars
        )

    @midset.setter
    def midset(self, value):
        self.mid = shlex_join(
            value, whitespace=self._join_char, quote_char=self._quote_char
        )

    @property
    def is_consistent(self):
        joined_midset = shlex_join(
            self.midset, whitespace=self._join_char, quote_char=self._quote_char
        )
        return self.leading + joined_midset + self.trailing == self._raw


class FortiConfigCommand(ShellCommand):

    def is_valid(self):
        if len(self.midset) != 2:
            return False
        if self.midset[:1] != ['config']:
            return False
        self._generate_cleaned_data()
        return True

    def _generate_cleaned_data(self):
        set_key = shlex_join(
            self.midset[:1], whitespace=self._join_char, quote_char=self._quote_char
        )
        set_value = self.midset[1:]
        self.cleaned_data = {
            set_key: set_value
        }


class FortiEditCommand(ShellCommand):

    def is_valid(self):
        if len(self.midset) != 2:
            return False
        if self.midset[:1] != ['edit']:
            return False
        self._generate_cleaned_data()
        return True

    def _generate_cleaned_data(self):
        set_key = shlex_join(
            self.midset[:1], whitespace=self._join_char, quote_char=self._quote_char
        )
        set_value = self.midset[1:]
        self.cleaned_data = {
            set_key: set_value
        }


class FortiSetCommand(ShellCommand):

    def is_valid(self):
        if len(self.midset) < 3:
            return False
        if self.midset[:1] != ['set']:
            return False
        self._generate_cleaned_data()
        return True

    def _generate_cleaned_data(self):
        set_key = shlex_join(
            self.midset[:2], whitespace=self._join_char, quote_char=self._quote_char
        )
        set_value = self.midset[2:]
        self.cleaned_data = {
            set_key: set_value
        }
