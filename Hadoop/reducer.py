#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

url = None
count = 0
word = None
url_count = {}
for line in sys.stdin:
    line = line.strip()
    url, word, count = line.split()
    url, word, count = str(url), str(word), int(count)
    url_count[url] = count


url_count = sorted(url_count.items(), key=lambda item:item[1], reverse=True)
tmp = 0 # print(Top 20 results)
for i in url_count:
    print("%s\t%s\t%s" % (word, i[0], i[1]))
    tmp += 1
    if tmp == 20:
        break
    # try:
    #     count = int(count)
    # except ValueError:  #count如果不是数字的话，直接忽略掉
    #     continue
    # if count == 0:
    #     continue


