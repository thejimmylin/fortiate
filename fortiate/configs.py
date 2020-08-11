import json
from collections import OrderedDict
from .commands import ShellCommand


__all__ = ['FortiConfig']


class FortiConfig():

    def __init__(self, lines):
        config_key = ''
        edit_key = ''
        set_key = ''
        config = OrderedDict()
        for line in lines:
            sc = ShellCommand(line, quote_char='"')
            if sc.phrases[0] == 'config':
                config_key = sc.command
                config[config_key] = {}
                continue
            if sc.phrases[0] == 'edit':
                edit_key = sc.command
                config[config_key][edit_key] = {}
                continue
            if sc[0] == 'set':
                set_key = sc[:2].command
                value = sc[2:]
                config[config_key][edit_key][set_key] = value
                continue
            if sc.phrases[0] in ('next', 'end'):
                continue
            raise ValueError(
                f'"{line}" is a valid line.'
            )
        self.config = config

    def __str__(self):
        lines = []
        for config_key, config_value in self.config.items():
            lines += [config_key]
            for edit_key, edit_value in config_value.items():
                lines += ['    ' + edit_key]
                for set_key, set_value in edit_value.items():
                    lines += ['        ' + set_key + ' ' + set_value.command]
        return '\n'.join(lines)
