
# https://github.com/pimoroni/mics6814-python
# sudo raspi-config nonint do_i2c 0
# sudo pip3 install pimoroni-mics6814

from .inputsTemplate import InputsTemplate
from mics6814 import MICS6814

class Mics6813(InputsTemplate):
  def __init__(self):
    try:
      self.__MICS6814 = MICS6814()
    except Exception as e:
      print("Ocurrió un error con el sensor del gas (MICS6813)", e)

  def getData(self):
    return {
      "oxidising" : self.__MICS6814.read_oxidising(),
      "reducing" : self.__MICS6814.read_reducing(),
      "nh3" : self.__MICS6814.read_nh3(),
      "adc" : self.__MICS6814.read_adc()
    }
    #return { "MICS6814" : str(self.__MICS6814.read_all())}
