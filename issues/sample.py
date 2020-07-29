from shlex import split as shlex_split
from shlex import join as shlex_join


with open(file='firewall_policy.conf', mode='r', encoding='utf-8') as f:
    lines = f.read().splitlines()


def parse1(string):
    return string.split()


def parse2(string):
    return shlex_split(string)


def parse3(string):
    return shlex_split(string, posix=False)


comment = 'Start'
print('\n' + '-' * 80 + '\n' + comment + '\n' + '-' * 80 + '\n')

print(parse1(lines[2]))
comment = 'This is obviously not what we need.'
print('\n' + '-' * 80 + '\n' + comment + '\n' + '-' * 80 + '\n')

print(parse2(lines[2]))
comment = 'This is better, but the quotes missed.'
print('\n' + '-' * 80 + '\n' + comment + '\n' + '-' * 80 + '\n')

print(parse3(lines[10]))
comment = 'This is great, but it does not work on lines[11]'
print('\n' + '-' * 80 + '\n' + comment + '\n' + '-' * 80 + '\n')

print(parse3(lines[11]))
comment = 'On lines[11] it would be like the beyond.'
print('\n' + '-' * 80 + '\n' + comment + '\n' + '-' * 80 + '\n')
