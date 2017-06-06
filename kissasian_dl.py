from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException
import sys
from bs4 import BeautifulSoup
import time
import logging
import os
import traceback
import re
import urllib2
import downloads

chromedriver = "./chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver

request_headers = {
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "http://thewebsite.com",
    "Connection": "keep-alive"
}

logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s [%(funcName)s] %(message)s',
                    datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)

FILE_HOSTERS = {'rapidvideo':'&s=rapid','openload':'&s=openload'}

def Soup(htmsrc):
    return BeautifulSoup(htmsrc,
                         'html.parser')

def get_html_norm(url):
    return urllib2.urlopen(
        urllib2.Request(url,
                        headers=request_headers)
    ).read()

def extract_video_link(url):
    new_soup = Soup(get_html_sel(url))
    return (new_soup.find('title').text, new_soup.find('video')['src'])


def get_html_sel(url, t=15):
    logger.info('Searching: {0}'.format(url))
    try:
        driver = webdriver.Chrome(chromedriver)
        driver.get(url)

        time.sleep(t)

        htmsrc = driver.page_source
        driver.quit()
        return (htmsrc)
    except NoSuchWindowException:
        sys.exit('The window closed unexpectedly.')

def get_filehostlink(url):
    for file_hoster_key, file_hoster_value in FILE_HOSTERS.iteritems():
        try:
            link = '{0}{1}'.format(url,file_hoster_value)
            soup = Soup(get_html_sel(link,t=15))
            return soup.find('iframe',src=re.compile(file_hoster_key))['src']
        except:
            traceback.print_exc()
            continue
        else:
            break

def kissasian_dl(url, loc):
    if not url.startswith('http://kissasian.com'):
        logger.info('The link does not belong to kissasian.com'); sys.exit()

    if not os.path.exists(loc):
        os.mkdir(loc)
    file_name, dwn_link =  extract_video_link(get_filehostlink(url))
    logger.info('Found a downloadable link: \n{0}'.format(dwn_link))
    downloads.download(url=dwn_link,
                       out_path='{0}/{1}'.format(loc, file_name),
                       progress=True)
    logger.info('Downloaded {0} to {1}'.format(file_name, loc))

def _Main():
    '''
    import argparse
    parser = argparse.ArgumentParser(description='Download episodes and movies from kisassian.com')
    parser.add_argument('--link', '-l', type=str, help='Enter link which is hosting the video')
    #parser.add_argument('--directory', '-d', type=str, default='.' help='Give folder location')
    args = parser.parse_args()
    kissasian_dl(link=args.link, loc=args.directory)
    '''

    kissasian_dl('http://kissasian.com/Drama/Your-Lie-in-April/Movie?id=33186', loc='/home/edhiraj/Videos')

if __name__ == '__main__':
    _Main()