import sys
import os
import json
"""
In case fortiate is not installed as a package, we add it to sys.path manually here.
If you install fortiate and added it to the $PYTHONPATH, this could be skipped.
"""
fortiate_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'fortiate'
)
sys.path.insert(1, fortiate_path)
from parsers import Parser  # noqa


BASE_DIR = os.path.dirname(__file__)
FILE_INPUT = os.path.join(BASE_DIR, 'conf', 'firewall policy.conf')
FILE_OUTPUT = os.path.join(BASE_DIR, 'conf', 'firewall policy output.conf')

p = Parser()
with open(file=FILE_INPUT, mode='r', encoding='utf-8') as f:
    lines = f.readlines()

formatted_lines = p.get_formatted_lines(lines=lines)
formatted_dct = p.get_formatted_dct(formatted_lines=formatted_lines)

print(json.dumps(obj=formatted_dct, sort_keys=True, indent=4))

reorganize_lines = p.get_reorganize_lines(formatted_lines=formatted_lines)
with open(file=FILE_OUTPUT, mode='w', encoding='utf-8') as file:
    file.writelines('\n'.join(reorganize_lines))
