
import time
import datetime
import json
import signal

#from broker import Broker
from inputs.senseHat import SenseHatController
#from inputs.bme680 import BME680
#from inputs.mics6813 import Mics6813
#from inputs.sgp30 import Sgp30

from mysql import MySql

RED_LED = (255, 0, 0)
GREEN_LED = (0, 255, 0)

config = None

with open('config.json', 'r') as jsonFile:
  config = json.load(jsonFile)

inputs = [SenseHatController()] #Mics6813(), Sgp30(), BME680

#broker = Broker(config)

database = MySql()

def stop(signum, frame):
  inputs[0].changeColor(RED_LED)
  time.sleep(3)
  inputs[0].changeColor()
  exit(0)

signal.signal(signal.SIGINT, stop)

def main():
  #place = f"{config['place']}/" if 'place' in config else ''
  try:
    inputs[0].changeColor(GREEN_LED)
    while True:
      sensorValues = dict()
      for input in inputs:
        sensorValues = { **sensorValues, **input.getData() }
      for sensorName in sensorValues:
        """
        broker.publish(
          f"{config['ship']}/{place}{sensorName}",
          {"value" : sensorValues[sensorName], "time" : str(datetime.datetime.utcnow())}
        )
        """
        database.insertData(sensorName, sensorValues[sensorName], str(datetime.datetime.utcnow()))
  except Exception as e:
    print(e)
    stop(None, None)

main()
