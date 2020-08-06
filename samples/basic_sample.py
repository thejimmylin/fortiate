import sys
import os
"""
In case fortiate is not installed as a package and is added to the $PYTHONPATH
we add it to sys.path manually here. If fortiate has been added to your
$PYTHONPATH already, this could be skipped.
"""
fortiate_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
)
sys.path.insert(1, fortiate_path)
"""
The above sys things could be skipped if you add fortiate to the $PYTHONPATH.
"""
import json
from fortiate.commands import shlex_join, ShellCommand  # NOQA


# Locate the conf file with relative path by module os.
current_dir = os.path.dirname(__file__)
conf_file = os.path.join(current_dir, 'conf', 'firewall_policy.conf')


with open(file=conf_file, mode='r', encoding='utf-8') as f:
    lines = f.read().splitlines()

print('\n')
print('------example1------')
print('\n')
for line in lines:
    isc = ShellCommand(line)
    print(isc.raw)

print('\n')
print('------example2------')
print('\n')
for line in lines:
    isc = ShellCommand(line)
    print(isc.command)

print('\n')
print('------example3------')
print('\n')
for line in lines:
    isc = ShellCommand(line)
    print(isc.split_command)

print('\n')
print('------example4------')
print('\n')
configs = {}
for index, line in enumerate(lines):
    isc = ShellCommand(line)
    if isc.split_command[0] == 'config':
        config_key = isc.command
        configs[config_key] = {}
        continue
    if isc.split_command[0] == 'edit':
        edit_key = isc.command
        configs[config_key][edit_key] = {}
        continue
    if isc.split_command[0] == 'set':
        k, value = isc.split_command[:2], isc.split_command[2:]
        set_key = shlex_join(k, whitespace=' ')
        configs[config_key][edit_key][set_key] = shlex_join(value, whitespace=' ')
        continue
    if isc.split_command[0] in ('next', 'end'):
        continue
    raise ValueError(f'An invalid line exsits in config file, index = {index}, line = {line}.')

# Pretty-print the configs dictionary.
print(json.dumps(configs, indent=4))
