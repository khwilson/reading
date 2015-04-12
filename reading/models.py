from sqlalchemy import Integer, Column, UnicodeText, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


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
