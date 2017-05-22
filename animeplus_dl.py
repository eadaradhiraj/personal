#!/usr/bin/env python
# -- coding: utf-8 --

import urllib2, time, re, sys, argparse

URL = "http://www.animeplus.tv"

def gethtml(link):
    time.sleep(1)
    try:
        req = urllib2.Request(link, headers={'User-Agent': "Magic Browser"})
        con = urllib2.urlopen(req)
        html = con.read()
        return html
    except urllib2.HTTPError as e:
        if e.code == 404:
            print("No such series or episode!! Please check!!\n")
        else:
            print("Error in connection!!")
        sys.exit()


def get_video_links(link):
    #nm = nm.lower()
    #ep_num = ep_num.lower()
    #link = 'http://www.animeplus.tv/'+'-'.join(nm.split(' '))+'-episode-'+'-'.join(ep_num.split(' '))+'-online'
    if not link.startswith(URL): sys.exit('Link does not belong to animeplus.tv')
    print('Searching \n'+ link)
    playlist = 1
    while True:
        try:
            htm = gethtml(link+'/'+str(playlist))
            rgx = re.compile('src\s*=\s*"(.+?\.(?:mkv|flv|mp4).*?)"')
            video_links = re.findall(rgx,htm)
            for video_link in video_links:
                try:
                    vidhtm = gethtml(video_link)
                    vid_rgx = re.compile('file\s*:\s*"(.+?\.(?:mkv|flv|mp4).*?)"')
                    dwn_link = re.search(vid_rgx,vidhtm).group(1)
                    file_name = re.search((r'"filename"\s*:\s*"(.+?\.(?:mkv|flv|mp4))"'),vidhtm).group(1)
                    _dwnfil(dwn_link, file_name = file_name)
                    if 'episode' in link: sys.exit()
                except KeyboardInterrupt:
                    sys.exit('Interuptted!!!')
                except Exception,e:
                    print('Unhandled exception: '+str(e))
                    pass
            sys.exit()
        except KeyboardInterrupt:
            sys.exit('Interuptted!!!')
        except Exception, e:
            print('Unhandled exception: ' + str(e))
            playlist += 1
            pass

def _dwnfil(url, file_name):
    try:
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
    except KeyboardInterrupt:
        sys.exit("\nInterrupted!!!")
    except Exception, e:
        print("\nError in download function " + str(e))
    else:
        print("\nComplete!")


def _Main():
    parser = argparse.ArgumentParser(description='Download anime from animeplus.tv')
    parser.add_argument('--link', '-l', type=str, help='Enter name of series in quotes')
    #parser.add_argument('--episode', '-e', type=str, help='Give episode number')
    args = parser.parse_args()
    get_video_links(link=args.link)

if __name__ == '__main__':
    _Main()
