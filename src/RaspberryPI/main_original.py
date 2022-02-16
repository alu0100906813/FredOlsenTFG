
import time
import datetime
import json

from broker import Broker
from inputs.senseHat import SenseHatController
#from inputs.bme680 import BME680
#from inputs.mics6813 import Mics6813
#from inputs.sgp30 import Sgp30

config = None

with open('config.json', 'r') as jsonFile:
  config = json.load(jsonFile)

inputs = [SenseHatController()] #Mics6813(), Sgp30(), BME680

broker = Broker(config)

def main():
  place = f"{config['place']}/" if 'place' in config else ''
  while True:
    sensorValues = dict()
    for input in inputs:
      sensorValues = { **sensorValues, **input.getData() }
    for sensorName in sensorValues:
      broker.publish(
        f"{config['ship']}/{place}{sensorName}",
        {"value" : sensorValues[sensorName], "time" : str(datetime.datetime.utcnow())}
      )
    time.sleep(1) # Ralentizamos ya que hay un cuello de botella al insertar en la bbdd

main()
