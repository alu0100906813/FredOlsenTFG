
import json

CONFIG_FILENAME = 'config.json'

class Config:
  _instance = None

  # https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
  def __new__(class_, *args, **kwargs):
    if not class_._instance:
        class_._instance = object.__new__(class_, *args, **kwargs)
    return class_._instance

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

  def getAll(self):
    """
    Obtiene los valores de toda la configuración
    """
    return self.data.copy()

  def getByKey(self, keys):
    pass