import re
from shlex import shlex


__all__ = ['shlex_split', 'shlex_join', 'quote', 'ShellCommand']


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
    # Use quote_char, and put quote_char shown in s into the_other_quote_char.
    # For example, quote_char is single quote, and then the_other_quote_char is double quote.
    # Now if s is McDonald's, it will be quoted as
    # 'McDonald'"'"'s'
    return q1 + s.replace(q1, q1 + q2 + q1 + q2 + q1) + q1


class ShellCommand():
    """
    A class describing a single line shell-like command.
    """

    def __init__(self, phrases=[], split_chars=' \t\r\n', join_char=' ', quote_char="'", check_consistency=True):
        self._split_chars = split_chars
        self._join_char = join_char
        self._quote_char = quote_char
        self._check_consistency = check_consistency
        self.phrases = phrases

    def __repr__(self):
        return f'{self.__class__.__name__}({self._phrases.__repr__()})'

    def __len__(self):
        return len(self._phrases)

    def __getitem__(self, obj):
        if isinstance(obj, slice):
            return ShellCommand(self._phrases[obj])
        if isinstance(obj, int):
            return self._phrases[obj]
        raise ValueError

    def __add__(self, obj):
        if isinstance(obj, ShellCommand):
            return ShellCommand(self._phrases + obj._phrases)
        raise ValueError

    def __eq__(self, obj):
        if not isinstance(obj, ShellCommand):
            return False
        is_equal = (
            self._split_chars == obj._split_chars and
            self._join_char == obj._join_char and
            self._quote_char == obj._quote_char and
            self._check_consistency == obj._check_consistency and
            self._phrases == obj._phrases
        )
        return is_equal

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
    def check_consistency(self):
        return self._check_consistency

    @property
    def phrases(self):
        return self._phrases

    @phrases.setter
    def phrases(self, value):
        self._phrases = value
        if self._check_consistency and not self.is_consistent():
            raise ValueError(f'{self} is not consistent.')

    @property
    def command(self):
        return shlex_join(self._phrases, whitespace=self._join_char, quote_char=self._quote_char)

    @command.setter
    def command(self, value):
        new_phrases = shlex_split(value, whitespace=self._split_chars)
        self.phrases = new_phrases

    def is_consistent(self):
        phrases = self._phrases
        command = shlex_join(self._phrases, whitespace=self._join_char, quote_char=self._quote_char)
        split_command = shlex_split(command, whitespace=self._split_chars)
        return phrases == split_command
