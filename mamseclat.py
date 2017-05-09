from bs4 import BeautifulSoup
import urllib2, re
from downmanage import *

def gethtml(link):
	req = urllib2.Request(link, headers={'User-Agent' : "Magic Browser"})
	con = urllib2.urlopen(req)
	html = con.read()
	return html

def findLatest():

	url = "http://watchseries.ag/serie/Madam_Secretary"
	head = "http://watchseries.ag"

	soup = BeautifulSoup(gethtml(url), 'html.parser')
	latep=soup.find("b", text = 'Latest Episode With Links: ').parent.parent.findAll('a')[-6]

	soup = BeautifulSoup(gethtml(head+latep['href']), 'html.parser')
	firstVod = soup.find("a", {"title" : "vodlocker.com"})

	soup = BeautifulSoup(gethtml(head+firstVod['href']), 'html.parser')
	firstVod = soup.find("a",{"href" : re.compile("vodlocker")})['href']
	return firstVod

if __name__ == '__main__':
	vodlocker(findLatest())
	#print findLatest()
