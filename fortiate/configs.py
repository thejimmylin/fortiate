from .commands import ShellCommand


class IndentedShellConfig():

    def __init__(self, lines):
        self._init_with_lines(lines)

    def _init_with_lines(self, lines):
        config_key = ''
        edit_key = ''
        set_key = ''
        context = {}
        for index, line in enumerate(lines):
            command = ShellCommand(raw=line)
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


# pseudocode

'''
class FortiAddressConfig(IndentedShellConfig):

    edit = commands.EditCommand(max_length=64, uniqe=True)
    subnet = commands.SetCommand(max_length=64)
    comments = commands.SetCommand(max_length=64, blank=True)
'''
