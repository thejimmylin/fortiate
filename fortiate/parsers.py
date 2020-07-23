import os
import shlex
import json


# Define & Configure
BASE_DIR = os.path.dirname(__file__)
FILE_INPUT_PATH = os.path.join(BASE_DIR, 'conf', 'firewall policy.conf')
FILE_OUTPUT_PATH = os.path.join(BASE_DIR, 'conf', 'firewall policy output.conf')


def get_leading_spaces(string, space=' '):
    leading_spaces_count = len(string) - len(string.lstrip(space))
    return space * leading_spaces_count


# Read and format with shlex
with open(file=FILE_INPUT_PATH, mode='r', encoding='utf-8') as file:
    formatted_lines = [[get_leading_spaces(line)] + shlex.split(line) for line in file.readlines()]

# All data-manipulating things happen here
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

print(json.dumps(obj=formatted_dct, sort_keys=True, indent=4))
"""
we should get somthing like this:

{
    "config firewall policy": {
        "edit 168": {
            "set action": "accept",
            "set comments": "\"customer\": \"Jimmy Lin\"",
            "set dstaddr": "all",
            "set dstintf": "port1",
            "set ippool": "enable",
            "set name": "policy168",
            "set nat": "enable",
            "set poolname": "ippool_jimmylin_168.100.168.11",
            "set schedule": "always",
            "set service": "ALL",
            "set srcaddr": "address__jimmylin_10.100.168.11/32",
            "set srcintf": "jimmylin__1688",
            "set uuid": "14435052-3097-4d70-98c7-1dd2d60e229f"
        },
        "edit 169": {
            "set action": "accept",
            "set comments": "\"customer\": \"Jimmy Lin\"",
            "set dstaddr": "vip__jimmylin__168.100.168.11",
            "set dstintf": "jimmylin__1688",
            "set name": "policy169",
            "set schedule": "always",
            "set service": "HTTP HTTPS RDP",
            "set srcaddr": "all",
            "set srcintf": "port1",
            "set uuid": "2d05b2f4-9968-43c0-8bfa-581e04144466"
        }
    }
}
"""

# Write
reorganize_lines = [line[0] + shlex.join(line[1:]) for line in formatted_lines]
with open(file=FILE_OUTPUT_PATH, mode='w', encoding='utf-8') as file:
    file.writelines('\n'.join(reorganize_lines))
