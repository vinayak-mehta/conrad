# -*- coding: utf-8 -*-

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
ID_LEN = 100
STR_LEN = 1024


class Event(Base):
    __tablename__ = "event"

    id = Column(String(ID_LEN), primary_key=True)
    name = Column(String(STR_LEN))
    url = Column(String(STR_LEN))
    city = Column(String(STR_LEN))
    state = Column(String(STR_LEN))
    country = Column(String(STR_LEN))
    cfp_open = Column(Boolean, default=False)
    cfp_start_date = Column(DateTime)
    cfp_end_date = Column(DateTime)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    source = Column(String(STR_LEN))
    tags = Column(Text)
    kind = Column(String(STR_LEN))


class Reminder(Base):
    __tablename__ = "reminder"

    id = Column(String(ID_LEN), ForeignKey("event.id"), primary_key=True)
