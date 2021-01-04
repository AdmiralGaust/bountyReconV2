cd ../
sudo pip3 install -r requirements.txt
cd database/tools
git clone https://github.com/codingo/Interlace
cd Interlace
sudo python3 setup.py install
cd ../../../
GO111MODULE=on go get -u -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder
export GO111MODULE=on
go get -u github.com/tomnomnom/httprobe
GO111MODULE=auto go get -u -v github.com/projectdiscovery/httpx/cmd/httpx
go get github.com/haccer/subjack
go get github.com/Ice3man543/SubOver
go get github.com/003random/getJS
cd database/tools/bfac
sudo python3 setup.py install
cd ../../../
go get github.com/ffuf/ffuf
python3 -m pip install mmh3
go get github.com/tomnomnom/burl
> GO111MODULE=on go get -u -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei
sudo apt-get install masscan
sudo chmod 4755 /usr/bin/masscan
sudo apt-get install nmap
GO111MODULE=on go get -u -v github.com/lc/gau
go get -u github.com/tomnomnom/gf
sudo apt-get install brutespray
