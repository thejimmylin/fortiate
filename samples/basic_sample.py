from base import FortiConfig
import os


# Locate the conf file with relative path by module os.
current_dir = os.path.dirname(__file__)
conf_file = os.path.join(current_dir, 'conf', 'firewall_policy.conf')

with open(file=conf_file, mode='r', encoding='utf-8') as f:
    lines = f.read().splitlines()

fc = FortiConfig(lines)
print(fc)

# This also works
# fc = FortiConfig(lines, quote_char='"')
# print(fc)
