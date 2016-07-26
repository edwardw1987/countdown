#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: edward
# @Date:   2016-07-26 15:59:10
# @Last Modified by:   edward
# @Last Modified time: 2016-07-26 16:27:46
import argparse

def save(i, o):
    with open(i, 'rb') as inf:
        bytes_ = inf.read()
    with open(o, 'wb') as outf:
        outf.write('src=%s' % repr(bytes_))
        outf.flush()

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description="saveasbytes")
    parser.add_argument('-i', dest='input', required=True,
                        action='store', help="input filepath")
    parser.add_argument('-o', dest='output', required=True,
                        action='store', help="output filepath")
    args = parser.parse_args()
    save(args.input, args.output)
