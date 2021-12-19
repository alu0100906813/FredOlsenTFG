
# "sqlite:///database.db"

from sqlalchemy import create_engine, Table, Column, Integer, JSON, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base

from singletonMeta import SingletonMeta

import json

Base = declarative_base()

class QueueTable(Base):
  """
  Contiene el modelo SQL para poder almacenar los datos que no se envian
  al MQTT a una base de datos local
  """
  __tablename__ = 'queuemodel'

  id = Column(Integer, primary_key=True)
  msg = Column(JSON, nullable=False)

class RPIQueue(metaclass=SingletonMeta):

  def __init__(self, engineData):
    """
    Se encarga de inicializar la cola. Conecta a la base de datos (Local)
    y posteriormente, carga el modelo y compruba cuantos items hay en la cola
    """
    engine = create_engine(engineData)
    Base.metadata.create_all(engine)
    self.session = sessionmaker(bind=engine)()
    self.queueLength = self.session.query(QueueTable).count()

  def push(self, msg, id = None):
    """
    Se encarga de poner en la cola el mensaje recibido como parámetro.
    Lo introduce al final de la cola
    """
    newMessage = QueueTable(msg=msg, id=id)
    self.session.add(newMessage)
    self.session.commit()
    self.queueLength = self.queueLength + 1

  def pop(self):
    """
    Se encarga de extraer el último elemento de la base de datos y devolverlo
    En caso de que no haya ningún elemento, devuelve None
    """
    row = self.session.query(QueueTable).first()
    if row is not None:
      self.session.delete(row)
      self.session.commit()
      row = row.__dict__
      del row['_sa_instance_state']
      self.queueLength = self.queueLength - 1 
    return row

  def isEmpty(self):
    """
    Devuelve si la cola está vacia o no
    """
    return self.queueLength is 0

  def getLength(self):
    """
    Obtiene los elementos que actualmente se encuentran en la cola
    """
    return self.queueLength
