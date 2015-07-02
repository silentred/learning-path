#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-03-03 13:14:54
# Project: test

import re, datetime
from urlparse import urljoin, urlparse, urlunparse, urlsplit, urlunsplit
import ast
import MySQLdb
import logging, logger
import pinyin
from declarative import  Recipe, Category, Base
from sqlalchemy.orm.exc import NoResultFound
from declarative import initSession

myLogger = logging.getLogger('1188meishi.catgory')

def searchCategory(session, obj):
    try:
        cat = session.query(Category).filter(Category.name == obj['name']).one()
    except NoResultFound, e:
        raise e
    except Exception, e:
        myLogger.error('Searh Category Error')
        raise e
    return cat


def searchAndSaveCategory(session, objs):
    if not len(objs):
        return None

    for obj in objs:
        try:
            cat = searchCategory(session, obj)
        except NoResultFound, e:
            cat = Category(
                    name=obj['name'].decode('unicode-escape'),
                    cat_type=obj['cat_type'].decode('unicode-escape'),
                    url_rewrite=pinyin.get(obj['name'].decode('unicode-escape')) or ''
                )
            session.add(cat)
            #myLogger.error('cannot find cat  whose name=%s' % (obj['name'],))
            continue
        except Exception, e:
            raise e

# def convertUnicodeForDic(data):
#     if isinstance(data, dict):
#         return { decodeUnicode(key):decodeUnicode(value) for key,value in data.items() }
#     if isinstance(data, list):
#         newData = []
#         for x in data:
#             decodedDict = convertUnicodeForDic(x)
#             newData.append(decodedDict)
#         return newData

# def decodeUnicode(data):
#     if isinstance(data, int ):
#         return data
#     if isinstance(data, str):
#         return data.decode('utf-8')

# def decodeUnicodeKey(dict):
#     return { decodeUnicode(key):value for key,value in dict.items() }

def start(kwargs):
    session, engine = initSession()
    with MySQLdb.connect(kwargs['db_host'], kwargs['db_user'], kwargs['db_pass'],'1188ys_resultdb') as cursor:
        #cursor = db.cursor()
        cursor.execute('''SELECT taskid, result from meishi_category''')
        allRows = cursor.fetchall()
        i = 0
        for row in allRows:
            try:
                itemObjs = ast.literal_eval(row[1])
                searchAndSaveCategory(session, itemObjs)
                i += 1
                if i % 200 == 0:
                    session.commit()
            except Exception, e:
                myLogger.error('Error: %s - taskid : %s',e, row[0])
                #logging.error('task id is  %s, eval error ', row[0])
        session.commit()
    

if __name__ == '__main__':
    kwargs = {'db_host':'172.16.1.248', 'db_user':'qiye_dev', 'db_pass': 'qiye..dev', 'db_name':'1188meishi'}
    start(kwargs)