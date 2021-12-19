
from abc import ABC, abstractmethod

class InputsTemplate(ABC):
  def __init__(self):
    pass

  @abstractmethod
  def getData(self):
    pass