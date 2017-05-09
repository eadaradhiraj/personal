import mechanize, re, sys, urllib2, argparse
from bs4 import BeautifulSoup
from time import sleep

Soup = lambda htm: BeautifulSoup(htm,'html.parser')

def vodlocker(url):
	br = mechanize.Browser()
	br.addheaders = [('User-agent', 'Firefox')]
	br.set_handle_robots(False)
	br.open(url)
	filnm=Soup(br.response().read()).find("input", attrs={"type":"hidden", "name":"fname"})['value']
	br.select_form(nr=1)
	sleep(7)
	br.submit()
	html=(br.response().read())
	_dwnfil(re.search('file\: \"(.*)\"', html).group(1),filnm)

def gorillavid(url):
	br = mechanize.Browser()
	br.addheaders = [('User-agent', 'Firefox')]
	br.set_handle_robots(False)
	br.open(url)
	filnm=Soup(br.response().read()).find("input", attrs={"type":"hidden", "name":"fname"})['value']
	br.select_form(nr=1)
	sleep(7)
	br.submit()
	html=(br.response().read())
	_dwnfil(re.search('file\: \"(.*)\"', html).group(1),filnm)

def streamin(url):
	br = mechanize.Browser()
	br.addheaders = [('User-agent', 'Firefox')]
	br.set_handle_robots(False)
	br.open(url)
	filnm=Soup(br.response().read()).find("input", attrs={"type":"hidden", "name":"fname"})['value']
	br.select_form(nr=0)
	sleep(7)
	br.submit()
	html=(br.response().read())
	_dwnfil(re.search('file\:\'(.*)\',', html).group(1),filnm)

def _dwnfil(url,file_name="vid"):
	try:
		u = urllib2.urlopen(url)
		f = open(file_name, 'wb')
		meta = u.info()
		file_size = int(meta.getheaders("Content-Length")[0])
		print "Downloading: %s Bytes: %s" % (file_name, file_size)

		file_size_dl = 0
		block_sz = 8192
		while True:
			buffer = u.read(block_sz)
			if not buffer:
				break
			file_size_dl += len(buffer)
			f.write(buffer)
			status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
			status = status + chr(8)*(len(status)+1)
			print status,
		f.close()
	except KeyboardInterrupt:
		sys.exit("Interrupted!!!")
	except Exception, e:
		sys.exit("Error in download function "+str(e))

def Main():
	parser = argparse.ArgumentParser(description='Download Manager')
	parser.add_argument('url', type=str, help='URL to download')
	args = parser.parse_args()
	url = args.url
	if 'http://' not in url:
		url = 'http://'+url
	if 'vodlocker' in url:
		vodlocker(url)
	elif 'gorillavid' in url:
		gorillavid(url)
	elif 'streamin' in url:
		streamin(url)
	else:
		sys.exit("Unrecognized link!!!")

if __name__ == '__main__':
	Main()
