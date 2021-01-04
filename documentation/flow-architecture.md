## Flow Architecture

* subs take list of domains and produces
** results/_target_/subdomains/amass.txt
** results/_target_/subdomains/subfinder.txt
** results/_target_/subdomains/subdomains-combined.txt

* resolver takes subdomains/subdomains-combined.txt and produces
** results/_target_/subdomains/subdomains-resolvable.txt
** results/_target_/resolver/cnames.txt
** results/_target_/resolver/ips.txt

* probeNtakeover takes subdomains-resolvable.txt and produces
** results/_target_/weburls.txt
** results/_target_/takeover/subjack.txt
** results/_target_/takeover/subover.txt

* jsmagic takes results/_target_/weburls.txt and produces
** results/_target_/javascript
** results/_target_/javascript/http_example_com/*.js
** results/_target_/javascript/http_example_com/javascript_urls.txt
***

* endpoints takes results/_target_/weburls.txt and produces
** results/_target_/javascript/endpoints.txt
** Also produce results/_target_/stko/ folder - burl input for checking second level takeover

* dirfuzz takes results/_target_/weburls.txt and produces
** results/_target_/dirfuzz
** results/_target_/dirfuzz/backupFiles.txt
** results/_target_/dirfuzz/http_domain_com_endpoints.txt
** results/_target_/dirfuzz/http_example_com_content.txt

* favfreak takes results/_target_/weburls.txt and produces 
** results/_target_/favfreak.txt
** This file contains all the technology found using favicon hashes