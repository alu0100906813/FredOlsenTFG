
from sense_emu import SenseHat
from .inputsTemplate import InputsTemplate

class SenseHatController(InputsTemplate):
  """
  Contiene el controlador del SenseHat
  """
  def __init__(self):
    try:
      self.senseHat = SenseHat()
    except Exception as e:
      print("Ocurrió un error con el SenseHat. Compruebe que está correctamente instalado o el emulador activado")

  def __getPressure(self):
    """
    Obtiene la presión del SensorHat
    """
    return self.senseHat.get_pressure()

  def __getTemperature(self):
    """
    Obtiene la temperatura del SensorHat
    """
    return self.senseHat.get_temperature()

  def __getHumidity(self):
    """
    Obtiene la humedad del SensorHat
    """
    return self.senseHat.get_humidity()

  def __getOrientation(self):
    """
    Obtiene la orientación del SensorHat
    Es decir, la guiñada, el cabeceo, y el alabeo
    """
    orientation = self.senseHat.get_orientation()
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
    acceleration = self.senseHat.get_accelerometer_raw()
    return {
      'x' : acceleration['x'],
      'y' : acceleration['y'],
      'z' : acceleration['z']
    }

  def getData(self):
    """
    Obtiene todos los valores del SensorHat y los junta en un JSON
    Además, también añade la fecha y hora en la que se han obtenido estos datos
    """
    orientation = self.__getOrientation()
    acceleration = self.__getAcceleration()
    return {
        'pressure' : self.__getPressure(),
        'temperature' : self.__getTemperature(),
        'humidity' : self.__getHumidity(),
        'accelerationX' : acceleration['x'],
        'accelerationY' : acceleration['y'],
        'accelerationZ' : acceleration['z'],
        'orientationPitch' : orientation['pitch'],
        'orientationRoll' : orientation['roll'],
        'orientationYaw' : orientation['yaw']
    }