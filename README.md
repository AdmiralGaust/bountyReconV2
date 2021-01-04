## bountyRecon v2

Bounty Recon is a framework built on top of many open source tools to facilitate automation of reconnaissance for active bug bounties. It is designed to cover maximum scope without requiring manual efforts or intervention.

It combines a lot of great open source tools including but not limited to interlace, subfinder, massdns, httpx, nuclei, masscan, nmap, and many others. The complete list of tools in use can be found [here](documentation/dependencies.md).

## Requirements

```
Go 1.14+ must be installed
$GOPATH/bin must be in $PATH 
python 3.6 and above 		as python3 in $PATH
python 2.7 			as python2 in $PATH
```

## Installation

```
git clone https://github.com/AdmiralGaust/bountyReconv2
cd bountyReconv2/documentation/

# install all tools and dependencies
sudo ./install-dependencies.sh
```

## Post-installation Instructions

* Edit the $HOME/.config/subfinder/config.yaml file to include API keys

* Verify all depedencies are installed and are in $PATH except for massdns which is included with the framework

* Make sure massdns included with framework is working properly in database/tools/massdns/ directory. If not, make the binary locally and copy it to the same location.


## Configuring SlackClient to recieve slack notificaions

* Create a slack bot and allow it to post messages to your slack channel
* Edit the modules/slacker.py to include bot's slack token

```
#Place your token here
token = ''
```

## Introduction to the modules

There are few modules which depends on output of previous module and cannot run independently. For eg; `resolver` depends on `subdomains` module for getting list of resolvable subdomains.

More information on modules and their functioning can be found [here](documentation/flow-architecture.md).

## Configuring the Scan

A sample scanner.py file is included with the framework. Edit the file and make required changes according to the target you are scanning.

```
# Specify friendly name of your target. Results of scan will be stored in results/target folder.
target = "example"

# Provide filepath containing list of top level domains
filename="domains.txt"

# Specify whether to perform port scanning for resolved hostnames or not
portscan=True

# Extra ips or ranges for scan, portscan must be set to true for this to work
extra_ips = []	#Strings - CIDR Supported

# Configure which modules to run
runs = ["subdomains","resolver","probeNtakeover","jsmagic","endpoints","cvescan","favfreak","bugs","dirfuzz","portscan","brutespray"]
```

## Scannnig the Target

Once you have installed all the dependencies and  configured all the details in scanner.py, you can launch the scan using python3.

```
python3 scanner.py
```

You may configure scanner to launch all modules or specific modules depending on the requirements. In case, the scan was aborted due to any reason, it can be restarted from the last module aborted. However, you need to manually remove completed modules from list `runs[]` in scanner.py. 

## Warning

If you are running on VPS and are limited with disk space, avoid using the bugs module. It produces a lot of output and may fill your entire disk.

## Support

If you have any improvement advice or suggestions, feel free to create an issue or submit a pull request.
