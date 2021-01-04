#!/usr/bin/python3

import requests, json
from sys import argv

if argv[1]=='' or argv[2]=='':
    print('[-] Usage: ./subdomains-recondev.py <list of domains> <subdomains output file>\n')

query = "https://recon.dev/api/search?key=free-c78c8950-7541-40f2-a221-01111eddebb5&domain={0}"

domains = []

def extract_domains(domain):
	res = requests.get(query.format(domain))
	if res.text.strip()!="null":
		temp = json.loads(res.text)
		for i in temp:
			j = i["rawDomains"]
			for k in j:
				domains.append(k.strip())


f = open(argv[1]).readlines()

for i in f:
	try:
		if i.strip()!='':
			extract_domains(i.strip())
	except:
		print("[-] Error retrieving subdomains from recondev")

with open(argv[2],'w') as t:
	for d in domains:
		t.write(d+'\n')