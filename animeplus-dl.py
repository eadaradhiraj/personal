#!/usr/bin/env python
# -- coding: utf-8 --

from bs4 import BeautifulSoup
import urllib2, time, re, sys, argparse

Soup = lambda htm: BeautifulSoup(htm, 'html.parser')

URL = "http://www.animeplus.tv"


class Color:
    BEG = '\033['
    SEP = ';'
    BOLD = '1'
    RED = '31'
    GREEN = '32'
    YELLOW = '33'
    END_BEG = 'm'
    END = '\033[0m'

def printClr(string, *args):
    # we have to work backwards
    string = Color.END_BEG + string

    fst = False
    for arg in args:
        if(fst is False):
            string = arg + string
            fst = True
            continue

        string = Color.SEP + string
        string = arg + string

    string = Color.BEG + string
    print(string + Color.END)

def gethtml(link):
    time.sleep(1)
    try:
        req = urllib2.Request(link, headers={'User-Agent': "Magic Browser"})
        con = urllib2.urlopen(req)
        html = con.read()
        return html
    except urllib2.HTTPError as e:
        if e.code == 404:
            printClr("No such series or episode!! Please check!!\n" +
                     link, Color.RED, Color.BOLD)
        else:
            printClr("Error in connection ", link, Color.RED, Color.BOLD)
        sys.exit()


def get_video_links(nm, ep_num):
    nm = nm.lower()
    ep_num = ep_num.lower()
    link = 'http://www.animeplus.tv/'+'-'.join(nm.split(' '))+'-episode-'+'-'.join(ep_num.split(' '))+'-online'
    printClr('Searching \n'+ link, Color.YELLOW, Color.BOLD)
    htm = gethtml(link)
    rgx = re.compile('src\s*=\s*"(.+?\.[flv|mp4].*?)"')
    video_links = re.findall(rgx,htm)
    for video_link in video_links:
        try:
            vidhtm = gethtml(video_link)
            vid_rgx = re.compile('file\s*:\s*"(.+?\.[flv|mp4].*?)"')
            dwn_link = re.search(vid_rgx,vidhtm).group(1)
            file_name = re.search((r'"filename"\s*:\s*"(.+?\.(flv|mp4))"'),vidhtm).group(1)
            _dwnfil(dwn_link, file_name = '~/Videos/'+file_name)
            sys.exit()
        except Exception,e:
            printClr('Unhandled exception: '+str(e),Color.RED, Color.BOLD)
            pass
        else:
            break

def _dwnfil(url, file_name="vid"):
    try:
        printClr("Found!!", Color.GREEN, Color.BOLD)
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
    except KeyboardInterrupt:
        printClr("\nInterrupted!!!",Color.RED, Color.BOLD)
    except Exception, e:
        printClr("\nError in download function " + str(e), Color.RED, Color.BOLD)
    else:
        printClr("\nComplete!", Color.GREEN, Color.BOLD)


def _Main():
    parser = argparse.ArgumentParser(description='Download anime from animeplus.tv')
    parser.add_argument('--series', '-s', type=str, help='Enter name of series in quotes')
    parser.add_argument('--episode', '-e', type=str, help='Give episode number')
    args = parser.parse_args()
    get_video_links(nm=args.series, ep_num=args.episode)

if __name__ == '__main__':
    _Main()
