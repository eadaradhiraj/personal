from bs4 import BeautifulSoup
import urllib2, sys, re, argparse
from downmanage import *

reload(sys)
sys.setdefaultencoding('utf8')

DOM = 'http://watchseries.ag'
reg = r'Episode (\d*)'

Soup = lambda htm: BeautifulSoup(htm,'html.parser')

def _findfilehosturl(link,filehoster):
	link2filehosturl = Soup(gethtml(link)).find("a", {"title" : re.compile(filehoster)})['href']
	filehost2url = Soup(gethtml(DOM+link2filehosturl)).find("a",{"href" : re.compile(filehoster)})['href']
	return filehost2url

def download(link):
	try:
		vodlocker(_findfilehosturl(link,'vodlocker'))
	except TypeError:
		try:
			gorillavid(_findfilehosturl(link,'gorillavid'))
		except TypeError:
			try:
				streamin(_findfilehosturl(link,'streamin'))
			except TypeError:
				sys.exit("No links available!!")
	except Exception, e:
		sys.exit("Error in getfilehosturl "+str(e))

def gethtml(link):
	try:
		req = urllib2.Request(link, headers={'User-Agent' : "Magic Browser"})
		con = urllib2.urlopen(req)
		html = con.read()
		return html
	except Exception,e:
		sys.exit("Error in gethtml function "+str(e))

def getlistofeps(ser,seas, ep):
	url = DOM+'/serie/'+ser
	soup = Soup(gethtml(url))
	episodes = dict()
	i = 1
	for ul in soup.findAll('ul',attrs={"class":"listings episodeListings"}):
		for a in ul.findAll('a', attrs={"class":"watchEpisodeLink p1"}):
			episodes[(i,int(re.search(reg,a['title']).group(1)))]=DOM+a['href']
		i += 1
	try: return episodes[(seas,ep)]
	except KeyError: sys.exit("Episode doesn't exist!!")
	except Exception,e: sys.exit("Error in getlistofpes function: "+str(e))

def _Main():
	parser = argparse.ArgumentParser(description='Download videos from Watchseries')
	parser.add_argument('show', type=str, help='Exact name of series as it appears in the watchseries full text querying')
	parser.add_argument('s_num', type=int, help='Number of season')
	parser.add_argument('ep_num', type=int, help='Number of Episode')
	args = parser.parse_args()

	eplink = getlistofeps(args.show,args.s_num,args.ep_num)
	download(eplink)

if __name__ == '__main__':
	_Main()
