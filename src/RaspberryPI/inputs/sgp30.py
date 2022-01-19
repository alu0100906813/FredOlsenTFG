
from .inputsTemplate import InputsTemplate

from sgp30 import SGP30

# sudo pip install pimoroni-sgp30
# https://github.com/pimoroni/sgp30-python

class SGP30(InputsTemplate):
  def __init__(self):
    try:
      self.__sgp30 = SGP30()
    except Exception as e:
      print("Ocurrió un error al intentar ejecutar el sensor SGP30", e)

  def getData(self):
    return { "SGP30" : self.__sgp30.get_air_quality() }