#!/usr/bin/python
## -*- encoding: utf-8 -*-
import re, os, logging, sys, fnmatch, traceback, urllib
import click
import Image
from logging.handlers import TimedRotatingFileHandler
from urlparse import urljoin, urlparse, urlunparse, urlsplit, urlunsplit

myLogger = logging.getLogger('thumbnail')
filepath = '/tmp/meishi1188_image.log'
fh = TimedRotatingFileHandler(filepath, when="d", interval=1, backupCount=4)
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
myLogger.addHandler(fh)

def thumbAllImage(path):
    matches = []
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, '*p800_*.jpg'):
            filepath = os.path.join(root, filename)
            smallImage = getSmallImagePath(filepath)
            if os.path.exists(smallImage):
                continue
            else:
                makeThumbnail(filepath, smallImage)
            #matches.append(fielpath)

def makeThumbnail(bigImage, smallImage):
    size = 180, 180
    try:
        im = Image.open(bigImage)
        im.thumbnail(size, Image.ANTIALIAS)
        im.save(smallImage, "JPEG")
    except IOError:
        #traceback.print_exc(file=sys.stdout)
        #sys.exit()
        myLogger.error("image broken: %s", bigImage)


def getSmallImagePath(bigImage):
    return re.sub(r'/p800_', '/c180_', bigImage)


@click.group()
@click.option('--path', default='/home/1188meishi_image', help='root path of big images')
def cli(**kwargs):
    pass

@cli.command()
@click.option('--path', default='/home/1188meishi_image', help='root path of big images')
def run(**kwargs):
    print kwargs
    click.echo('hello world')
    thumbAllImage(kwargs['path'])

@cli.command()
@click.option('--log', default='/tmp/meishi1188_image.log', help='path of log file')
@click.option('--path', default='/home/1188meishi_image', help='root path of big images')
def download(**kwargs):
    print "dowloading from log"
    if os.path.isfile(kwargs['log']):
        obj = open(kwargs['log'], 'rU')
        try:
            for line in obj:
                if re.match('^.*image broken: (.+\.jpg)$', line):
                    path=re.search('^.*image broken: (.+\.jpg)$', line).group(1).strip()
                    url='http://i3.meishichina.com/%s' % path[len(kwargs['path']):]
                    try:
                        urllib.urlretrieve(url, path)
                    except Exception, e:
                        myLogger.error("stop downloadImage at line: %s", path)
                        traceback.print_exc(file=sys.stdout)
                        sys.exit()
        finally:
            obj.close()

if __name__ == '__main__':
    cli()