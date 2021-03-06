
from sense_emu import SenseHat
from .inputsTemplate import InputsTemplate

class SenseHatController(InputsTemplate):
  """
  Contiene el controlador del SenseHat
  """
  def __init__(self):
    try:
      self.__senseHat = SenseHat()
    except Exception as e:
      print("Ocurrió un error con el SenseHat. Compruebe que está correctamente instalado o el emulador activado")

  def __getPressure(self):
    """
    Obtiene la presión del SensorHat
    """
    return self.__senseHat.get_pressure()

  def __getTemperature(self):
    """
    Obtiene la temperatura del SensorHat
    """
    return self.__senseHat.get_temperature()

  def __getHumidity(self):
    """
    Obtiene la humedad del SensorHat
    """
    return self.__senseHat.get_humidity()

  def __getOrientation(self):
    """
    Obtiene la orientación del SensorHat
    Es decir, la guiñada, el cabeceo, y el alabeo
    """
    orientation = self.__senseHat.get_orientation()
    return {
      'pitch' : orientation['pitch'],
      'roll' : orientation['roll'],
      'yaw' : orientation['yaw']
    }

  def __getAcceleration(self):
    """
    Obtiene la aceleración del SensorHat
    En sus tres ejes, x, y, z
    """
    acceleration = self.__senseHat.get_accelerometer_raw()
    return {
      'x' : acceleration['x'],
      'y' : acceleration['y'],
      'z' : acceleration['z']
    }

  def changeColor(self, color = None):
    if color is not None:
      self.__senseHat.clear(color)
    else:
      self.__senseHat.clear()

  def getData(self):
    """
    Obtiene todos los valores del SensorHat y los junta en un JSON
    Además, también añade la fecha y hora en la que se han obtenido estos datos
    """
    #orientation = self.__getOrientation()
    acceleration = self.__getAcceleration()
    return {
        #'pressure' : self.__getPressure(),
        #'temperature' : self.__getTemperature(),
        #'humidity' : self.__getHumidity(),
        #'acceleration/X' : acceleration['x'],
        #'acceleration/Y' : acceleration['y'],
        'acceleration/Z' : acceleration['z'],
        #'orientation/Pitch' : orientation['pitch'],
        #'orientation/Roll' : orientation['roll'],
        #'orientation/Yaw' : orientation['yaw']
    }