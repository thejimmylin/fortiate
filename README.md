# fortiate
 For reading and writing config of Forti.

## What does fortiate do?
 It turns config like this
 ```
 config firewall policy
    edit 168
        set name "policy168"
        set uuid 14435052-3097-4d70-98c7-1dd2d60e229f
        set srcintf "jimmylin__1688"
        set dstintf "port1"
        set srcaddr "address__jimmylin_10.100.168.11/32"
        set dstaddr "all"
        set action accept
        set schedule "always"
        set service "ALL"
        set comments "\"customer\": \"Jimmy Lin\""
        set nat enable
        set ippool enable
        set poolname "ippool_jimmylin_168.100.168.11"
    next
end
```
to this
```
{
    "config firewall policy": {
        "edit 168": {
            "set action": "accept",
            "set comments": "\"customer\": \"Jimmy Lin\"",
            "set dstaddr": "all",
            "set dstintf": "port1",
            "set ippool": "enable",
            "set name": "policy168",
            "set nat": "enable",
            "set poolname": "ippool_jimmylin_168.100.168.11",
            "set schedule": "always",
            "set service": "ALL",
            "set srcaddr": "address__jimmylin_10.100.168.11/32",
            "set srcintf": "jimmylin__1688",
            "set uuid": "14435052-3097-4d70-98c7-1dd2d60e229f"
        },
    }
}
```
You can edit data on this dictionary-like object and turn it back.

## Installation & Run samples
```
cd /your/repos/path
mkdir fortiate
cd fortiate
python3 -m venv venv 
source ./venv/bin/activate
git clone https://github.com/j3ygithub/fortiate
cd fortigate
python samples.py
```

You should see something like this.
```
------ start ------
{
    "config firewall policy": {
        "edit 168": {
            "set action": "accept",
            "set comments": "\"customer\": \"Jimmy Lin\"",
            "set dstaddr": "all",
            "set dstintf": "port1",
            "set ippool": "enable",
            "set name": "policy168",
            "set nat": "enable",
            "set poolname": "ippool_jimmylin_168.100.168.11",
            "set schedule": "always",
            "set service": "ALL",
            "set srcaddr": "address__jimmylin_10.100.168.11/32",
            "set srcintf": "jimmylin__1688",
            "set uuid": "14435052-3097-4d70-98c7-1dd2d60e229f"
        },
        "edit 169": {
            "set action": "accept",
            "set comments": "\"customer\": \"Jimmy Lin\"",
            "set dstaddr": "vip__jimmylin__168.100.168.11",
            "set dstintf": "jimmylin__1688",
            "set name": "policy169",
            "set schedule": "always",
            "set service": "HTTP HTTPS RDP",
            "set srcaddr": "all",
            "set srcintf": "port1",
            "set uuid": "2d05b2f4-9968-43c0-8bfa-581e04144466"
        },
        "edit 170": {
            "set action": "accept",
            "set comments": "\"customer\": \"Jimmy Lin\"",
            "set dstaddr": "vip__jimmylin__168.100.168.11",
            "set dstintf": "jimmylin__1688",
            "set name": "policy170",
            "set schedule": "always",
            "set service": "service__tcp__8080_8080 a service name with spaces",
            "set srcaddr": "all",
            "set srcintf": "port1",
            "set uuid": "2d05b2f4-9968-43c0-8bfa-581e04144466"
        }
    }
}
------ end ------
```

See smaples.py for more detail.
