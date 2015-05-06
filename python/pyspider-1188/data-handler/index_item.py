#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-03-03 13:14:54
# Project: test

import re, datetime
from urlparse import urljoin, urlparse, urlunparse, urlsplit, urlunsplit
import sqlite3
import ast
import MySQLdb
import logging
import pinyin
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from declarative import  Base, Video, VideoInfo, Category, PlaySource, Specicalty, RankItem, IndexItem
from sqlalchemy.orm.exc import NoResultFound

def initSession():
    engine = create_engine('mysql+mysqldb://test:test@172.16.1.19/1188test?charset=utf8&use_unicode=0')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session

def searchVideo(session,orig_id, video_type_id):
    try:
        video = session.query(Video).filter(Video.orig_id == int(orig_id)).filter(Video.video_type_id == int(video_type_id)).one()
    except NoResultFound, e:
        raise e
    except Exception, e:
        print 'SearhVideo Error'
        raise e
    return video


def searchAndSaveIndexItem(session, rankObjs):
    if not len(rankObjs):
        return None

    for rank in rankObjs:
        try:
            video = searchVideo(session, rank['orig_id'], rank['video_type_id'])
            if not rank.has_key('cover'):
                rank['cover'] = ''
            index = IndexItem(video=video,
                    desc = rank['desc'].decode('unicode-escape'),
                    page_id = rank['page_id'],
                    video_type_id = rank['video_type_id'],
                    section = rank['section'].decode('unicode-escape'),
                    sub_section = rank['sub_section'].decode('unicode-escape') if rank.has_key('sub_section') else '',
                    cover = rank['cover'],
                    big_cover = rank['big_cover'] if rank.has_key('big_cover') else '',
                    broadcast_time = rank['broadcast_time'].decode('unicode-escape') if rank.has_key('broadcast_time') else '',
                    long_desc = rank['long_desc'].decode('unicode-escape') if rank.has_key('long_desc') else '',
                    date_add = datetime.datetime.now()
                )
            session.add(index)
        except NoResultFound, e:
            print 'cannot find video whose orig_id=%s, video_type_id=%s ' % (rank['orig_id'], rank['video_type_id'])
            continue
        except Exception, e:
            raise e


session = initSession()
with MySQLdb.connect('172.16.1.248', 'qiye_dev', 'qiye..dev', '1188ys_resultdb') as cursor:
    #cursor = db.cursor()
    cursor.execute('''SELECT taskid, result from index_item''')
    allRows = cursor.fetchall()
    i = 0
    for row in allRows:
        try:
            itemObjs = ast.literal_eval(row[1])
            # 根据orig_id和video_type_id来查询现在的id。保存。
            searchAndSaveIndexItem(session, itemObjs)
            i += 1
            if i % 200 == 0:
                session.commit()
        except Exception, e:
            logging.error('Error: %s, taskid : %s',e, row[0])
            #logging.error('task id is  %s, eval error ', row[0])
    session.commit()
    


# try:
#     db = MySQLdb.connect('192.168.2.50', 'test', 'test', 'test')
#     cursor = db.cursor()
#     cursor.execute(""" SELECT * from api """)
#     for x in cursor.fetchall():
#         print x[1]

# except Exception, e:
#     print e

