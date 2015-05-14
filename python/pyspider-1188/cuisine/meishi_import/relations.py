#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-03-03 13:14:54
# Project: test

import logging, logger, time, pinyin, ast, sys, traceback, json, MySQLdb, re, datetime
from urlparse import urljoin, urlparse, urlunparse, urlsplit, urlunsplit
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from declarative import  Recipe, Category, Base, Material, Collection, Recipe
from sqlalchemy.orm.exc import NoResultFound
from category import initSession, convertUnicodeForDic, decodeUnicodeKey

myLogger = logging.getLogger('1188meishi.recipe')

def search(session, obj):
    try:
        cat = session.query(Recipe).filter(Recipe.orig_id == obj[u'orig_id']).one()
    except NoResultFound, e:
        raise e
    except Exception, e:
        myLogger.error('Searh Recipe Error')
        raise e
    return cat


def searchAndSave(session, obj):
    if not len(obj):
        return None
    try:
        cat = search(session, obj)
    except NoResultFound, e:
        cover = ''
        if len(obj[u'pics'])>0:
            cover = obj[u'pics'][0]

        #print obj[u'main_material']
        main_material =  json.dumps(obj[u'main_material']).decode('unicode-escape')
        condiment = json.dumps(obj[u'comdiment']).decode('unicode-escape')
        procedure  = json.dumps(obj[u'procedure']).decode('unicode-escape')

        cat = Recipe(
                name=obj[u'name'],
                orig_id= obj[u'orig_id'],
                intro=obj[u'intro'],
                main_material=main_material,
                condiment=condiment,
                procedure=procedure,
                tips=obj[u'tips'],
                picture=json.dumps(obj[u'pics']),
                cover=cover,
                tool = obj[u'tool'],
                date_add= datetime.datetime.now()                
            )
        session.add(cat)
        #myLogger.error('cannot find cat  whose name=%s' % (obj['name'],))
    except Exception, e:
        raise e


def start():
    session, engine = initSession()
    with MySQLdb.connect('172.16.1.248', 'qiye_dev', 'qiye..dev', '1188ys_resultdb') as cursor:
        #cursor = db.cursor()
        cursor.execute('''SELECT taskid, result from meishi_recipe limit 0, 500''')
        allRows = cursor.fetchall()
        i = 0
        for row in allRows:
            try:
                itemObj = json.loads(row[1])
                searchAndSave(session, itemObj)
                i += 1
                if i % 200 == 0:
                    session.commit()
            except Exception, e:
                traceback.print_exc(file=sys.stdout)
                myLogger.error('Error: %s - taskid : %s',e, row[0])
                #sys.exit()
                #logging.error('task id is  %s, eval error ', row[0])
        session.commit()
    

if __name__ == '__main__':
    start()