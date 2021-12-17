
from time import sleep
from datetime import datetime
import json

from brokerConnector import BrokerConnector
from sense_emu import SenseHat
from config import Config

SLEEP_DELAY = 5.0

config = Config()

broker = BrokerConnector({
  'clientID' : 1,
  'host' : config.get('host'),
  'port' : config.get('port')
})
broker.run()

senseHat = None

try:
  senseHat = SenseHat()
except Exception as e:
  print("Ocurrió un error con el SenseHat. Compruebe que está correctamente instalado o el emulador activado")

def getCurrentTime():
  """
  Devuelve el tiempo actual parseado. Mostrando la fecha y hora completa
  """
  return datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")

def getPressure():
  """
  Obtiene la presión del SensorHat
  """
  return senseHat.get_pressure()

def getTemperature():
  """
  Obtiene la temperatura del SensorHat
  """
  return senseHat.get_temperature()

def getHumidity():
  """
  Obtiene la humedad del SensorHat
  """
  return senseHat.get_humidity()

def getOrientation():
  """
  Obtiene la orientación del SensorHat
  Es decir, la guiñada, el cabeceo, y el alabeo
  """
  orientation = senseHat.get_orientation()
  return {
    'pitch' : orientation['pitch'],
    'roll' : orientation['roll'],
    'yaw' : orientation['yaw']
  }

def acceleration():
  """
  Obtiene la aceleración del SensorHat
  En sus tres ejes, x, y, z
  """
  acceleration = senseHat.get_accelerometer_raw()
  return {
    'x' : acceleration['x'],
    'y' : acceleration['y'],
    'z' : acceleration['z']
  }

def getJSONData():
  """
  Obtiene todos los valores del SensorHat y los junta en un JSON
  Además, también añade la fecha y hora en la que se han obtenido estos datos
  """
  return {
      'time' : getCurrentTime(),
      'pressure' : getPressure(),
      'temperature' : senseHat.get_temperature(),
      'humidity' : senseHat.get_humidity(),
      'orientation' : getOrientation(),
      'acceleration' : acceleration()
  }

def mergeDict(firstDict, secondDict):
  """
  Une dos diccionarios de Python en uno solo
  """
  return {**firstDict, **secondDict}

def main():
  """
  Obtiene los datos de configuración de las raspberry y los datos de los sensores del SensorHat
  Los empaqueta en un JSON y los envia al broker
  Esto lo hace de manera indefinida
  """
  while True:
    data = getJSONData()
    data = mergeDict(data, config.getAll())
    print(json.dumps(data, indent=1))
    broker.publish('NEW_TEST', data)
    sleep(SLEEP_DELAY)

main()