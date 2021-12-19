
from datetime import datetime
import json
from time import sleep

from brokerConnector import BrokerConnector
from config import Config

from inputs.senseHat import SenseHatController
from RPIQueue.RPIQueue import RPIQueue

SLEEP_DELAY = 3.0

config = Config()

input = SenseHatController()

broker = BrokerConnector({
  'clientID' : 1,
  'host' : config.get('host'),
  'port' : config.get('port')
})
broker.run()

queue = RPIQueue("sqlite:///database.db")

def publishStoredMessages():
  for i in range(0, 10): # Cambiar el 10 por variable global o algo
    if queue.getLength() == 0:
      break
    data = queue.pop()
    if not broker.publish('NEW_TEST', data): # Cambiar new test
      queue.push(data)

def main():
  #import server
  while True:
    data = input.getData()
    #print(json.dumps(data, indent=1))
    print(queue.getLength())
    isPublised = broker.publish('NEW_TEST', data) # Cambiar new test
    if not isPublised:
      queue.push(data)
    publishStoredMessages()
    sleep(SLEEP_DELAY)

main()