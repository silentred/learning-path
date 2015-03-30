#!/usr/bin/python
## -*- encoding: utf-8 -*-
import re, datetime, urllib, os, threading, time, random, errno, MySQLdb, math
from urlparse import urljoin, urlparse, urlunparse, urlsplit, urlunsplit

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise exc

def downlaodImage(url):
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
        print "io error, url: %s" % (url,)
    except Exception, e:
        raise e

# url = "http://img3.2345.com/dianyingimg/zongyi/img/f/5/sup15012_223x310.jpg?1419516249"

# def printTime(name):
#     for x in xrange(1,3):
#         print "Thread %s : time is %s" % (name, time.ctime(time.time()))
#         time.sleep(random.random())

# threads = []
# for x in xrange(1,100):
#     if len(threads)>10:
#         for t in threads:
#             t.join()
#         del threads[:] # empty the list
#     t1 = threading.Thread(target = printTime, args=("No%d" % (x),) )
#     threads.append(t1)
#     t1.start()

# threads = []
# try:
#     db = MySQLdb.connect('192.168.2.50', 'test', 'test', '1188test')
#     cursor = db.cursor()
#     cursor.execute(""" SELECT poster_image, small_image from video_info""")
#     for x in cursor.fetchall():
#         poster =  x[0]
#         small = x[1]
#         if len(threads)>20:
#             for t in threads:
#                 t.join()
#             del threads[:] # empty the list
#         t1 = threading.Thread(target = downlaodImage, args=(poster,) )
#         t2 = threading.Thread(target = downlaodImage, args=(small,) )
#         threads.append(t1)
#         threads.append(t2)
#         t1.start()
#         t2.start()
# except Exception, e:
#     print e

# def partitionDownload(fetchResult):
#     for x in fetchResult:
#         poster =  x[0]
#         small = x[1]
#         downlaodImage(poster)
#         downlaodImage(small)
#         print "time: %f s" % (time.time()) 

# threads = []
# limit  =1000.0
# try:
#     db = MySQLdb.connect('192.168.2.50', 'test', 'test', '1188test')
#     cursor = db.cursor()
#     cursor.execute("SELECT count(1) from video_info")
#     rowCount = cursor.fetchone()[0]
#     runtimes = math.ceil(rowCount/limit)
#     for x in xrange(0, int(runtimes)):
#         sql = "SELECT poster_image, small_image from video_info  limit %d, %d" % (int(x*limit ), int(limit))
#         cursor.execute(sql)
#         result = cursor.fetchall()
#         t1 = threading.Thread(target = partitionDownload, args=(result,) )
#         threads.append(t1)
#         t1.start()
# except Exception, e:
#     print e

try:
    db = MySQLdb.connect('192.168.2.50', 'test', 'test', '1188test')
    cursor = db.cursor()
    cursor.execute(""" SELECT poster_image, small_image, id from video_info LIMIT 47000, 50000""")
    for x in cursor.fetchall():
        poster =  x[0]
        small = x[1]
        downlaodImage(poster)
        downlaodImage(small)
        if x[2]%100 == 0:
            print "printing id %d" % (x[2])
except Exception, e:
    print e, "task id is %s" % x[2]