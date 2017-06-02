#!/usr/bin/python
# -*- coding: utf-8 -*-

# Lit of libraries needed to run the programme
import threading
import urllib2
import time
import os
import traceback
import fileDownloader
import downloads
from bs4 import BeautifulSoup
from google import search


# lambda function to create a soup from the html source
def Soup(htm):
    return BeautifulSoup(htm, 'html.parser')

# The following function downloas the file using http protocol
def _dwnfil(url, file_name):
    print(url)
    fileDownloader.DownloadFile(url=url, localFileName=file_name).download()
    #downloads.download(url=url, out_path=file_name, progress=True)
    '''
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
    '''


# The following acquires the html source code using urllib2
def gethtml(url):
    time.sleep(2)
    req = urllib2.Request(url, headers={'User-Agent': "Magic Browser"})
    con = urllib2.urlopen(req)
    html = con.read()
    return html

def search_url (url, folder_name):
    if url.endswith('.pdf') or url.endswith('.epub') or url.endswith('.mobi'):

        if 'github.com' in url:
            url = url.replace('blob', 'raw')

        try:
            _dwnfil(url, file_name=folder_name + '/' + url.split('/')[-1])
        except:
            traceback.print_exc()
            return

    else:
        try:
            soup = Soup(gethtml(url))
        except:
            traceback.print_exc()
            return

        for link in soup.find_all('a', href=True):
            href = link['href']
            try:
                if href.endswith('.pdf') or href.endswith('.epub') or href.endswith('.mobi'):
                    if 'github.com' in href:
                        href = href.replace('blob', 'raw')
                    _dwnfil(href, file_name=folder_name + '/' + href.split('/')[-1])
            except:
                traceback.print_exc()
                continue

# Seaching for each ebook using google and finding for suitable links and downloadingt those found
def ebooksearch(ebook_name):

    print('Looking for ebook: ' + ebook_name)

    folder_name = unicode(ebook_name[:150], errors='replace')

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    google_search_results = search(query=ebook_name, stop=10)

    searchThreads = []

    for url in google_search_results:
        # search_for_ebooks(ebook_name,url)
        searchThread = threading.Thread(target=search_url, args=(url, folder_name))
        searchThreads.append(searchThread)
        searchThread.start()

    # Wait for all threads to end.
    for searchThread in searchThreads:
        searchThread.join()
    print('Done.')




# main function which asks for command line arguments
if __name__ == '__main__':
    ebooksearch("[10] S. Borkar. Thousand core chips—a technology perspective. In Design Automation Conference, pages 746–749. ACM, 2007.")
