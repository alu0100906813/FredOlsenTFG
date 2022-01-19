
from .inputsTemplate import InputsTemplate

from bme68x import BME68X

class BME68X(InputsTemplate):
  def __init__(self):
    try: 
      self.__bme68x = BME68X(0x76, 0) # 0x76 o 0x77 es la defecto de la bme688
      self.__bme68x.set_heatr_conf(1, 320, 100, 1) # Copiado tal cual, investigar
    except Exception as e:
      print("Ocurrió un error con el sensor BME68x", e)

  def getData(self):
    return { "BME68X" : bme68x.get_data() }