#!/usr/bin/env python
# -- coding: utf-8 --

import urllib2
import downloads
import re
import sys
import os

URL_BASE = "http://www.animeplus.tv"

# request headers while establishing connection with the url
request_headers = {
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "http://thewebsite.com",
    "Connection": "keep-alive"
}

# Get html source of url
def gethtml(url):
    return urllib2.urlopen(
        urllib2.Request(url,
                        headers=request_headers)
    ).read()


def get_video_links(link, folder_name):

    if not link.startswith(URL_BASE):
        sys.exit('Link does not belong to animeplus.tv')

    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    print('Searching: {0}'.format(link))
    playlist = 1

    while True:

        errs = None

        # This stops the script if any error occurs while establishing the connction
        # It also stops when the playlist is exceeded
        try:
            htm = gethtml('{0}/{1}'.format(link,playlist))
        except:
            sys.exit('Not Found!!!')

        # Acquires video links with the following exceptions
        # Can add more extensions if necessary
        video_links = re.findall(
            r'src\s*=\s*"(.+?\.(?:mkv|flv|mp4).*?)"', htm)

        # Iterates through all video links found in the playlist
        for video_link in video_links:

            try:

                vidhtm = gethtml(video_link)
                dwn_link = re.search(r'file\s*:\s*"(.+?\.(?:mkv|flv|mp4).*?)"',
                                     vidhtm).group(1)
                file_name = re.search((r'"filename"\s*:\s*"(.+?\.(?:mkv|flv|mp4))"'),
                                      vidhtm).group(1)

                print ('Found')
                downloads.download(url=dwn_link, out_path='{0}/{1}'.format(folder_name, file_name), progress=True)

            except KeyboardInterrupt:
                sys.exit('Cancelled!!')

            # If any errors exist,
            # store the errors in a variable
            # then move on to the next link in the playlist
            except Exception as e:
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
            playlist += 1
            continue
        return


# Main function
def _Main():
    '''
    import argparse
    parser = argparse.ArgumentParser(description='Download anime from animeplus.tv')
    parser.add_argument('--link', '-l', type=str, help='Enter link which is hosting the video')
    #parser.add_argument('--episode', '-e', type=str, help='Give episode number')
    args = parser.parse_args()
    get_video_links(link=args.link)
    '''
    get_video_links('http://www.animeplus.tv/love-hina-episode-2-online', folder_name='/home/edhiraj/Videos')


if __name__ == '__main__':
    _Main()
