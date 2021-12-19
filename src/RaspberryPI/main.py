
from datetime import datetime
import json
from time import sleep

from brokerConnector import BrokerConnector
from config import Config

from inputs.senseHat import SenseHatController
#from queue.queue import RPIQueue

SLEEP_DELAY = 5.0

config = Config()

input = SenseHatController()

broker = BrokerConnector({
  'clientID' : 1,
  'host' : config.get('host'),
  'port' : config.get('port')
})
broker.run()

#queue = RPIQueue("sqlite:///database.db")

def main():
  """
  Obtiene los datos de configuración de las raspberry y los datos de los sensores del SensorHat
  Los empaqueta en un JSON y los envia al broker
  Esto lo hace de manera indefinida
  """
  import server
  while True:
    data = input.getData()
    print(json.dumps(data, indent=1))
    isPublised = broker.publish('NEW_TEST', data)
    if not isPublised:
      pass
      #queue.push(data)
    sleep(SLEEP_DELAY)

#main()