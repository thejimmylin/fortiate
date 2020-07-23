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

## Installation & Run examples
```
cd /your/repos/path
mkdir fortiate
cd fortiate
python3 -m venv venv 
source ./venv/bin/activate
git clone https://github.com/j3ygithub/fortiate
cd fortigate
python parser.py
```
