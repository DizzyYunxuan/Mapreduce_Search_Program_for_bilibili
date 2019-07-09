#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import re

#The word U wanna Search
word = ''

url = None
count = 0

# Find the end of the current html page
patten = '(This is the end of a html: av(.*?))/'


for line in sys.stdin:
    line = line.replace('\n', '')
    tmp = re.search(patten, line)
    count += line.upper().count(word.upper())
    if tmp:
        url = 'https://www.bilibili.com/video/' + tmp.group(1).split(' ')[-1]
        print("%s\t%s\t%d" % (url, word, count))
        url = None
        count = 0
