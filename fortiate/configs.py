from collections import OrderedDict
from .commands import ShellCommand


__all__ = ['FortiConfig']


class FortiConfig():

    def __init__(self, lines):
        config_key = ''
        edit_key = ''
        set_key = ''
        context = OrderedDict()
        for line in lines:
            sc = ShellCommand(line, quote_char='"')
            if sc.midset[0] == 'set':
                k, value = sc.midset[:2], sc.midset[2:]
                set_key = ' '.join(k)
                context[config_key][edit_key][set_key] = ' '.join(value)
                continue
            if sc.midset[0] == 'edit':
                edit_key = ' '.join(sc.midset)
                context[config_key][edit_key] = {}
                continue
            if sc.midset[0] == 'config':
                config_key = ' '.join(sc.midset)
                context[config_key] = {}
                continue
            if sc.midset[0] in ('next', 'end'):
                continue
            raise ValueError(
                f'"{line}" is a valid line.'
            )
        self.context = context
