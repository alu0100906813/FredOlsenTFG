
from datetime import datetime
import json
from time import sleep

from brokerConnector import BrokerConnector
from config import Config

from inputs.senseHat import SenseHatController
from RPIQueue import RPIQueue

SLEEP_DELAY = 3.0

def publishStoredMessages():
  """
  Se encarga de publicar mensajes al Broker
  Estos mensajes son los que anteriormente no se han podido enviar
  Y se encuentran guardados en la Base de Datos
  """
  for i in range(0, 10): # Cambiar el 10 por variable global o algo
    if queue.getLength() == 0:
      break
    data = queue.pop()
    if not broker.publish('NEW_TEST', data): # Cambiar new test
      queue.push(data)

def main():
  """
  Inicializa el programa. Para ello, obtiene datos de sensores y los envia
  al broker de forma infinita. En caso de que no se envie, los envía a la cola
  """
  import server
  while True:
    data = input.getData()
    #print(json.dumps(data, indent=1))
    #print(queue.getLength())
    if not broker.publish('NEW_TEST', data): # Cambiar new test
      queue.push(data)
    publishStoredMessages()
    sleep(SLEEP_DELAY)

if __name__ == '__main__':
  config = Config()

  input = SenseHatController()

  broker = BrokerConnector({
    'clientID' : 1,
    'host' : config.get('host'),
    'port' : config.get('port')
  })
  broker.run()

  queue = RPIQueue("sqlite:///database.db")
  main()