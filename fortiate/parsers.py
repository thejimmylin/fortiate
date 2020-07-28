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


def shlex_split(s, comments=False, posix=True, whitespace=' \t\r\n', whitespace_split=True):
    """
    Re-define the split function in shlex to make it possible to
    specify custom whitespace characters when we call this function.
    When not provided, it act like the original one.
    """
    lex = shlex(s, posix=posix)
    lex.whitespace = whitespace
    lex.whitespace_split = whitespace_split
    if not comments:
        lex.commenters = ''
    return list(lex)


class IndentedShellCommand():
    """
    A class describing a single line shell-like command with indentation,
    generating formatted data using module shlex and preserve the indentation
    part of it.
    """

    def __init__(self, raw, indented_with=' ', whitespace=' '):
        self._raw = raw
        self._indented_with = indented_with
        self._whitespace = whitespace
        if not self.is_consistent():
            print(
                'Warning: The raw command and its concatenation of '
                'indentation and split command are not consistent. Maybe '
                'there are consecutive/trailing white spaces?'
            )

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
            self.command, posix=False, whitespace=self._whitespace
        )

    @split_command.setter
    def split_command(self, value):
        self.command = self._whitespace.join(value)

    def is_consistent(self):
        joined_command = self._whitespace.join(self.split_command)
        return self.indentation + joined_command == self._raw


class FortiConfig():

    def __init__(self, lines=[], file=''):
        if lines:
            self.init_with_lines(lines)
        elif file:
            self.init_with_file(file)
        else:
            raise ValueError('No commands/file provided, initialization failed.')

    @property
    def commands(self):
        return self._commands

    def init_with_lines(self, lines):
        config_key = ''
        edit_key = ''
        set_key = ''
        context = {}
        for index, line in enumerate(lines):
            command = IndentedShellCommand(raw=line)
            if command.split_command[0] == 'set':
                k, value = command.split_command[:2], command.split_command[2:]
                set_key = ' '.join(k)
                context[config_key][edit_key][set_key] = ' '.join(value)
                continue
            if command.split_command[0] == 'edit':
                edit_key = ' '.join(command.split_command)
                context[config_key][edit_key] = {}
                continue
            if command.split_command[0] == 'config':
                config_key = ' '.join(command.split_command)
                context[config_key] = {}
                continue
            if command.split_command[0] in ('next', 'end'):
                continue
            raise ValueError(f'An invalid line exsits in config file, index = {index}, line = {line}.')
        self.context = context

    def init_with_file(self, file):
        with open(file=file, mode='r', encoding='utf-8') as f:
            lines = f.read().splitlines()
        self.init_with_lines(lines)


def print_self(stdout):
    print('print_self' + '(' + stdout.__repr__() + ')')


class FortiStyleStr():

    def __init__(self, raw):
        self.raw = raw

    def __repr__(self):
        return self.__repr__()

    def __str__(self):
        return self.__str__()
