## Flow Architecture

* subs take list of domains and produces
  1. results/_target_/subdomains/subfinder.txt
  2. results/_target_/subdomains/subdomains-combined.txt

* resolver takes subdomains/subdomains-combined.txt and produces
  1. results/_target_/subdomains/subdomains-resolvable.txt
  2. results/_target_/resolver/cnames.txt
  3. results/_target_/resolver/ips.txt

* probeNtakeover takes subdomains-resolvable.txt and produces
  1. results/_target_/weburls.txt
  2. results/_target_/takeover/subjack.txt
  3. results/_target_/takeover/subover.txt

* jsmagic takes results/_target_/weburls.txt and produces
  1. results/_target_/javascript
  2. results/_target_/javascript/http_example_com/*.js
  3. results/_target_/javascript/http_example_com/javascript_urls.txt

* endpoints takes results/_target_/weburls.txt and produces
  1. results/_target_/javascript/endpoints.txt
  2. Also produce results/_target_/stko/ folder - burl input for checking second level takeover

* dirfuzz takes results/_target_/weburls.txt and produces
  1. results/_target_/dirfuzz
  2. results/_target_/dirfuzz/backupFiles.txt
  3. results/_target_/dirfuzz/http_domain_com_endpoints.txt
  4. results/_target_/dirfuzz/http_example_com_content.txt

* favfreak takes results/_target_/weburls.txt and produces 
  1. results/_target_/favfreak.txt
  2. This file contains all the technology found using favicon hashes
