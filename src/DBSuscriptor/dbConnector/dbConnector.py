
# Esta es una clase abstracta que permite conectarte a la base de datos (InfluxDB)

from abc import ABC, abstractmethod

class DBConnector(ABC):
  
  def __init__(self):
    pass

  @abstractmethod
  def connect(self, DBData):
    pass

  @abstractmethod
  def sendData(self):
    pass