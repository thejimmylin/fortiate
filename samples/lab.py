import os
from collections import OrderedDict
from base import ShellCommand


current_dir = os.path.dirname(__file__)
conf_file = os.path.join(current_dir, 'conf', 'firewall_policy.conf')
with open(file=conf_file, mode='r', encoding='utf-8') as f:
    lines = f.read().splitlines()


for line in lines:
    sc = ShellCommand(line, quote_char="'", check_consistency=False)
    sc.midset = sc.midset
    print(sc.midset)
    print(sc.mid)

# uuid = ShellCommand()
# uuid.midset = ['set', 'uuid', '35da4ce3-9dd8-494f-8525-024e0e501211']
# extip = FortiSetCommand()
# extip.midset = ['set', 'extip', '168.100.168.11']
# extintf = FortiSetCommand()
# extintf.midset = ['set', 'extintf', 'port1']
# mappedip = FortiSetCommand()
# mappedip.midset = ['set', 'mappedip', '10.100.168.11']

# commands = [uuid, extip, extintf, mappedip]
# context = OrderedDict()
# for command in commands:
#     if command.is_valid():
#         context.update(command.cleaned_data)
