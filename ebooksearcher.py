#!/usr/bin/python
# -*- coding: utf-8 -*-

# Lit of libraries needed to run the programme
import urllib2, time, sys, os
from bs4 import BeautifulSoup
from google import search


# lambda function to create a soup from the html source
def Soup(htm):
    return BeautifulSoup(htm, 'html.parser')

# The following function downloas the file using http protocol
def _dwnfil(url, file_name="ebook"):
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
        status = status + chr(8) * (len(status) + 1)
        print status,
    f.close()


# The following acquires the html source code using urllib2
def gethtml(url):
    time.sleep(2)
    req = urllib2.Request(url, headers={'User-Agent': "Magic Browser"})
    con = urllib2.urlopen(req)
    html = con.read()
    return html

# Seaching for each ebook using google and finding for suitable links and downloadingt those found
def ebooksearch(ebook_name):

    print('Looking for ebook: ' + ebook_name)

    if not os.path.exists(ebook_name):
        os.makedirs(ebook_name)

    for url in search(query=ebook_name, stop=10):

        print(url)

        if url.endswith('.pdf') or url.endswith('.epub') or url.endswith('.mobi'):

            if 'github.com' in url:
                url = url.replace('blob', 'raw')

            try:
                _dwnfil(url, file_name=ebook_name + '/' + url.split('/')[-1])
            except Exception, e:
                print(url+'\t'+str(e))
                continue

        else:
            try:
                soup = Soup(gethtml(url))
            except Exception, e:
                print(url+'\t'+str(e))
                continue

            for link in soup.find_all('a', href=True):
                try:
                    for a in Soup(gethtml(link['href'])).find_all('a', href=True):
                        href = a['href']
                        try:
                            if href.endswith('.pdf') or href.endswith('.epub') or href.endswith('.mobi'):
                                if 'github.com' in href:
                                    href = href.replace('blob', 'raw')
                                _dwnfil(href, file_name=ebook_name + '/' + href.split('/')[-1])
                        except Exception, e:
                            print(href+'\t'+str(e))
                            continue
                except Exception,e:
                    #print(str(link)+'\t'+str(e))
                    continue



# main function which asks for command line arguments
if __name__ == '__main__':
    ebooksearch("Full Metal Panic Volume 1")
