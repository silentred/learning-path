import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric, Boolean, Text, Table, CHAR, SmallInteger, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
 
Base = declarative_base()

VTYPE = {
    'movie' : 1,
    'comic' : 2,
    'tv' : 3,
    'variety' : 4
}
 
category_video = Table('category_video', Base.metadata,
    Column('cat_id', Integer, ForeignKey('category.id')),
    Column('video_id', Integer, ForeignKey('video.id'))
)

specialty_video = Table('specialty_video', Base.metadata,
    Column('spe_id', Integer, ForeignKey('specialty.id')),
    Column('video_id', Integer, ForeignKey('video.id'))
)

class Video(Base):
    __tablename__ = 'video'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, index=True)
    rating = Column(Numeric(3,1), nullable=False)
    director = Column(CHAR(30), nullable=False, default='')
    runtime = Column(Integer, nullable=True, default=0)
    year = Column(Integer, nullable=True, default=0, index=True)
    location = Column(CHAR(20), nullable=False, default='', index=True)
    lang = Column(CHAR(20), nullable=False, default='')
    orig_id = Column(Integer, nullable=False)
    click_count = Column(Integer, nullable=True, default=0)
    video_type_id = Column(Integer, nullable=True, index=True)
    platform = Column(CHAR(10), nullable=True)
    is_closed = Column(Boolean, nullable=True, default=True, index=True)
    # many to many 
    categories = relationship("Category", secondary=category_video, backref="videos")
    specialties = relationship("Specicalty", secondary=specialty_video, backref="videos")

class VideoInfo(Base):
    __tablename__ = 'video_info'
    id = Column(Integer, primary_key=True)
    video_id = Column(Integer, ForeignKey('video.id'), index=True)
    introduction =  Column(Text, nullable=False, default='')
    poster_image = Column(String(255), nullable=False, default='')
    small_image = Column(String(255), nullable=False, default='')
    actors = Column(String(255), nullable=False, default='')
    meta_title = Column(String(255), nullable=False, default='')
    alias = Column(String(255), nullable=False, default='')
    upd_desc = Column(String(255), nullable=False, default='')
     # one to one relation
    video = relationship("Video", backref=backref("video_info", uselist=False))


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    video_type_id = Column(Integer, nullable=False, index=True)
    url_rewrite = Column(String(50), nullable=False, default='', index=True)
    is_hot = Column(Boolean, nullable=False, default=0)
    is_displayed= Column(Boolean, nullable=False, default=0, index=True)

class PlaySource(Base):
    __tablename__ = 'play_source'
    id = Column(Integer, primary_key=True)
    #api_id =  Column(Integer, nullable=True)
    api_name = Column(CHAR(15), nullable=True)
    url = Column(String(255), nullable=False)
    episode_num = Column(Integer, nullable=True)
    # many to one
    video_id = Column(Integer, ForeignKey('video.id'))
    video = relationship('Video')

class Specicalty(Base):
    __tablename__ = 'specialty'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, default='')
    video_type_id = Column(Integer, nullable=False)

class TVPlot(Base):
    __tablename__='tv_plot'
    id = Column(Integer, primary_key=True)
    video_id = Column(Integer, ForeignKey('video.id'), nullable=False)
    content =  Column(Text, nullable=False, default='')
    episode_num = Column(SmallInteger, nullable=True)
    # many to one
    video = relationship("Video", backref=backref("tv_plot"))
        
class VarietySource(Base):
    __tablename__= 'variety_source'
    id = Column(Integer, primary_key=True)
    #api_id =  Column(Integer, nullable=True)
    api_name = Column(CHAR(30), nullable=True)
    url = Column(String(355), nullable=False)
    title = Column(CHAR(100), nullable=True)
    guests = Column(String(255), nullable=False, default='')
    date = Column(Date, nullable=False)
    small_image = Column(String(255), nullable=False, default='')
    # many to one
    video_id = Column(Integer, ForeignKey('video.id'))
    video = relationship('Video')

class IndexItem(Base):
    __tablename__= 'index_item'
    id = Column(Integer, primary_key=True)
    video_type_id =  Column(Integer, nullable=False, index=True)
    section  = Column(CHAR(15), nullable=False)
    sub_section = Column(CHAR(15), nullable=True)
    video_id = Column(Integer, ForeignKey('video.id'))
    title = Column(CHAR(20), nullable=False)
    desc =  Column(CHAR(40), nullable=False)
    cover = Column(String(255), nullable=False)
    big_cover = Column(String(255), nullable=True)
    broadcast_time = Column(CHAR(40), nullable=True)
    long_desc = Column(String(150), nullable=True)

class RankItem(Base):
    __tablename__= 'rank_item'
    id = Column(Integer, primary_key=True)
    video_type_id =  Column(Integer, nullable=False, index=True)
    section  = Column(CHAR(15), nullable=False)
    video_id = Column(Integer, ForeignKey('video.id'))
    position = Column(SmallInteger, nullable=False)
    


# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('mysql+mysqldb://test:test@192.168.2.50/1188test?charset=utf8&use_unicode=0')


# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
if __name__ == '__main__':
    Base.metadata.create_all(engine)