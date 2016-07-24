# -*- coding: utf-8 -*-
# @Author: edward
# @Date:   2016-07-24 21:38:45
# @Last Modified by:   edward
# @Last Modified time: 2016-07-24 21:41:08
# -*- coding:utf-8 -*-
import base64
from StringIO import StringIO
import os
import glob

def encode_file(fn, buffer):
    print 'Encode >>', fn
    _, ext = os.path.splitext(fn)
    if ext in ['.png', '.ico', '.jpg']:
        file = open(fn, 'rb')
        pic = file.read()
        b64 = pic.encode('base64')
        buffer.write('%s = PyEmbeddedImage(\n"%s")\n\n' % (os.path.basename(fn).split('.')[0].replace('-', '_'), b64.strip().replace('\n', '"\n"')))
        
def encode(dir, buffer):
    if os.path.isdir(dir):
        lst = glob.glob(os.path.join(dir, '*.*'))
        for fn in lst:
            encode_file(fn, buffer)
    else:
        encode_file(dir, buffer)
        
def main(src_dir, res_file):
    print 'Out file >> ', os.path.abspath(src_dir), '\n\n'
    output = open(os.path.join(src_dir, res_file), 'w')
    output.write('# -×- coding:utf-8 -*-\n'
'from wx.lib.embeddedimage import PyEmbeddedImage\n\n')
    encode(src_dir, output)
    output.flush()
    output.close()

if __name__ == '__main__':
    import os
    main(os.getcwd(), 'resource.py')