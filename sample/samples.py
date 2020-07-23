import os
import json
from ..fortiate.parsers import Parser


BASE_DIR = os.path.dirname(__file__)
FILE_INPUT_PATH = os.path.join(BASE_DIR, 'conf', 'firewall policy.conf')
FILE_OUTPUT_PATH = os.path.join(BASE_DIR, 'conf', 'firewall policy output.conf')

p = Parser()
with open(file=FILE_INPUT_PATH, mode='r', encoding='utf-8') as f:
    lines = f.readlines()

formatted_lines = p.get_formatted_lines(lines=lines)
formatted_dct = p.get_formatted_dct(formatted_lines=formatted_lines)

print('------ start ------')
print(json.dumps(obj=formatted_dct, sort_keys=True, indent=4))
print('------ end ------')

reorganize_lines = p.get_reorganize_lines(formatted_lines=formatted_lines)
with open(file=FILE_OUTPUT_PATH, mode='w', encoding='utf-8') as file:
    file.writelines('\n'.join(reorganize_lines))
