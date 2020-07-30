from .commands import IndentedShellCommand


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