import csv
import socket
import subprocess
from urllib.parse import urlparse

HOSTING_PROVIDERS = { 'Cloudflare' : [],
		      'AWS' : [],
		      'DO' : [],
		      'Fastly' : [],
		      'Google' : [],
		      'Other' : [],
		      'Unknown' : []
		    }


with open('defi-sites.csv', newline='') as defi_sites:
	reader = csv.reader(defi_sites, delimiter=',')
	
	data_csv = open('hosting_provider_data.csv', 'w', newline='')
	fieldnames = ['site', 'provider']
	writer = csv.DictWriter(data_csv, fieldnames=fieldnames)
	writer.writeheader()
  
	for row in reader:
		site = row[0]
		if site == 'site':
			continue
		try:
			ip = socket.gethostbyname(urlparse(site).netloc)
			sp = subprocess.Popen('whois -h whois.cymru.com " -v ' + ip + ' " ', shell=True, stdout=subprocess.PIPE)
			ret = sp.stdout.read()
			asn = ret.decode('utf-8').split('|')[-1]
			if "CLOUDFLARE" in asn:
				writer.writerow({'site': site, 'provider': 'cloudflare'})
				HOSTING_PROVIDERS['Cloudflare'].append(site)
			elif 'AMAZON' in asn:
				writer.writerow({'site': site, 'provider': 'aws'})
				HOSTING_PROVIDERS['AWS'].append(site)
			elif 'DIGITALOCEAN' in asn:
				writer.writerow({'site': site, 'provider': 'digital ocean'})
				HOSTING_PROVIDERS['DO'].append(site)
			
			elif 'GOOGLE' in asn:
				HOSTING_PROVIDERS['Google'].append(site)
				writer.writerow({'site': site, 'provider': 'google'})
			elif 'FASTLY' in asn:
				HOSTING_PROVIDERS['Fastly'].append(site)
				writer.writerow({'site': site, 'provider': 'fastly'})
			else:
				HOSTING_PROVIDERS['Other'].append(site)
				writer.writerow({'site': site, 'provider': 'other'})
				print(asn)
		except Exception as e:
			HOSTING_PROVIDERS['Unknown'].append(site)
			writer.writerow({'site': site, 'provider': 'unknown'})

print('Cloudflare: ' + str(len(HOSTING_PROVIDERS['Cloudflare'])))
print('AWS: ' + str(len(HOSTING_PROVIDERS['AWS'])))
print('Google: ' + str(len(HOSTING_PROVIDERS['Google'])))
print('Fastly: ' + str(len(HOSTING_PROVIDERS['Fastly'])))
print('DO: ' + str(len(HOSTING_PROVIDERS['DO'])))
print('Other: ' + str(len(HOSTING_PROVIDERS['Other'])))
print('Unknown: ' + str(len(HOSTING_PROVIDERS['Unknown'])))
