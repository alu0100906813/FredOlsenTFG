
from .inputsTemplate import InputsTemplate

import bme680

class BME680(InputsTemplate):

  def __init__(self):
    try: 
      try:

        self.__sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)

      except (RuntimeError, IOError):

        self.__sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

        self.__sensor.set_humidity_oversample(bme680.OS_2X)
        self.__sensor.set_pressure_oversample(bme680.OS_4X)
        self.__sensor.set_temperature_oversample(bme680.OS_8X)
        self.__sensor.set_filter(bme680.FILTER_SIZE_3)
        self.__sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

    except Exception as e:
      print("Ocurrió un error con el sensor BME68x", e)
    
  def getData(self):
    if self.__sensor.get_sensor_data():
      jsonResponse = {
        "temperature" : self.__sensor.data.temperature,
        "pressure" : self.__sensor.data.pressure,
        "humidity" : self.__sensor.data.humidity
      }
      if self.__sensor.data.heat_stable:
        jsonResponse["gasResistance"] = self.__sensor.gas_resistance
      return jsonResponse
    return dict()