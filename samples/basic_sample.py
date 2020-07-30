import sys
import os
"""
In case fortiate is not installed as a package, we add it to sys.path manually here.
If you install fortiate and added it to the $PYTHONPATH, this could be skipped.
"""
fortiate_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'fortiate'
)
sys.path.insert(1, fortiate_path)
"""
The above sys things could be skipped if you add fortiate to the $PYTHONPATH.
"""
from commands import shlex_join, IndentedShellCommand  # noqa


current_dir = os.path.dirname(__file__)
file = os.path.join(current_dir, 'conf', 'firewall_policy.conf')
with open(file=file, mode='r', encoding='utf-8') as f:
    lines = f.read().splitlines()

for line in lines:
    isc = IndentedShellCommand(raw=line)
    print(isc.split_command)

for line in lines:
    print(isc.raw)
