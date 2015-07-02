#!/usr/bin/python
## -*- encoding: utf-8 -*-
import re, datetime, urllib, os, threading, time, random, errno, MySQLdb, math, logger, logging, sys, json
from urlparse import urljoin, urlparse, urlunparse, urlsplit, urlunsplit

# class Downloader():
#     """docstring for Downloader"""
#     def __init__(self, dirPath, dbConnection, threadNum=10):
#         self.dirPath = dirPath
#         self.dbConnection = dbConnection
#         self.threadNum = threadNum

myLogger = logging.getLogger('1188meishi.img')

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise exc

def downloadImage(url):
    #start_time = time.time()
    baseDir = "/home/1188meishi_image"
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
        id = x[1]
        pics = json.loads(x[0])

        # procedure_pics = json.loads(x[2])
        # for each in procedure_pics:
        #     if each['img'] is not None:
        #         downloadImage(each['img'])
        procedure_pics = getAllProcedurePics(x[2])
        for each in procedure_pics:
            downloadImage(each)

        for each in pics:
            if each is not None:
                downloadImage(each)
                #取得小图url
                #small_pic = re.sub(r'/p800_', '/c180_', each)
                #downloadImage(small_pic)

        if id%10000 == 0:
            myLogger.info("dowloading id %d" % (id))

def getAllProcedurePics(json_string):
    results = re.findall(r'(?<=img": ").*?(?="\})', json_string);
    return filter(None, results)
        


def start(kwargs):
    start_time = time.time()
    threads = []
    limit  =200.0
    workerNum = 30
    try:
        db = MySQLdb.connect(kwargs['db_host'], kwargs['db_user'], kwargs['db_pass'], kwargs['db_name'])
        cursor = db.cursor()
        cursor.execute("SELECT count(1) from recipe_info")
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

            sql = "SELECT picture, id, `procedure` from recipe_info  limit %d, %d" % (int(x*limit ), int(limit))
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
        #traceback.print_exc(file=sys.stdout)
        #sys.exit()
        myLogger.error(e)

if __name__ == '__main__':
    kwargs = {'db_host':'172.16.1.248', 'db_user':'qiye_dev', 'db_pass': 'qiye..dev', 'db_name':'1188meishi'}
    start(kwargs)
