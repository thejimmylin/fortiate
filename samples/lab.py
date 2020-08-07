from base import FortiSetCommand, FortiEditCommand, FortiConfigCommand


# test2 - build a simple config with multiple commands instance
# instance come from list instead of string
"""
config firewall vip
    edit "vip__jimmylin__168.100.168.11"
        set uuid 35da4ce3-9dd8-494f-8525-024e0e501211
        set extip 168.100.168.11
        set extintf "port1"
        set mappedip "10.100.168.11"
    next
end
"""

uuid = FortiSetCommand()
uuid.midset = ['set', 'uuid', '35da4ce3-9dd8-494f-8525-024e0e501211']
extip = FortiSetCommand()
extip.midset = ['set', 'extip', '168.100.168.11']
extintf = FortiSetCommand()
extintf.midset = ['set', 'extintf', 'port1']
mappedip = FortiSetCommand()
mappedip.midset = ['set', 'mappedip', '10.100.168.11']

commands = [uuid, extip, extintf, mappedip]
context = {}
for command in commands:
    if command.is_valid():
        context.update(command.cleaned_data)
