import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric, Boolean, Text, Table
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
    Column('sep_id', Integer, ForeignKey('specialty.id')),
    Column('video_id', Integer, ForeignKey('video.id'))
)

class Video(Base):
    __tablename__ = 'video'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=True)
    rating = Column(Numeric(3,1), nullable=True)
    director = Column(String(50), nullable=True)
    runtime = Column(Integer, nullable=True)
    year = Column(Integer, nullable=True)
    location = Column(String(50), nullable=True)
    lang = Column(String(50), nullable=True)
    orig_id = Column(Integer, nullable=True)
    click_count = Column(Integer, nullable=True)
    video_type_id = Column(Integer, nullable=True)
    platform = Column(String(50), nullable=True)
    is_closed = Column(Boolean, nullable=True)
    # many to many 
    categories = relationship("Category", secondary=category_video, backref="videos")
    specialties = relationship("Specicalty", secondary=specialty_video, backref="videos")

class VideoInfo(Base):
    __tablename__ = 'video_info'
    id = Column(Integer, primary_key=True)
    video_id = Column(Integer, ForeignKey('video.id'))
    introduction =  Column(Text, nullable=True)
    poster_image = Column(String(255), nullable=True)
    small_image = Column(String(255), nullable=True)
    actors = Column(String(255), nullable=True)
    meta_title = Column(String(255), nullable=True)
     # one to one relation
    video = relationship("Video", backref=backref("video_info", uselist=False))


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=True)
    video_type_id = Column(Integer, nullable=True)
    url_rewrite = Column(String(50), nullable=True)
    is_hot = Column(Boolean, nullable=True)

class PlaySource(Base):
    __tablename__ = 'play_source'
    id = Column(Integer, primary_key=True)
    api_id =  Column(Integer, nullable=True)
    api_name = Column(String(50), nullable=True)
    url = Column(String(255), nullable=True)
    title = Column(String(255), nullable=True)
    # many to one
    video_id = Column(Integer, ForeignKey('video.id'))
    video = relationship('Video')

class Specicalty(Base):
    __tablename__ = 'specialty'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=True)
    video_type_id = Column(Integer, nullable=True)

        
        


# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///sqlalchemy_example.db')


# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
if __name__ == '__main__':
    Base.metadata.create_all(engine)