import re
import requests
import numpy as np
import os
import threading
import eventlet


# MutiThread download html pages

# Get urls recursively with maxdepth
class Geturls():
    def __init__(self, url, depth):
        self.url = url
        self.depth = depth

    def getAllurl(self, maxdepth):
        # if Thread reach the maxdepth, return
        if self.depth == maxdepth:
            return

        try:
            # Pretend to be browser
            hea = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                              '/41.0.2272.118 Safari/537.36'}
            if not os.path.exists('./html_list/' + os.path.basename(self.url)) or self.depth == 0:
                response = requests.get(self.url, headers=hea).text
            else:
                return
        except:
            return
        # url pattern to be match
        url_patten = r'<a href="(.*?)"'
        res = re.findall(url_patten, response)

        # Modify different url format
        for idx in range(len(res)):
            if res[idx][:2] == '//':
                res[idx] = 'https:' + res[idx]
            elif res[idx][:7] == '/video/':
                res[idx] = os.path.dirname(res[idx])
                res[idx] = 'https://www.bilibili.com' + res[idx]
        print('%s\tGet %d urls in depth %d' % (self.url, res.__len__(), self.depth))
        res = np.unique(res)
        for i in res:
            if i:
                Geturls(i, self.depth + 1).getAllurl(maxdepth)
                ms = multiThread(i)
                ms.start()


class multiThread(threading.Thread):
    def __init__(self, url):
        super(multiThread, self).__init__()
        self.url = url

    def run(self):
        hea = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                          '/41.0.2272.118 Safari/537.36'}
        try:
            response = requests.get(self.url, headers=hea, timeout=5).text
        except:
            response = None
        # Get the number of av***
        name = os.path.basename(self.url)

        # if number is exist , skip
        if name and response:
            if not os.path.exists('../../html_pages/' + name):
                with open('../../html_pages/' + name, 'w') as html:
                    print('Saving\t' + name + '\t' + str(response.__len__()))
                    html.write(response)
            else:
                print(name + '\t exist!')


# Only collect bilibili video pages with increasing the number of av****
class v_pages_Thread(threading.Thread):
    def __init__(self, url):
        super(v_pages_Thread, self).__init__()
        self.url = url

    def run(self):
        hea = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
        response = requests.get(self.url, headers=hea, timeout=20).text
        name = os.path.basename(self.url)
        if name and response and '视频去哪了呢' not in response and not os.path.exists('../../video_pages/' + name):
            with open('../../video_pages/' + name, 'w') as html:
                print('Saving\t' + name + '\t' + str(response.__len__()))
                html.write(response)
                html.close()
        else:
            print('Saving %s fail' % name)


if __name__ == '__main__':

    # Searching every url in current url, and download pages recursively with maxdepth.
    Geturls('https://www.bilibili.com/', 0).getAllurl(8)

    # Only collecting bilibili video pages with increasing the number of av****. 500 threads per time.
    # But it depends on your machine, Otherwise memory overflow
    for j in range(200000):
        for i in range(500):
            url = 'https://www.bilibili.com/video/av' + str(j * 500 + i)
            ms = v_pages_Thread(url)
            ms.start()
        # Wait 500 threads complete
        ms.join()
