
# "sqlite:///database.db"

from model import QueueTable, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import json

class Queue():

  def __init__(self):
    engine = create_engine("sqlite:///database.db")
    Base.metadata.create_all(engine)
    self.session = sessionmaker(bind=engine)()
    self.queueLength = self.session.query(QueueTable).count()

  def push(self, msg, id = None):
    newMessage = QueueTable(msg=msg, id=id)
    self.session.add(newMessage)
    self.session.commit()

  def pop(self):
    row = self.session.query(QueueTable).first()
    if row is not None:
      self.session.delete(row)
      self.session.commit()
      row = row.__dict__
    return row

  def isEmpty(self):
    return self.queueLength is 0

  def getLength(self):
    return self.queueLength
