from sqlalchemy import (
    Column, Integer, Text, SmallInteger, LargeBinary
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Mailing(Base):
    __tablename__ = 'mailing'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sender = Column(Text, nullable=True)
    target_email = Column(Text, nullable=True)
    created_at = Column(Integer, nullable=True)
    sent_at = Column(Integer, nullable=True)
    subject = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    html_template = Column(Text, nullable=True)
    attachment = Column(SmallInteger, nullable=False, default=0)
    attachment_name = Column(Text, nullable=True)
    attachment_content = Column(LargeBinary, nullable=True)
    status = Column(Text, nullable=True)
