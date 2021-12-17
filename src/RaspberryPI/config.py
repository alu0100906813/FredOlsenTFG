
import json

CONFIG_FILENAME = 'config'

class Config:
  def __init__(self, config_filename = None):
    self.filename = config_filename if config_filename else CONFIG_FILENAME
    self.__read__()

  def __read__(self):
    try:
      self.data = json.load(open(self.filename))
    except Exception as error:
      print("Ocurrió un error al intentar abrir el fichero de configuración: ", error)
      exit()

  def get(self, configParam):
    return self.data[configParam]

  def getAll(self):
    return self.data.copy()