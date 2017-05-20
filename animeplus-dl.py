from bs4 import BeautifulSoup
import urllib2, time, re, sys
import logging
logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(name)s[%(funcName)s] %(message)s')

Soup = lambda htm: BeautifulSoup(htm, 'html.parser')

URL = "http://www.animeplus.tv"

def gethtml(link):
    time.sleep(1)
    req = urllib2.Request(link, headers={'User-Agent': "Magic Browser"})
    con = urllib2.urlopen(req)
    html = con.read()
    return html


def getflvs(nm, ep_num):
    nm = nm.lower()
    ep_num = ep_num.lower()
    link = 'http://www.animeplus.tv/'+'-'.join(nm.split(' '))+'-episode-'+'-'.join(ep_num.split(' '))+'-online'
    logging.info('Searching %s', link)
    htm = gethtml(link)
    rgx = re.compile('src\s*=\s*"(.+?\.[flv|mp4].*?)"')
    video_links = re.findall(rgx,htm)
    for video_link in video_links:
        try:
            vidhtm = gethtml(video_link)
            vid_rgx = re.compile('file\s*:\s*"(.+?\.[flv|mp4].*?)"')
            dwn_link = re.search(vid_rgx,vidhtm).group(1)
            file_name = re.search((r'"filename"\s*:\s*"(.+?\.(flv|mp4))"'),vidhtm).group(1)
            _dwnfil(dwn_link, file_name = '/home/eadaradhiraj/Videos/'+file_name)
        except Exception,e:
            logging.error('Unhandled exception: %s', e)
            pass
        else:
            break

def _dwnfil(url, file_name="vid"):
    try:
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
        sys.exit("Interrupted!!!")
    except Exception, e:
        sys.exit("Error in download function " + str(e))
    else:
        logging.info('Complete')


def _Main():
    nm = raw_input('Enter anime: ')
    ep_num = raw_input('Enter episode number: ')
    getflvs(nm, ep_num)


if __name__ == '__main__':
    _Main()
