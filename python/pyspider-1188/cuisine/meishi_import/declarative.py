#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-03-03 13:14:54
# Project: test
# 
import os
import sys
from sqlalchemy import Column, ForeignKey, INTEGER, String, Date, DateTime, Numeric, Boolean, Text, Table, CHAR, SmallInteger, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
from sqlalchemy.dialects.mysql import INTEGER
 
Base = declarative_base()

recipe_category = Table('recipe_category', Base.metadata,
    Column('recipe_id', INTEGER(unsigned=True), ForeignKey('recipe.id')),
    Column('cat_id', INTEGER(unsigned=True), ForeignKey('category.id'))
)

recipe_material = Table('recipe_material', Base.metadata,
    Column('material_id', INTEGER(unsigned=True), ForeignKey('material.id')),
    Column('recipe_id', INTEGER(unsigned=True), ForeignKey('recipe.id'))
)

recipe_collection = Table('recipe_collection', Base.metadata,
    Column('collection_id', INTEGER(unsigned=True), ForeignKey('collection.id')),
    Column('recipe_id', INTEGER(unsigned=True), ForeignKey('recipe.id'))
)

class Recipe(Base):
    __tablename__ = 'recipe'
    id = Column(INTEGER(unsigned=True), primary_key=True)
    name = Column(CHAR(40), nullable=False, index=True)
    picture = Column(String(3096), nullable=False, doc='具体照片： ["xxx.jpg", "xxx2.jpg"], 数组中是大图路径，小图路径可')
    cover = Column(String(255), nullable=False, doc='一个小图的封面，用于列表展示的时候读取')
    intro = Column(String(1024), nullable=True, doc='简介')
    main_material = Column(String(2048), nullable=True, doc='主料，json格式，{"鸡肉": "200克",.....}')
    condiment = Column(String(1024), nullable=True, doc='辅料,json格式')
    procedure = Column(Text, nullable=True, doc='过程，json')
    orig_id = Column(INTEGER, nullable=False)
    view = Column(INTEGER, nullable=False, default=0)
    like = Column(INTEGER, nullable=False, default=0)
    favor = Column(INTEGER, nullable=False, default=0)
    date_add = Column(DateTime, nullable=True)
    date_upd = Column(DateTime, nullable=True)
    tips = Column(Text, nullable=True)
    tool = Column(CHAR(40), nullable=True)
    # many to many 
    categories = relationship("Category", secondary=recipe_category, backref="recipes")
    materials = relationship("Material", secondary=recipe_material, backref="recipes")
    collections = relationship("Collection", secondary=recipe_collection, backref="recipes")

class Category(Base):
    __tablename__ = 'category'
    id = Column(INTEGER(unsigned=True), primary_key=True)
    name = Column(CHAR(20), nullable=False)
    cat_type = Column(CHAR(20), nullable=False, index=True, doc="主食，甜品等类别，比较固定，可以写死配置")
    url_rewrite = Column(CHAR(50), nullable=False, default='', index=True)

class Material(Base):
    __tablename__ = 'material'
    id = Column(INTEGER(unsigned=True), primary_key=True)
    name = Column(CHAR(20), nullable=False)
    nutrition = Column(String(2048), nullable=True)
    intro = Column(String(1024), nullable=True, doc="短描述")
    description = Column(Text, nullable=True, doc="营养价值长描述")
    view = Column(INTEGER, nullable=False, default=0)
    like = Column(INTEGER, nullable=False, default=0)
    favor = Column(INTEGER, nullable=False, default=0)
    date_add = Column(DateTime, nullable=True)
    material_type = Column(CHAR(20), nullable=False, index=True, doc="类型名，例如：鱼类，虾类，贝类等")
    cover = Column(String(255), nullable=True, doc="图片")



class Collection(Base):
    __tablename__ = 'collection'
    id = Column(INTEGER(unsigned=True), primary_key=True)
    name = Column(CHAR(40), nullable=False)
    orig_id = Column(INTEGER, nullable=False)
    intro = Column(Text, nullable=False)
    view = Column(INTEGER, nullable=False, default=0)
    like = Column(INTEGER, nullable=False, default=0)
    favor = Column(INTEGER, nullable=False, default=0)
    date_add = Column(DateTime, nullable=True)
    date_upd = Column(DateTime, nullable=True)



# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('mysql+mysqldb://test:test@172.16.1.19/1188meishi?charset=utf8&use_unicode=0')


# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
if __name__ == '__main__':
    Base.metadata.create_all(engine)