#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-03-03 13:14:54
# Project: test

import re
from urlparse import urljoin, urlparse, urlunparse, urlsplit, urlunsplit
import sqlite3, math, time
import ast
import MySQLdb
import logging
import pinyin
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from declarative import  Base, Video, VideoInfo, Category, PlaySource, Specicalty, TVPlot
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

def searchTV(session,tv_id, video_type_id):
    try:
        movie = session.query(Video).filter(Video.orig_id == tv_id).filter(Video.video_type_id == video_type_id).one()
    except NoResultFound, e:
        raise e
    except Exception, e:
        raise e
    return movie

def saveVideo(session, movie, video_type_id):
    #处理rating和runtime
    if not movie['rating']:
        movie['rating'] = '0'
    rating = re.search('\d+(\.?\d?)*', movie['rating']).group(0)
    if not movie['year']:
        movie['year'] = 0
    
    video = Video(name=movie['title'].decode('unicode-escape'), 
            rating= float(rating) ,
            year = int(movie['year']),
            location = movie['location'].decode('unicode-escape'),
            orig_id = int(movie['orig_id']),
            video_type_id = video_type_id,
            is_closed = int(movie['closed']),
            director=movie['director'].decode('unicode-escape')
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
        if len(movie['casting']) > 0:
            actorList = [x.decode('unicode-escape') for x in movie['casting']]
            actors = ', '.join(actorList)

        introduction = movie['introduction'].decode('unicode-escape')
        introduction = re.sub(r'\s*展开全部\s*收起全部\s*', '', introduction)
        videoInfoObj = VideoInfo(introduction=introduction,
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

def searchAndLinkPlaySource(sesstion, movie, savedMovieObj, video_type_id):
    if savedMovieObj is None:
        return None
    play_sources = movie['play_source']
    for api_name in play_sources:
        for episode_num in play_sources[api_name]:
            try:
                playSource = session.query(PlaySource).filter(PlaySource.api_name == api_name).filter(PlaySource.video_id == savedMovieObj.id).filter(PlaySource.episode_num == int(episode_num.decode('unicode-escape')[:-1])).one()
            except NoResultFound, e:
                playSource = PlaySource(api_name=api_name,
                        url=play_sources[api_name][episode_num],
                        video=savedMovieObj,
                        episode_num = int(episode_num.decode('unicode-escape')[:-1])
                    )
                session.add(playSource)
            except Exception, e:
                logging.error(e)
                raise e

def searchAndLinkSpecialty(sesstion, movie, savedMovieObj, video_type_id):
    if savedMovieObj is None:
        return None
    seps = movie['specialties']
    for sep in seps:
        try:
            sepObj = session.query(Specicalty).filter(Specicalty.name == sep.decode('unicode-escape')).filter(Specicalty.video_type_id == video_type_id).one()
            savedMovieObj.specialties.append(sepObj)
        except NoResultFound, e:
            # if not found, then save the sep, and associate the relations
            sepObj = Specicalty(name=sep.decode('unicode-escape'),
                    video_type_id=video_type_id
                )
            session.add(sepObj)
            savedMovieObj.specialties.append(sepObj)
        except Exception, e:
            logging.error(e)
            raise e

def searchAndSaveTVPlot(session, video,savedTVObj ):
    if savedTVObj is None:
        return None
    try:
        tvPlot = session.query(TVPlot).filter(TVPlot.video == savedTVObj).filter(TVPlot.episode_num == video['episode_num']).one()
    except NoResultFound, e:
        tvPlot = TVPlot(content=video['content'].decode('unicode-escape'), 
                episode_num = video['episode_num'],
                video = savedTVObj
            )
        session.add(tvPlot)
    except Exception, e:
        raise e
    return tvPlot

session = initSession()
limit = 1000.0
with sqlite3.connect('result.db') as db:
    cursor = db.cursor()
    rowCount = cursor.execute('''SELECT count(*) from resultdb_tv''').fetchone()[0]
    runtimes = math.ceil(rowCount/limit)
    for x in xrange(0, int(runtimes)):
        sql = "SELECT taskid, result from resultdb_tv limit %d, %d" % (int(x*limit ), int(limit))
        print sql
        print time.asctime( time.localtime(time.time()) )
        cursor.execute(sql)
        allRows = cursor.fetchall()
        i = 0
        for row in allRows:
            try:
                video = ast.literal_eval(row[1])
                if not video['is_plot']:
                    # 保存video, 如果已经存在就返回搜索到的Video对象
                    savedMovieObj = searchAndSaveVideo(session, video, 3)
                    # 保存VideoInfo
                    saveVideoInfo(session, video, savedMovieObj)
                    #保存并关联category
                    searchAndLinkCategory(session, video, savedMovieObj, 3)
                    #保存并关联play source
                    searchAndLinkPlaySource(session, video, savedMovieObj, 3)
                    # 保存并关联sepcialty
                    #searchAndLinkSpecialty(session, video, savedMovieObj, 2)
                else:
                    savedTVObj = searchTV(session, video['tv_id'], 3)
                    searchAndSaveTVPlot(session, video, savedTVObj)
                
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

