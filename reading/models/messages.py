from sqlalchemy import Integer, Column, UnicodeText, ForeignKey
from sqlalchemy.org import relationship

from .base import Base



class BulkMessage(Base):
    __tablename__ = 'bulk_message'
    id = Column(Integer, primary_key=True)
    message = Column(UnicodeText)
    recipients = relationship("SentMessage")


class SentMessage(Base):
    __tablename__ = 'sent_message'
    id = Column(Integer, primary_key=True)
    bulk_message_id = Column(Integer, ForeignKey('bulk_message.id'))
    message = Column(UnicodeText)
