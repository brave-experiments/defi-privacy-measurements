import csv
import socket
import subprocess

HOSTING_PROVIDERS = { 'Cloudflare' : [],
		      'AWS' : [],
		      'DO' : [],
		      'Google' : [],
		      'Other' : [],
		      'Unknown' : []
		    }


with open('sites_sanitized.csv', newline='') as defi_sites:
	reader = csv.reader(defi_sites, delimiter=',')

	for row in reader:
		site = row[0]
		if site == 'site':
			continue
		try:
			ip = socket.gethostbyname(site)
			sp = subprocess.Popen('whois -h whois.cymru.com " -v ' + ip + ' " ', shell=True, stdout=subprocess.PIPE)
			ret = sp.stdout.read()
			asn = ret.decode('utf-8').split('|')[-1]
			print(asn)
			if "CLOUDFLARE" in asn:
				HOSTING_PROVIDERS['Cloudflare'].append(site)
			elif 'AMAZON' in asn:
				HOSTING_PROVIDERS['AWS'].append(site)
			elif 'DIGITALOCEAN' in asn:
				HOSTING_PROVIDERS['DO'].append(site)
			
			elif 'GOOGLE' in asn:
				HOSTING_PROVIDERS['Google'].append(site)
			else:
				HOSTING_PROVIDERS['Other'].append(site)
		except Exception as e:
			HOSTING_PROVIDERS['Unknown'].append(site)
			print(site + " : " + str(e))

print('Cloudflare: ' + str(len(HOSTING_PROVIDERS['Cloudflare'])))
print('AWS: ' + str(len(HOSTING_PROVIDERS['AWS'])))
print('Google: ' + str(len(HOSTING_PROVIDERS['Google'])))
print('DO: ' + str(len(HOSTING_PROVIDERS['DO'])))
print('Other: ' + str(len(HOSTING_PROVIDERS['Other'])))
print('Unknown: ' + str(len(HOSTING_PROVIDERS['Unknown'])))
