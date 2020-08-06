from base import FortiSetCommand

fsc = FortiSetCommand("set service HTTP HTTPS RDP 'set service tcp 8080-8080 udp 0-0'\n")
