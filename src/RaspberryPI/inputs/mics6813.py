
# https://github.com/pimoroni/mics6814-python
# sudo raspi-config nonint do_i2c 0
# sudo pip3 install pimoroni-mics6814

from .inputsTemplate import InputsTemplate

from mics6814 import MICS6814

class MICS6813(InputsTemplate):
  def __init__(self):
    try:
      self.__MICS6813 = mics6813()
    except Except as e:
      print("Ocurrió un error con el sensor del gas (MICS6813)", e)

  def getData(self):
    return { "MICS6813" : self.__MICS6813.read_all()}