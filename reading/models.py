from sqlalchemy import Boolean, Integer, Column, UnicodeText, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from .constants import API_KEY_LENGTH
from .utils import random_string


Base = declarative_base()


class BulkMessage(Base):
    __tablename__ = 'bulk_message'
    id = Column(Integer, primary_key=True)
    message = Column(UnicodeText)
    recipients = relationship("SentMessage")


class SentMessage(Base):
    __tablename__ = 'sent_message'
    id = Column(Integer, primary_key=True)
    bulk_message_id = Column(Integer, ForeignKey('bulk_message.id'))
    story_id = Column(Integer, ForeignKey('story.id'))
    message = Column(UnicodeText)


class Story(Base):
    __tablename__ = 'story'
    id = Column(Integer, primary_key=True)
    title = Column(UnicodeText)
    story_text = Column(UnicodeText)
    messages_sent = relationship("SentMessage")


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(UnicodeText, nullable=False)
    administrator = Column(Boolean, unique=False, default=False)
    api_key = Column(UnicodeText, unique=True)
    active = Column(Boolean, default=True, unique=False)


class Database(object):
    """ An abstraction of a database object, in case we want to support other down the line """

    def __init__(self, engine):
        self.engine = engine
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def drop_tables(self):
        Base.metadata.drop_all(self.engine)

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def add_user(self, email, administrator, api_key=None):
        if not api_key:
            api_key = random_string(API_KEY_LENGTH)
        user = User(email=email, administrator=administrator, api_key=api_key, active=True)
        self.session.add(user)
        self.session.commit()
