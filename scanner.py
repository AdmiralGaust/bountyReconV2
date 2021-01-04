#!/usr/bin/python3

from modules import processor
import subprocess
from modules import slacker


# Friendly name of your target. Eg- uber
target = "example"

# File containing list of top level domains
filename="domains.txt"

# Perform port scanning
portscan=True

#Extra ips or ranges for scan, portscan must be set to true
extra_ips = []	#Strings - CIDR Supported

# Slack Channel name to recieve notifications
channel="general"

# Configure which modules to run
runs = ["subdomains","resolver","probeNtakeover","jsmagic","endpoints","cvescan","favfreak","bugs","dirfuzz","portscan","brutespray"]

# remember to configure slack api token in slacker.py
SlackClient = slacker.SlackClient()   


def notify(msg):
	SlackClient.sendMessage(msg,channel=channel)

# Configuring 
p = processor.processor()
p.targetname = target
p.filename = filename
p.portscan = portscan
p.extra_ips = extra_ips


for run in runs:
	p.configure(run=run)
	notify("{0} started for {1}".format(run,target))
	p.process()
	notify("{0} finished for {1}".format(run,target))

