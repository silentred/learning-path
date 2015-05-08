#!/usr/bin/python
## -*- encoding: utf-8 -*-
import re, datetime, urllib, os, threading, time, random, errno, MySQLdb, math, logger, logging
from urlparse import urljoin, urlparse, urlunparse, urlsplit, urlunsplit

# class Downloader():
#     """docstring for Downloader"""
#     def __init__(self, dirPath, dbConnection, threadNum=10):
#         self.dirPath = dirPath
#         self.dbConnection = dbConnection
#         self.threadNum = threadNum

myLogger = logging.getLogger('v1188ys.download.image')

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise exc

def downloadImage(url):
    #start_time = time.time()
    baseDir = "/home/jason/shared/image"
    #baseDir = "/root/image"
    parsed = urlparse(url)
    path = parsed[2]
    fullPath = baseDir+path
    fullDir = os.path.dirname(fullPath)
    if not os.path.exists(fullDir):
        mkdir_p(fullDir)

    fileExists = os.path.exists(fullPath)
    try:
        if not fileExists:
            result = urllib.urlretrieve(url, fullPath)
            #print "execution time: %f s" % (time.time()-start_time) 
    except IOError, e:
        myLogger.error("io error: %s - url: %s" % (e,url))
    except Exception, e:
        raise e

def partitionDownload(fetchResult):
    for x in fetchResult:
        poster =  x[0]
        small = x[1]
        downloadImage(poster)
        downloadImage(small)
        if x[2]%10000 == 0:
            myLogger.info("dowloading id %d" % (x[2]))


def start():
    start_time = time.time()
    threads = []
    limit  =1000.0
    workerNum = 10
    try:
        db = MySQLdb.connect('172.16.1.19', 'test', 'test', '1188test')
        cursor = db.cursor()
        cursor.execute("SELECT count(1) from video_info")
        rowCount = cursor.fetchone()[0]
        runtimes = math.ceil(rowCount/limit)
        for x in xrange(0, int(runtimes)):
            while True:
                #if not alive, delete it
                for t in threads:
                    if not t.isAlive():
                        threads.remove(t)
                # if <10, then go to get more from DB 
                if len(threads) < workerNum:
                    #print 'current threads num is %d' % (len(threads),)
                    break
                #sleep for 1s, waiting for the next check
                #print "waiting for 1s"
                time.sleep(1)

            sql = "SELECT poster_image, small_image, id from video_info  limit %d, %d" % (int(x*limit ), int(limit))
            cursor.execute(sql)
            result = cursor.fetchall()
            #if result is empty?
            if len(result) == 0:
                #print 'result is empty, ready to exit main process'
                break 
            t1 = threading.Thread(target = partitionDownload, args=(result,) )
            threads.append(t1)
            t1.start()
    except Exception, e:
        myLogger.error(e)
