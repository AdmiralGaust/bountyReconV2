#!/usr/bin/python3

import re,os
from sys import argv

if argv[1]=='' or argv[2]=='':
    print('[-] Usage: ./nmap_scan.py <output_from_masscan> <filename_to_output>\n')

nmap_command = "nmap -sV -Pn -oG {out} --append-output --script vulners -p {port} {ip}"

f = open(argv[1]).readlines()

for i in f:
    if i.startswith('Discovered'):
        port = re.search('(\d*)\/tcp',i).group(1)
        ip = re.search('on ([\d\.]*)',i).group(1)
        os.system(nmap_command.format(ip=ip,port=port,out=argv[2]))
