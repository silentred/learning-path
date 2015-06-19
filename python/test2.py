#!/usr/bin/python
## -*- encoding: utf-8 -*-
#
import re
import os, sys
import Image

# 逐行读取文件的方法
# obj = open('hello.txt', 'rU')
# try:
#     for x in obj:
#         pass
# finally:
#     obj.close()


print re.sub(r'/p800_', '/c180_', 'http://i3.meishichina.com/attachment/recipe/2014/05/20/p800_20140520093751990433063.jpg')



size = 180, 180
for infile in sys.argv[1:]:
    print infile
    outfile = os.path.splitext(infile)[0] + ".thumbnail"
    print outfile
    if infile != outfile:
        try:
            im = Image.open(infile)
            im.thumbnail(size, Image.ANTIALIAS)
            im.save(outfile, "PNG")
        except IOError:
            print "cannot create thumbnail for '%s'" % infile


json_string = 'sdf "img": "http://sdfc.om/sdf.jpg", sdf'
# 前后零宽断言
result = re.findall(r'(?<=img": ").+?(?="\})', json_string)
print result
