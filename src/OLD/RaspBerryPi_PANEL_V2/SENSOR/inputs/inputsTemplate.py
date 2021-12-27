
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
  def getData(self):
    """
    Obtiene los datos en formato JSON del sensor para poder enviar al broker
    Cada uno de estos datos ha de enviarse por separado. Es decir, una key no puede contener un object
    Ej: {'a' : 1, 'b' : 2}
    MAL Ej: {'a' : 1, 'b' : {c : '2'}} (Ya que b es un objeto)
    """
    pass