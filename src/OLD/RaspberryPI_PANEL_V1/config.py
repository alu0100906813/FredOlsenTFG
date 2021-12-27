
import json

from singletonMeta import SingletonMeta

CONFIG_FILENAME = 'config.json'

class Config(metaclass=SingletonMeta):

  """
  Se encarga de leer el fichero de configuración, y de cargar los datos de este
  También permite obtener algún dato de la configuración u obtenerlos todos
  """
  def __init__(self, config_filename = None):
    self.filename = config_filename if config_filename else CONFIG_FILENAME
    self.__read__()

  def __read__(self):
    """
    Lee todos los datos de la configuración
    """
    try:
      self.data = json.load(open(self.filename))
    except Exception as error:
      print("Ocurrió un error al intentar abrir el fichero de configuración: ", error)
      exit()
  
  def get(self, configParam):
    """
    Obtiene el valor de la configuración cuyo nombre es configParam
    EJ. nombre: "ship" y devuelve un valor de "ship1"
    """
    return self.data[configParam]

  def set(self, configParam, value):
    """
    Permite establecer una configuración. Actualiza o crea un nuevo valor
    """
    self.data[configParam] = value
    return self.data[configParam]

  def getAll(self):
    """
    Obtiene los valores de toda la configuración
    """
    return self.data.copy()

  def saveConfig(self):
    """
    Guarda la configuración en el archivo de configuración
    """
    try:
      with open(CONFIG_FILENAME, 'w') as file:
        json.dump(self.data, file)
    except Exception as e:
      print("Ocurrió un error al intentar guardar el fichero de configuración", e)