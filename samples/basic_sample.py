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


base_dir = os.path.dirname(__file__)
file_input = os.path.join(base_dir, 'conf', 'firewall policy.conf')
file_output = os.path.join(base_dir, 'conf', 'firewall policy output.conf')

p = Parser()
with open(file=file_input, mode='r', encoding='utf-8') as f:
    lines = f.readlines()

formatted_lines = p.get_formatted_lines(lines=lines)
formatted_dct = p.get_formatted_dct(formatted_lines=formatted_lines)

print(json.dumps(obj=formatted_dct, sort_keys=True, indent=4))

reorganize_lines = p.get_reorganize_lines(formatted_lines=formatted_lines)
with open(file=file_output, mode='w', encoding='utf-8') as file:
    file.writelines('\n'.join(reorganize_lines))
