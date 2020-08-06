from base import FortiSetCommand


fsc1 = FortiSetCommand("set service HTTP HTTPS RDP 'set service tcp 8080-8080 udp 0-0'\n")
fsc2 = FortiSetCommand()
fsc2.cleaned_data
