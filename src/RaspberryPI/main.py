
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
  while True:
    sensorValues = input.getData()
    for sensorName in sensorValues:
      broker.publish(
        f"{config['ship']}/{sensorName}",
        {"value" : sensorValues[sensorName], "time" : str(datetime.datetime.now())}
      )

main()