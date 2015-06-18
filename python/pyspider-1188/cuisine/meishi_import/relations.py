#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-03-03 13:14:54
# Project: test

import logging, logger, time, pinyin, ast, sys, traceback, json, MySQLdb, re, datetime, math
from urlparse import urljoin, urlparse, urlunparse, urlsplit, urlunsplit
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from declarative import  Recipe, Category, Base, Material, Collection, Recipe
from sqlalchemy.orm.exc import NoResultFound
from category import initSession #, convertUnicodeForDic, decodeUnicodeKey

myLogger = logging.getLogger('1188meishi.relations')

def searchRecipe(session, orig_id):
    try:
        cat = session.query(Recipe).filter(Recipe.orig_id == int(orig_id)).one()
    except NoResultFound, e:
        myLogger.error('Recipe not found, orig_id: %d', int(orig_id))
        #raise e
        return None
    except Exception, e:
        myLogger.error('Searh Recipe Error')
        #raise e
        return None
    return cat

def searchMaterial(session, obj):
    try:
        material = session.query(Material).filter(Material.name == obj[u'name']).one()
    except NoResultFound, e:
        myLogger.error('Searh Material Not Found: %s',obj[u'name'] )
        raise e
    except Exception, e:
        myLogger.error('Searh Material Error')
        raise e
    return material

def searchCategory(session, obj):
    pass

def searchCollection(session, obj):
    try:
        collection = session.query(Collection).filter(Collection.name == obj[u'name']).one()
    except NoResultFound, e:
        myLogger.error('Searh Collection Not Found: %s',obj[u'name'] )
        raise e
    except Exception, e:
        myLogger.error('Searh Collection Error')
        raise e
    return collection

def searchAndSave(session, obj):
    if not len(obj):
        return None

    if obj[u'type_name'] == u'collection':
        collection = searchCollection(session, obj)
        if collection is not None:
            for x in obj[u'orig_ids']:
                recipe = searchRecipe(session, x)
                if recipe is not None:
                    collection.recipes.append(recipe)

    elif obj[u'type_name'] == u'material':
        print "this is material"
        material = searchMaterial(session, obj)
        if material is not None:
            for x in obj[u'orig_ids']:
                recipe = searchRecipe(session, x)
                if recipe is not None:
                    material.recipes.append(recipe)

def start():
    session, engine = initSession()
    with MySQLdb.connect('172.16.1.248', 'qiye_dev', 'qiye..dev', '1188ys_resultdb') as cursor:
        #cursor = db.cursor()
        limit = 1000
        cursor.execute('''SELECT count(*) from meishi_material_recipe_relation''')
        rowCount = cursor.fetchone()[0]
        runtimes = math.ceil(rowCount/limit)

        for x in xrange(0, int(runtimes)):
            sql = "SELECT taskid, result from meishi_material_recipe_relation limit %d, %d" % (int(x*limit ), int(limit))
            cursor.execute(sql)
            allRows = cursor.fetchall()
            i = 0
            for row in allRows:
                try:
                    itemObj = json.loads(row[1])
                    searchAndSave(session, itemObj)
                    #sys.exit()
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