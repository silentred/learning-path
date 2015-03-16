#!/usr/bin/python
## -*- encoding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from declarative import  Base, Video, VideoInfo, Category, PlaySource, Specicalty
 
engine = create_engine('sqlite:///sqlalchemy_example.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()
 
# one to one
# video = Video(name='new video')
# session.add(video)
# session.commit()
# video_info = VideoInfo(video=video)
# session.add(video_info)
# session.commit()

# many to many
# video2 = Video(name='video2')
# cat1 = Category(name="cat 1")
# cat2 = Category(name="cat 2")
# video2.categories.append(cat1)
# video2.categories.append(cat2)
# session.add(video2)
# session.add(cat1)
# session.add(cat2)
 

video = session.query(Video).filter(Video.name == 'new video').one()
#cat2 = session.query(Category).filter(Category.name =='cat 2').one()
#video.categories.append(cat2)
#video.categories.remove(cat2)

# insert many objects once
# play_source1 = PlaySource(api_name='youku', video=video, url='http://www.asdf.com')
# play_source2 = PlaySource(api_name='tudou', video=video, url='http://www.tudou.com')
# session.add_all([ play_source1, play_source2])

# sep1 = Specicalty(name="love")
# sep2 = Specicalty(name="comody")
# session.add_all([sep1, sep2])
# video.specialties.append(sep2)

#session.commit()
