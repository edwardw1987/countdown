#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: edward
# @Date:   2016-07-23 12:06:14
# @Last Modified by:   edward
# @Last Modified time: 2016-07-23 12:27:36
import sys
import re

path = sys.argv[1]
text = open(path).read()
text = ''.join(re.split('\d+\s*/\s*\d+', text))
REPLACES = [
    ('”', '"'),
    ('“', '"'),
]
for to_replace, replacement in REPLACES:
    text = text.replace(to_replace, replacement)
with open(path, 'w') as outfile:
    outfile.write(text)
    outfile.flush()
