from declarative import Base, Category, Video, VideoInfo
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

engine = create_engine('sqlite:///sqlalchemy_example.db')
Base.metadata.bind = engine
DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()
 # Return the first Person from all Persons in the database
try:
    video = session.query(Video).filter(Video.name == 'new video').one()
except NoResultFound, e:
    print  e
else:
    print video.name
#person = session.query(Person).first()
#print person.name
