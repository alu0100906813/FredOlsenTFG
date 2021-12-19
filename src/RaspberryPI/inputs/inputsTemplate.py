
from abc import ABC, abstractmethod

class InputsTemplate(ABC):
  """
  Contiene una plantilla para poder añadir classes que obtienen datos de sensores
  Como por ejemplo, una clase para obtener valores de SensorHat, otra para obtener valores de un GPS, etc
  Estas clases hederaría de esta clase
  """
  def __init__(self):
    pass

  @abstractmethod
  """
  Obtiene los datos en formato JSON del sensor para poder enviar al broker
  """
  def getData(self):
    pass