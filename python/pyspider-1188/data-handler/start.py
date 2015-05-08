#!/usr/bin/python
## -*- encoding: utf-8 -*-

from importHandler import downloadImageIndex, logger, indexItem, downloadImage, downloadImageQiyi, movie, comic, tv, variety, newsItem, rankItem
import logging, argparse, sys

def start_all():
    start_import()
    start_download()
    #print 'all'

def start_import():
    movie.start()
    comic.start()
    tv.start()
    variety.start()
    indexItem.start()
    newsItem.start()
    rankItem.start()
    #print 'import'
    
def start_download():
    downloadImageIndex.start()
    downloadImage.start()
    downloadImageQiyi.start()
    #print 'downloadImage'

if __name__ == '__main__' :
    myLogger = logging.getLogger('v1188ys.start')
    myLogger.info('starting...')

    parser = argparse.ArgumentParser(description='Start importing and downloading')
    parser.add_argument('action', help='all | import (just import row data into DB)| download (just download images in DB)')
    args = parser.parse_args()
    #print args
    if args.action == 'all':
        start_all()
    elif args.action == 'import':
        start_import()
    elif args.action == 'download':
        start_download()

    myLogger.info('ending...')