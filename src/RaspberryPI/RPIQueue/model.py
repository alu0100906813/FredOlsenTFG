
from sqlalchemy import Table, Column, Integer, JSON, MetaData
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class QueueTable(Base):
  __tablename__ = 'queuemodel'

  id = Column(Integer, primary_key=True)
  msg = Column(JSON, nullable=False)