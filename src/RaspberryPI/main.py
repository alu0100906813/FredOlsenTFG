
import time
import datetime
import json

from broker import Broker
from inputs.senseHat import SenseHatController

config = None

with open('config.json', 'r') as jsonFile:
  config = json.load(jsonFile)

inputs = [SenseHatController()]

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