#!/usr/bin/env python
# -- coding: utf-8 --

import urllib2
import time
import re
import sys

URL = "http://www.animeplus.tv"

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


def get_video_links(link, loc):
    # nm = nm.lower()
    # ep_num = ep_num.lower()
    # link = 'http://www.animeplus.tv/'+'-'.join(nm.split(' '))+'-episode-'+'-'.join(ep_num.split(' '))+'-online'
    # if not link.startswith(URL): sys.exit('Link does not belong to animeplus.tv')
    print('Searching \n' + link)
    playlist = 1

    while True:

        errs = None

        # This stops the script if any error occurs while establishing the connction
        # It also stops when the playlist is exceeded
        try:
            htm = gethtml(link + '/' + str(playlist))
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
                _dwnfil(dwn_link, file_name=loc + '/' + file_name)

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
                if 'episode' in link:
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


# Code to download the file
def _dwnfil(url, file_name):
    print("Found!!")
    u = urllib2.urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print ("Downloading: %s Bytes: %s" % (file_name, file_size))

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
    get_video_links('http://www.animeplus.tv/kimi-no-na-wa.-2016-online', loc='.')


if __name__ == '__main__':
    _Main()
