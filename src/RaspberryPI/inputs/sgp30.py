
import re

from .inputsTemplate import InputsTemplate

from sgp30 import SGP30

# sudo pip install pimoroni-sgp30
# https://github.com/pimoroni/sgp30-python

SEPARATOR_REGEX = '([^:]+):\s*(\d+)\s*\((\w+)'

class Sgp30(InputsTemplate):
  def __init__(self):
    try:
      self.__sgp30 = SGP30()
    except Exception as e:
      print("Ocurrió un error al intentar ejecutar el sensor SGP30", e)

  def getData(self):
    result = str(self.__sgp30.get_air_quality()).split('\n')
    result.pop(0) # La primera línea no aporta ningún valor
    result = [re.findall(SEPARATOR_REGEX, item) for item in result]
    result.pop() # Al hacer el regex, nos da un item vacío de más
    return {item[0][0] : int(item[0][1]) for item in result}
    #return { "SGP30" : self.__sgp30.get_air_quality() }
