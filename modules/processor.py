import os
import subprocess

class processorNeedsMoreInfo(Exception):
	"""Exception handling for processor"""
	pass

class processor(object):
	"""Provides an instance for processor class"""

	# file containing list of domains
	filename = None
	#Target's friendly name
	targetname = None
	#Whether to perform port scanning
	portscan = False
	extra_ips = []

	#command to execute depends upon run argument
	command = ""
	run = ""

	#Cusotmize to include other modules
	available_runs = ["subdomains","resolver","probeNtakeover","jsmagic","endpoints","dirfuzz","favfreak","cvescan","portscan","bugs","brutespray"]

	#Command Templates
	command_subdomains = "interlace -t {0} -o {1} -cL ./core/templates/subs.config --no-bar "
	command_resolver = "interlace -t {0} -cL ./core/templates/resolver.config --no-bar"
	command_probeNtakeover = "interlace -t {0} -cL ./core/templates/probeNtakeover.config --no-bar"
	command_jsmagic = "interlace -tL results/{0}/weburls.txt -cL ./core/templates/jsmagic.config --no-bar -threads 100 -o results/{0}/javascript"
	command_endpoints = "echo python2 modules/endpoint-extractor.py -u {0} -t {1}"
	command_dirfuzz = "echo interlace -t {0} -cL ./core/templates/dirfuzz.config --no-bar -threads 3 -o {1}"
	command_favfreak = "cat results/{0}/weburls.txt |python3 database/tools/FavFreak/favfreak.py | tee results/{0}/favfreak.txt"
	command_cvescan = "nuclei -l results/{0}/weburls.txt -t cves/ -o results/{0}/cvescan.txt"
	command_portscan = "masscan -p 0-65535 --rate 1000 -Pn -iL results/{0}/resolver/ips.txt | tee results/{0}/portscan/masscan.txt"
	command_bugs = "interlace -tL results/{0}/subdomains/subdomains-resolvable.txt -cL ./core/templates/bugs2.config --no-bar -threads 100 -o results/{0}/bugs"
	command_brutespray = "brutespray -f results/{0}/portscan/nmap.txt -o results/{0}/brutespray -t 100"


	def configure(self,run=None):

		if run ==None:
			raise processorNeedsMoreInfo("\n[!] Please specify run argument")

		if run not in self.available_runs:
			raise processorNeedsMoreInfo("\n[!] Please specify a valid value for run : " + str(self.available_runs))

		self.run = run
		self.validate()

	def validateTarget(self):
		if self.targetname==None or self.targetname=="":
			raise processorNeedsMoreInfo("[-] Please specify the valid value for targetname")

	def FileExists(self,filepath):
		if not os.path.isfile(filepath):
			raise processorNeedsMoreInfo("[!] File does not exist : {0}".format(filepath))

	def ExecuteCommand(self,cmd):
		subprocess.run(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

	def validateSubdomains(self):
		
		if self.filename==None:
			raise processorNeedsMoreInfo("[-] Please specify the valid value for filename")
		self.validateTarget()
		self.FileExists(self.filename)

	def validateResolver(self):

		self.validateTarget()
		self.FileExists("results/{0}/subdomains/subdomains-combined.txt".format(self.targetname))

	def validateprobeNtakeover(self):
		self.validateTarget()
		self.FileExists("results/{0}/subdomains/subdomains-resolvable.txt".format(self.targetname))

	def validateJsmagic(self):
		self.validateTarget()
		self.FileExists("results/{0}/weburls.txt".format(self.targetname))

	def validate(self):

		#Change to modules parent directory path
		file_directory = os.path.dirname(os.path.realpath(__file__)) 
		os.chdir(os.path.join(file_directory,'../'))

		#Validate subdomains settings
		if self.run == "subdomains":
			self.command = self.command_subdomains.format(self.filename,self.targetname)
			self.validateSubdomains()

		#Validate setitings for resolver
		if self.run=="resolver":
			self.command = self.command_resolver.format(self.targetname)
			self.validateResolver()

		#Validate settings for httprobe and takeovers
		if self.run == "probeNtakeover":
			self.command = self.command_probeNtakeover.format(self.targetname)
			self.validateprobeNtakeover()

		#Validate settings for downloading js files and storing urls
		if self.run == "jsmagic":
			self.command = self.command_jsmagic.format(self.targetname)
			self.validateJsmagic()

		if self.run == "endpoints":
			self.command = self.command_endpoints.format("TARGET_URL",self.targetname)
			self.validateJsmagic()  #has same requirements as jsmagic

		if self.run == "dirfuzz":
			self.command = self.command_dirfuzz.format("TARGET_URL",self.targetname)
			self.validateJsmagic()	#same requirement as jsmagic

		if self.run == "favfreak":
			self.command = self.command_favfreak.format(self.targetname)
			self.validateJsmagic()  #same requirement as jsmagic

		if self.run == "cvescan":
			self.command = self.command_cvescan.format(self.targetname)
			self.validateJsmagic()  #same requirement as jsmagic

		if self.run == "portscan":
			if self.portscan == True:
				self.command = self.command_portscan.format(self.targetname)
				self.FileExists("results/{0}/resolver/ips.txt".format(self.targetname))
			else:
				self.command = ''

		if self.run == "bugs":
			self.command = "echo [+] Running Bugs Module"
			self.FileExists("results/{0}/subdomains/subdomains-resolvable.txt".format(self.	targetname))

		if self.run == "brutespray":
			self.command = self.command_brutespray.format(self.targetname)
			self.FileExists("results/{0}/portscan/nmap.txt".format(self.targetname))

	def afterRunSubdomains(self):

		print("[+] Combining output of all tools from subdomain scan")
		ouput_path = "results/{0}/subdomains".format(self.targetname)
		combine_results = 'sort -u {0}/*.txt |sed  "/^[\\.*]/d" |sed "s/\\.$//"|sort -u > {0}/subdomains-combined.txt'.format(ouput_path)
		self.ExecuteCommand(combine_results)

	def afterRunResolver(self):

		ouput_path = "results/{0}/resolver".format(self.targetname)
		subprocess.run("sort -u {0}/massdns.txt | grep -i cname > {0}/cnames.txt".format(ouput_path),shell=True)
		subprocess.run("sort -u {0}/massdns.txt | grep -iv cname |cut -d ' ' -f 3|sort -u > {0}/ips.txt".format(ouput_path),shell=True)
		subprocess.run("sort -u {0}/massdns.txt |cut -d ' ' -f 1|sed 's/\\.$//'|sort -u > {0}/../subdomains/subdomains-resolvable.txt".format(ouput_path),shell=True)

	def afterRunEndpoints(self):

		weburls = open('results/{0}/weburls.txt'.format(self.targetname)).readlines()
		for url in weburls:
			cmd = "python2 modules/endpoint-extractor.py -u {0} -t {1}".format(url.strip(),self.targetname)
			self.ExecuteCommand(cmd)

		cmd_burl = "cat results/{0}/stko/urls.txt |burl |tee results/{0}/stko/broken-urls.txt".format(self.targetname)
		self.ExecuteCommand(cmd_burl)
			
	def afterRunProbeNtakeover(self):

		with open("results/{0}/weburls_temp.txt".format(self.targetname)) as f:
			urls = f.readlines()

			for url in urls:
				if url.strip() == '':
					continue
				domain = url.split(':')[1][2:]
				if 'http://{0}:80\n'.format(domain) in urls and 'https://{0}:443\n'.format(domain) in urls:
					urls.remove('http://{0}:80\n'.format(domain))
		with open("results/{0}/weburls.txt".format(self.targetname),'w') as f:
			f.write(''.join(urls))

	def afterRunDirfuzz(self):

		urls = open('results/{0}/weburls.txt'.format(self.targetname)).readlines()

		#create batch of 10 urls to execute at a time
		for i in range(0,len(urls),10):

			print("[+] dirfuzz procesing batch of 10 urls : batch {0}".format(str(i)))
			tmpfile = "results/{0}/.temp".format(self.targetname)
			f = open(tmpfile,'w')

			#Place upto 10 urls in .temp file
			for url in urls[i:i+10]:
				if url.strip() != '':
					f.write(url.strip() + '\n')

			f.close()
			cmd = "interlace -tL {0} -cL ./core/templates/dirfuzz.config --no-bar -threads 15 -o {1}".format(tmpfile,self.targetname)
			self.ExecuteCommand(cmd)

	def beforeRunPortScan(self):
		self.ExecuteCommand("mkdir -p results/{0}/portscan".format(self.targetname))

		with open('results/{0}/resolver/ips.txt'.format(self.targetname),'a') as f:
			for i in self.extra_ips:
				f.write('\n'+i.strip())

	def afterRunPortscan(self):
		self.ExecuteCommand("sudo nmap --script-updatedb")

		self.ExecuteCommand("database/tools/scripts/nmap_scan.py results/{0}/portscan/masscan.txt results/{0}/portscan/nmap.txt".format(self.targetname))

	def findBugs(self):
		#gf redirects and ssrf
		self.ExecuteCommand(self.command_bugs.format(self.targetname))

		#gf commands
		gf_command = "cd results/{0}/ && gf {1} >> bugs/{1}.txt && cd ../../"

		self.ExecuteCommand(gf_command.format(self.targetname,"aws-keys"))
		self.ExecuteCommand(gf_command.format(self.targetname,"gcm-keys"))
		self.ExecuteCommand(gf_command.format(self.targetname,"s3-buckets"))
		self.ExecuteCommand(gf_command.format(self.targetname,"cors"))

		for i in range(1,6):
			self.ExecuteCommand(gf_command.format(self.targetname,"credentials"+str(i)))

	def afterRunBugs(self):
		self.ExecuteCommand("cp ./database/gfPatterns/* ~/.gf/")

		self.ExecuteCommand("mkdir -p results/{0}/bugs/gau".format(self.targetname))
		self.ExecuteCommand("mkdir -p results/{0}/bugs/redirects".format(self.targetname))
		self.ExecuteCommand("mkdir -p results/{0}/bugs/ssrf".format(self.targetname))

		urls = open('results/{0}/subdomains/subdomains-resolvable.txt'.format(self.targetname)).readlines()

		#create batch of 10 urls to execute at a time
		for i in range(0,len(urls),10):

			tmpfile = "results/{0}/.temp_bugs".format(self.targetname)
			f = open(tmpfile,'w')

			#Place upto 10 urls in .temp_bugs file
			for url in urls[i:i+10]:
				if url.strip() != '':
					f.write(url.strip() + '\n')

			f.close()
			cmd = "interlace -tL {0} -cL ./core/templates/bugs.config --no-bar -threads 10 -o results/{1}/bugs".format(tmpfile,self.targetname)
			self.ExecuteCommand(cmd)
			self.findBugs()
			self.ExecuteCommand('rm results/{0}/bugs/gau/*'.format(self.targetname))

	def beforeRun(self):

		if self.run == "subdomains":
			print("Extracting subdomains from recondev api")
			self.ExecuteCommand("mkdir -p results/{0}/subdomains".format(self.targetname))
			self.ExecuteCommand("./database/tools/scripts/subdomains-recondev.py {0} results/{1}/subdomains/recondev.txt".format(self.filename,self.targetname))

		if self.run == "resolver":
			self.ExecuteCommand("mkdir -p results/{0}/resolver".format(self.targetname))

		if self.run == "probeNtakeover":
			self.ExecuteCommand("mkdir -p results/{0}/takeover".format(self.targetname))

		if self.run == "dirfuzz":
			self.ExecuteCommand("mkdir -p results/{0}/dirfuzz/".format(self.targetname))

		if self.run == "cvescan":
			self.ExecuteCommand("nuclei -update-templates")

		if self.run == "portscan" and self.portscan == True:
			self.beforeRunPortScan()

	def afterRun(self):

		#Combine output of all tools from subs.config --> subdomain enumeration
		if self.run=="subdomains":
			self.afterRunSubdomains()

		#Create ips.txt, cnames.txt and subdomains-resolvable.txt from massdns output
		if self.run == "resolver":
			self.afterRunResolver()

		#Made endoint-extractor single threaded
		if self.run == "endpoints":
			self.afterRunEndpoints()

		#Sed remove dot at the end of urls and empty lines
		if self.run == "probeNtakeover":
			self.afterRunProbeNtakeover()


		#Run dirfuzz per target basis
		if self.run == "dirfuzz":
			self.afterRunDirfuzz()

		#Run nmap afer masscan finishes
		if self.run == "portscan" and self.portscan==True:
			self.afterRunPortscan()

		if self.run == "bugs":
			self.afterRunBugs()

	def process(self):

		self.beforeRun()
		print("[+] Running Command : " + self.command)
		self.ExecuteCommand(self.command)
		try:
			self.afterRun()
		except:
			print("[-] Unable to perform after run operations")
