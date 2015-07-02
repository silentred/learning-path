#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-03-03 13:14:54
# Project: test

import logging, logger, time, pinyin, ast, sys, traceback, json, MySQLdb, re, datetime, math
from urlparse import urljoin, urlparse, urlunparse, urlsplit, urlunsplit
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from declarative import  Recipe, Category, Base, Material, Collection, Recipe, RecipeInfo
from sqlalchemy.orm.exc import NoResultFound
from declarative import initSession
#, convertUnicodeForDic, decodeUnicodeKey

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
        return cat
    except NoResultFound, e:
        cover = ''
        if len(obj[u'pics'])>0:
            cover = obj[u'pics'][0]

        #print obj[u'main_material']

        cat = Recipe(
                name=obj[u'name'],
                orig_id= obj[u'orig_id'],
                cover=cover,
                date_add= datetime.datetime.now()                
            )
        session.add(cat)
        return cat
        #myLogger.error('cannot find cat  whose name=%s' % (obj['name'],))
    except Exception, e:
        raise e

def saveRecipeInfo(session, obj, savedRecipeObj):
    if savedRecipeObj is None:
        return None
    try:
        recipeInfo = session.query(RecipeInfo).filter(RecipeInfo.recipe == savedRecipeObj).one()
        return recipeInfo
    except NoResultFound, e:
        main_material =  json.dumps(obj[u'main_material']).decode('unicode-escape')
        condiment = json.dumps(obj[u'comdiment']).decode('unicode-escape')
        procedure  = json.dumps(obj[u'procedure']).decode('unicode-escape')
        recipeInfo = RecipeInfo(
                intro=obj[u'intro'],
                main_material=main_material,
                condiment=condiment,
                procedure=procedure,
                tips=obj[u'tips'],
                picture=json.dumps(obj[u'pics']),
                tool = obj[u'tool'],
                recipe = savedRecipeObj
            )
        session.add(recipeInfo)
        return recipeInfo
    except Exception, e:
        myLogger.error(e)
        raise e

def saveCategoryRelation(session, itemObj, recipe):
    if recipe is None:
        return None
    cats = itemObj[u'cats']
    for each in cats:
        try:
            categories = session.query(Category).filter(Category.name == each).all()
        except NoResultFound, e:
            myLogger.error("category not found")
            raise e
        except Exception, e:
            raise e
        for cat in categories:
            recipe.categories.append(cat)
    

def start(kwargs):
    session, engine = initSession()
    with MySQLdb.connect(kwargs['db_host'], kwargs['db_user'], kwargs['db_pass'], '1188ys_resultdb') as cursor:
        #cursor = db.cursor()
        limit = 1000
        cursor.execute('''SELECT count(*) from meishi_recipe''')
        rowCount = cursor.fetchone()[0]
        runtimes = math.ceil(rowCount/limit)

        for x in xrange(0, int(runtimes)):
            sql = "SELECT taskid, result from meishi_recipe limit %d, %d" % (int(x*limit ), int(limit))
            cursor.execute(sql)
            allRows = cursor.fetchall()
            i = 0
            for row in allRows:
                try:
                    itemObj = json.loads(row[1])
                    recipe = searchAndSave(session, itemObj)
                    saveRecipeInfo(session, itemObj, recipe)
                    saveCategoryRelation(session, itemObj, recipe)
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
    kwargs = {'db_host':'172.16.1.248', 'db_user':'qiye_dev', 'db_pass': 'qiye..dev', 'db_name':'1188meishi'}
    start(kwargs)