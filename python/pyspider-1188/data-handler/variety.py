#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-03-03 13:14:54
# Project: test

import re, sqlite3, ast, MySQLdb, logging, pinyin, datetime
from urlparse import urljoin, urlparse, urlunparse, urlsplit, urlunsplit
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from declarative import  Base, Video, VideoInfo, Category, PlaySource, VarietySource
from sqlalchemy.orm.exc import NoResultFound

def initSession():
    engine = create_engine('mysql+mysqldb://test:test@192.168.2.50/1188test?charset=utf8&use_unicode=0')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session

def searchVideo(session,movie, video_type_id):
    try:
        movie = session.query(Video).filter(Video.orig_id == int(movie['orig_id'])).filter(Video.video_type_id == int(video_type_id)).one()
    except NoResultFound, e:
        raise e
    except Exception, e:
        print 'SearhVideo Error'
        raise e
    return movie

def searchVariety(session, variety_id, video_type_id):
    try:
        video = session.query(Video).filter(Video.orig_id == variety_id).filter(Video.video_type_id == video_type_id).one()
    except NoResultFound, e:
        raise e
    except Exception, e:
        raise e
    return video

def saveVideo(session, movie, video_type_id):
    #处理rating和runtime
    if not movie['rating']:
        movie['rating'] = '0'
    rating = re.search('\d+(\.?\d?)*', movie['rating']).group(0)
    
    video = Video(name=movie['title'].decode('unicode-escape'), 
            rating= float(rating),
            location = movie['location'].decode('unicode-escape'),
            orig_id = int(movie['orig_id']),
            video_type_id = video_type_id,
            platform = movie['platform'].decode('unicode-escape')
        )
    session.add(video)
    return video

def searchAndSaveVideo(session, movie, video_type_id):
    if not movie['title']:
        return None

    try:
        movie = searchVideo(session, movie, video_type_id)
    except NoResultFound, e:
        movie = saveVideo(session, movie, video_type_id)
    except Exception, e:
        print 'Unknown error'
        raise e
    return movie


def saveVideoInfo(session, movie, savedMovieObj):
    if savedMovieObj is None:
        return None
    try:
        # 查找是否已经存在
        videoInfoObj = session.query(VideoInfo).filter(VideoInfo.video == savedMovieObj).one()
        return videoInfoObj
    except NoResultFound, e:
        actors = ''
        if len(movie['hosts']) > 0:
            actorList = [x.decode('unicode-escape') for x in movie['hosts']]
            actors = ', '.join(actorList)

        videoInfoObj = VideoInfo(introduction=movie['introduction'].decode('unicode-escape'),
                poster_image = movie['poster_image'],
                small_image = movie['small_image'],
                video = savedMovieObj,
                actors = actors
            )
        session.add(videoInfoObj)
        return videoInfoObj
    except Exception, e:
        logging.error(e)
        raise e
    

def searchAndLinkCategory(sesstion, movie, savedMovieObj, video_type_id):
    if savedMovieObj is None:
        return None
    cats = movie['categories']
    for catName in cats:
        try:
            # 查找已有的
            catObj = session.query(Category).filter(Category.name == catName.decode('unicode-escape')).filter(Category.video_type_id == video_type_id).one()
            savedMovieObj.categories.append(catObj)
        except NoResultFound, e:
            # if not found, then save the cat, and associate the relations
            catObj = Category(name=catName.decode('unicode-escape'),
                    video_type_id=video_type_id,
                    url_rewrite = pinyin.get(catName.decode('unicode-escape')) or '',
                    is_hot = 0,
                    is_displayed = 0
                )
            session.add(catObj)
            savedMovieObj.categories.append(catObj)
        except Exception, e:
            logging.error(e)
            continue

def searchAndSaveVarietySource(session, video,savedVSObj ):
    if savedVSObj is None:
        return None
    sourceList = video['source']
    for each in sourceList:
        date= datetime.datetime.strptime(each['date'], '%Y-%m-%d').date()
        each['guests'] = ', '.join([x.decode('unicode-escape') for x in each['guests']])
        try:
            playSource = session.query(VarietySource).filter(VarietySource.video == savedVSObj).filter(VarietySource.api_name == video['api']).filter(VarietySource.date == date).one()
        except NoResultFound, e:
            playSource = VarietySource(date=date, 
                    title = each['desc'].decode('unicode-escape'),
                    guests = each['guests'],
                    video = savedVSObj,
                    small_image = each['img'],
                    url = each['url'],
                    api_name = video['api']
                )
            session.add(playSource)
        except Exception, e:
            raise e
        return playSource

session = initSession()
with sqlite3.connect('result.db') as db:
    cursor = db.cursor()
    cursor.execute('''SELECT taskid, result from resultdb_variety limit 0, 500''')
    allRows = cursor.fetchall()
    i = 0
    for row in allRows:
        try:
            video = ast.literal_eval(row[1])
            if not video['is_play_source']:
                # 保存video, 如果已经存在就返回搜索到的Video对象
                savedMovieObj = searchAndSaveVideo(session, video, 4)
                # 保存VideoInfo
                saveVideoInfo(session, video, savedMovieObj)
                #保存并关联category
                searchAndLinkCategory(session, video, savedMovieObj, 4)
            else:
                savedVarietyObj = searchVariety(session, video['variety_id'], 4)
                searchAndSaveVarietySource(session, video, savedVarietyObj)
            
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

