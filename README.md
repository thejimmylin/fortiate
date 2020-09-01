# fortiate
For reading and writing config of Forti easily.

## What does fortiate do?
 What it mainly do is it turns config like this
 ```
config firewall policy
    edit 168
        set name "policy168"
        set uuid 14435052-3097-4d70-98c7-1dd2d60e229f
        set srcintf "jimmylin__1688"
        set dstintf "port1"
        set srcaddr "address__jimmylin__10.100.168.11/32"
        set dstaddr "all"
        set action accept
        set schedule "always"
        set service "ALL"
        set comments "\"customer\": \"Jimmy Lin\""
        set nat enable
        set ippool enable
        set poolname "ippool__jimmylin__168.100.168.11"
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
            "set poolname": "ippool__jimmylin__168.100.168.11",
            "set schedule": "always",
            "set service": "ALL",
            "set srcaddr": "address__jimmylin__10.100.168.11/32",
            "set srcintf": "jimmylin__1688",
            "set uuid": "14435052-3097-4d70-98c7-1dd2d60e229f"
        },
    }
}
```

## Installation

OS X & Linux:

```
python3 -m venv /Users/jimmy_lin/envs/fortiate
source /Users/jimmy_lin/envs/fortiate/bin/activate
git clone https://github.com/j3ygithub/fortiate /Users/jimmy_lin/repos/fortiate
```

Windows:

```
python -m venv C:\Users\jimmy_lin\envs\fortiate
C:\Users\jimmy_lin\envs\fortiate\Scripts\activate
git clone https://github.com/j3ygithub/fortiate C:\Users\jimmy_lin\repos\fortiate
```

## Run a basic sample

```
(fortiate) PS C:\Users\LinKeiChi\repos\fortiate\samples> python -i .\basic_sample.py
printing fc..

 config firewall policy
    edit 168
        set name 'policy 168'
        set uuid 14435052-3097-4d70-98c7-1dd2d60e229f
        set srcintf jimmylin__1688
        set dstintf port1
        set srcaddr address__jimmylin__10.100.168.11/32
        set dstaddr all
        set action accept
        set schedule always
        set service ALL
        set comments '{"customer": "Jimmy Lin", "remark": "this comment contains json"}'
        set nat enable
        set ippool enable
        set poolname ippool__jimmylin__168.100.168.11
    edit 169
        set name 'policy 169'
        set uuid 2d05b2f4-9968-43c0-8bfa-581e04144466
        set srcintf port1
        set dstintf jimmylin__1688
        set srcaddr all
        set dstaddr vip__jimmylin__168.100.168.11
        set action accept
        set schedule always
        set service HTTP HTTPS RDP
        set comments '{"customer": "Jimmy Lin", "remark": "this comment contains json"}'
    edit 170
        set name 'policy 170'
        set uuid 2d05b2f4-9968-43c0-8bfa-581e04144466
        set srcintf port1
        set dstintf jimmylin__1688
        set srcaddr all
        set dstaddr vip__jimmylin__168.100.168.11
        set action accept
        set schedule always
        set service service__tcp__8080__8080
        set comments '{"customer": "Jimmy Lin", "remark": "this comment contains json"}'
    next
end

```

**fc** is a instance of class **FortiConfig** initialized with Forti config file C:\Users\LinKeiChi\repos\fortiate\samples\conf\firewall_policy.conf

You can read/edit these data with **fc** easily

```
>>> fc
<fortiate.configs.FortiConfig object at 0x00000251E5909D30>
>>> fc.data['config firewall policy']['edit 169']['set service']
ShellCommand(['HTTP', 'HTTPS', 'RDP'])
```

**ShellCommand** is like a list of phrases, you can read/edit it easily too.

```
>>> fc.data['config firewall policy']['edit 169']['set service'][0]
'HTTP'
>>> fc.data['config firewall policy']['edit 169']['set service'][1:]
ShellCommand(['HTTPS', 'RDP'])
>>> fc.data['config firewall policy']['edit 169']['set service'].command
'HTTP HTTPS RDP'
>>> 
>>> fc.data['config firewall policy']['edit 169']['set service'] += ShellCommand('FTP')
>>> fc.data['config firewall policy']['edit 169']['set service']
ShellCommand(['HTTP', 'HTTPS', 'RDP', 'FTP'])
```

Now we have a new output of **print(fc)**
```
>>> print(fc)
>>> fc.data['config firewall policy']['edit 169']['set service'] += ShellCommand('FTP')
>>> print(fc)
config firewall policy
    edit 168
...
...
    edit 169
        set name 'policy 169'
        set uuid 2d05b2f4-9968-43c0-8bfa-581e04144466
        set srcintf port1
        set dstintf jimmylin__1688
        set srcaddr all
        set dstaddr vip__jimmylin__168.100.168.11
        set action accept
        set schedule always
        set service HTTP HTTPS RDP FTP
        set comments '{"customer": "Jimmy Lin", "remark": "this comment contains json"}'
    edit 170
...
...
end
```
See smaples.py for more detail.


## Meta

Jimmy Lin <b00502013@gmail.com>

Distributed under the MIT license. See ``LICENSE`` for more information.

[https://github.com/j3ygithub/](https://github.com/j3ygithub/)

## Contributing

1. Fork it (<https://github.com/j3ygithub/rj3y/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
