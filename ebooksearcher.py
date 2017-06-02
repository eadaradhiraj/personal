#!/usr/bin/python
# -*- coding: utf-8 -*-

# Lit of libraries needed to run the programme
import urllib2
import time
import os
import downloads
import threading
from bs4 import BeautifulSoup
from google import search

# lambda function to create a soup from the html source
def Soup(htm) : return BeautifulSoup(htm, 'html.parser')

# The following acquires the html source code using urllib2
def gethtml(url):
    time.sleep(2)
    req = urllib2.Request(url, headers={'User-Agent': "Magic Browser"})
    con = urllib2.urlopen(req)
    html = con.read()
    return html

def search_for_ebooks(ebook_name, url):

    def sub_search(ebook_name, href):
        try:
            if 'github.com' in href:
                href = href.replace('blob', 'raw')
            downloads.download(url=href, out_path=ebook_name + '/' + href.split('/')[-1], progress=True)
        except Exception, e:
            # print(href + '\t' + str(e))
            return

    #print(url)

    if url.endswith('.pdf') or url.endswith('.epub') or url.endswith('.mobi'):
        sub_search(ebook_name, url)


    else:
        try:
            soup = Soup(gethtml(url))
        except Exception, e:
            #print(url + '\t' + str(e))
            return

        for link in soup.find_all('a', href=True):
            subthreads = []
            try:
                for a in Soup(gethtml(link['href'])).find_all('a', href=True):
                    href = a['href']
                    if href.endswith('.pdf') or href.endswith('.epub') or href.endswith('.mobi'):
                        subthread = threading.Thread(target=sub_search, args=(ebook_name, href))
                        subthreads.append(subthread)
                        subthread.start()

                    # Wait for all threads to end.
                for subthread in subthreads:
                    subthread.join()
            except:
                continue

# Seaching for each ebook using google and finding for suitable links and downloadingt those found
def ebook_searcher(ebook_name):

    print('Looking for ebook: ' + ebook_name)

    if not os.path.exists(ebook_name):
        os.makedirs(ebook_name)

    google_search_results = search(query=ebook_name, stop=10)

    downloadThreads = []

    for url in google_search_results:
        #search_for_ebooks(ebook_name,url)
        downloadThread = threading.Thread(target=search_for_ebooks, args=(ebook_name, url))
        downloadThreads.append(downloadThread)
        downloadThread.start()

    # Wait for all threads to end.
    for downloadThread in downloadThreads:
        downloadThread.join()
    print('Done.')


# main function which asks for command line arguments
if __name__ == '__main__':
    ebook_searcher("Full Metal Panic Vol. 1")
