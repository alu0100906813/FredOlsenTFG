
from datetime import datetime
import json
import requests
from time import sleep

from brokerConnector import BrokerConnector

from inputs.senseHat import SenseHatController

SLEEP_DELAY = 1.0

frontEndHost = 'http://localhost'
frontEndPort = 5000
frontEndURL = frontEndHost + ':' + str(frontEndPort)

config = dict()

def getConfig():
  try:
    response = requests.get(frontEndURL + '/updateConfig')
  except Exception as e:
    print(e)
    return False
  if(response.status_code != 200):
    print(response.status_code)
    return False
  global config
  config = response.json()
  return True

def updateBackend(status):
  try:
    response = requests.post(frontEndURL + '/updateStatus', params={'status' : status})
  except Exception as e:
    print(e)

def main():
  """
  Inicializa el programa. Para ello, obtiene datos de sensores y los envia
  al broker de forma infinita. En caso de que no se envie, los envía a la cola
  Por cada mensaje se envia: Topic, valor, datetime (Cuando se recogió el dato) y ship
  """
  while not getConfig():
    pass
  broker = BrokerConnector({
  'clientID' : config['id'],
  'host' : config['host'],
  'port' : int(config['port'])
  })
  broker.run()
  
  while True:
    data = list(input.getData().items())
    now = datetime.now()
    for topicValue in data: # 0 es el Topic, y 1 es el Valor
      broker.publish(topicValue[0], topicValue[1], config['ship'], now)
    updateBackend(broker.isConnected())
    sleep(SLEEP_DELAY)

input = SenseHatController()

main()