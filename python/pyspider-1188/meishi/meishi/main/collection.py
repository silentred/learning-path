#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-03-03 13:14:54
# Project: test

import logging, logger, time, pinyin, ast, sys, traceback, json, MySQLdb, re, datetime
from urlparse import urljoin, urlparse, urlunparse, urlsplit, urlunsplit
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from declarative import  Recipe, Category, Base, Material, Collection
from sqlalchemy.orm.exc import NoResultFound
from declarative import initSession

myLogger = logging.getLogger('1188meishi.collection')
# def initSession():
#     engine = create_engine('mysql+mysqldb://test:test@172.16.1.19/1188meishi?charset=utf8&use_unicode=0')
#     Base.metadata.bind = engine
#     DBSession = sessionmaker(bind=engine)
#     session = DBSession()
#     return (session, engine)

def search(session, obj):
    try:
        cat = session.query(Collection).filter(Collection.name == obj['name'].decode('unicode-escape')).one()
    except NoResultFound, e:
        raise e
    except Exception, e:
        myLogger.error('Searh Collection Error')
        raise e
    return cat


def searchAndSave(session, obj):
    if not len(obj):
        return None
    try:
        cat = search(session, obj)
    except NoResultFound, e:
        cat = Collection(
                name=obj['name'].decode('unicode-escape'),
                orig_id= obj['orig_id'],
                intro=obj['intro'].decode('unicode-escape'),
                date_add= datetime.datetime.now()                
            )
        session.add(cat)
        #myLogger.error('cannot find cat  whose name=%s' % (obj['name'],))
    except Exception, e:
        raise e

def start(kwargs):
    session, engine = initSession()
    with MySQLdb.connect(kwargs['db_host'], kwargs['db_user'], kwargs['db_pass'], '1188ys_resultdb') as cursor:
        #cursor = db.cursor()
        cursor.execute('''SELECT taskid, result from meishi_collection''')
        allRows = cursor.fetchall()
        i = 0
        for row in allRows:
            try:
                itemObj = ast.literal_eval(row[1])
                searchAndSave(session, itemObj)
                i += 1
                if i % 200 == 0:
                    session.commit()
            except Exception, e:
                #traceback.print_exc(file=sys.stdout)
                myLogger.error('Error: %s - taskid : %s',e, row[0])
                #sys.exit()
                #logging.error('task id is  %s, eval error ', row[0])
        session.commit()
    

if __name__ == '__main__':
    kwargs = {'db_host':'172.16.1.248', 'db_user':'qiye_dev', 'db_pass': 'qiye..dev', 'db_name':'1188meishi'}
    start(kwargs)