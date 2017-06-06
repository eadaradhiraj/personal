#!/usr/bin/env python
# -- coding: utf-8 --

import urllib2
import downloads
import re
import sys
import os
import logging
import traceback
from bs4 import BeautifulSoup
import json
import itertools

logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s [%(funcName)s] %(message)s',
                    datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)

URL_BASE = "http://www.animeplus.tv"

# request headers while establishing connection with the url
request_headers = {
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "http://thewebsite.com",
    "Connection": "keep-alive"
}

def Soup(htm):
    return BeautifulSoup(htm,'html.parser')

# Get html source of url
def gethtml(url):
    return urllib2.urlopen(
        urllib2.Request(url,
                        headers=request_headers)
    ).read()


def get_video_links(link, loc):

    if not link.startswith(URL_BASE):
        sys.exit('Link does not belong to animeplus.tv')

    if not os.path.exists(loc):
        os.mkdir(loc)

    logger.info('Searching: {0}'.format(link))
    playlist = 1

    while True:

        errs = None

        # This stops the script if any error occurs while establishing the connection
        try:
            htm = gethtml('{0}/{1}'.format(link,playlist))
        except:
            sys.exit('Not Found!!!')

        # Acquires video links with the following exceptions
        # Can add more extensions if necessary

        video_links = [l['src'] for l in Soup(htm).find('div',attrs={'id':'streams'}).find_all('iframe',src=True)]

        # Iterates through all video links found in the playlist
        for video_link in video_links:

            try:
                #acquires javascript object from the html link which contains links
                video_sub_links_dict = json.loads(re.search(r'var\svideo_links\s*\=\s*({.*})\;',
                                                            gethtml(video_link)).group(1))

                #iterates through sublinks by going through the javascript object

                for vid_sub_link in list(itertools.chain.from_iterable(video_sub_links_dict['normal'].values())):
                    try:
                        dwn_link = vid_sub_link['link']
                        file_name = vid_sub_link['filename']
                        logger.info('Found a downloadable link: \n{0}'.format(dwn_link))
                        downloads.download(url=dwn_link,
                                           out_path='{0}/{1}'.format(loc, file_name),
                                           progress=True)
                        logger.info('Downloaded {0} to {1}'.format(file_name, loc))
                        #try any one link and break
                        break
                    except:
                        traceback.print_exc()
                        logger.info('Moving on to the next sublink')
                        #if failure occurs move onto the next sublink
                        continue


            except KeyboardInterrupt:
                logger.debug('Cancelled by user!')
                sys.exit()

            # If any errors exist,
            # store the errors in a variable
            # then move on to the next link in the playlist
            except Exception as e:
                traceback.print_exc()
                logger.debug('Problem downloading from link!')
                logger.info('Moving on to the next link in the playlist!')
                if errs is None:
                    errs = e
                continue

            else:
                # If the link points to an episode,
                # then stops the script when the download is a success
                # for any one file
                if 'episode' or 'ova' in link:
                    return
                else:
                    pass

        # If any exceptions
        # while acquiring links from a playlist
        # move on to the next playlist
        if errs is not None:
            logger.debug('All downloadable links failed in playlist!')
            logger.info('Moving on to the next playlist!')
            playlist += 1
            continue
        return


# Main function
def _Main():
    '''
    import argparse
    parser = argparse.ArgumentParser(description='Download anime from animeplus.tv')
    parser.add_argument('--link', '-l', type=str, help='Enter link which is hosting the video')
    #parser.add_argument('--directory', '-d', type=str, default='.' help='Give folder location')
    args = parser.parse_args()
    get_video_links(link=args.link, loc=args.directory)
    '''

    get_video_links('http://www.animeplus.tv/omamori-himari-episode-5-online', loc='.')


if __name__ == '__main__':
    _Main()
