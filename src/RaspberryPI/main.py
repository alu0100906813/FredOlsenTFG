
import time
import datetime
import json

from broker import Broker
from inputs.senseHat import SenseHatController

config = None

with open('config.json', 'r') as jsonFile:
  config = json.load(jsonFile)

input = SenseHatController()

broker = Broker(config)

def main():
  place = f"{config['place']}/" if 'place' in config else ''
  while True:
    sensorValues = input.getData()
    for sensorName in sensorValues:
      broker.publish(
        f"{config['ship']}/{place}{sensorName}",
        {"value" : sensorValues[sensorName], "time" : str(datetime.datetime.now())}
      )
    time.sleep(1.5) # Ralentizamos ya que hay un cuello de botella al insertar en la bbdd

main()