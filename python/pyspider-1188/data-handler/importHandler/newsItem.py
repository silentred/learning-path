#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-03-03 13:14:54
# Project: test

import re, datetime
from urlparse import urljoin, urlparse, urlunparse, urlsplit, urlunsplit
import sqlite3
import ast
import MySQLdb
import logging, logger
import pinyin
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from declarative import  Base, Video, VideoInfo, Category, PlaySource, Specicalty, RankItem, IndexItem, NewsItem
from sqlalchemy.orm.exc import NoResultFound

myLogger = logging.getLogger('v1188ys.importer.news_item')
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


def searchAndSaveNews(session, newsObjs):
    if not len(newsObjs):
        return None

    for news in newsObjs:
        try:
            now = add_date = datetime.datetime.now()
            if news['page_id']==0:
                newsItem = NewsItem(
                        title = news['title'].decode('unicode-escape'),
                        section = news['section'],
                        url = news['url'],
                        cover = news['cover'],
                        page_id = news['page_id'],
                        add_date = now
                    )
            elif news['page_id']==4 and news['section']=='new_updates':
                if news.has_key('video_id') and news['video_id']!=0:
                    video = searchVideo(session, news['video_id'], 4)
                    newsItem = NewsItem(
                            title = news['title'].decode('unicode-escape'),
                            desc = news['desc'].decode('unicode-escape'),
                            section = news['section'],
                            url = news['url'],
                            page_id = news['page_id'],
                            video = video,
                            add_date = now
                        )
                else:
                    newsItem = NewsItem(
                            title = news['title'].decode('unicode-escape'),
                            desc = news['desc'].decode('unicode-escape'),
                            section = news['section'],
                            url = news['url'],
                            page_id = news['page_id'],
                            add_date = now
                        )
            elif news['page_id']==4 and news['section']=='entertain_news':
                if news.has_key('video_id') and news['video_id']!=0:
                    video = searchVideo(session, news['video_id'], 4)
                    newsItem = NewsItem(
                            title = news['title'].decode('unicode-escape'),
                            section = news['section'],
                            url = news['url'],
                            page_id = news['page_id'],
                            video = video,
                            add_date = now
                        )
                else:
                    newsItem = NewsItem(
                            title = news['title'].decode('unicode-escape'),
                            section = news['section'],
                            url = news['url'],
                            page_id = news['page_id'],
                            add_date = now
                        )
            session.add(newsItem)
        except NoResultFound, e:
            #print 'cannot find video whose orig_id=%s, video_type_id=%s ' % (news['orig_id'], news['video_type_id'])
            continue
        except Exception, e:
            raise e

def start():
    session = initSession()
    with MySQLdb.connect('172.16.1.248', 'qiye_dev', 'qiye..dev', '1188ys_resultdb') as cursor:
        #cursor = db.cursor()
        cursor.execute('''SELECT taskid, result from news_item''')
        allRows = cursor.fetchall()
        i = 0
        for row in allRows:
            try:
                newsObjs = ast.literal_eval(row[1])
                # 根据orig_id和video_type_id来查询现在的id。保存。
                searchAndSaveNews(session, newsObjs)
                i += 1
                if i % 200 == 0:
                    session.commit()
            except Exception, e:
                myLogger.error('Error: %s, taskid : %s',e, row[0])
                #logging.error('task id is  %s, eval error ', row[0])
        session.commit()
    
