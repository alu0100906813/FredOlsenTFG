
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
    if not broker.publish(data['topic'], data['msg'], data['ship'], data['time']): # Cambiar new test
      queue.push(data['topic'], data['msg'], data['ship'], data['time'])

def main():
  """
  Inicializa el programa. Para ello, obtiene datos de sensores y los envia
  al broker de forma infinita. En caso de que no se envie, los envía a la cola
  Por cada mensaje se envia: Topic, valor, datetime (Cuando se recogió el dato) y ship
  """
  import server
  while True:
    data = list(input.getData().items())
    now = datetime.now()
    for topicValue in data: # 0 es el Topic, y 1 es el Valor
      if not broker.publish(topicValue[0], topicValue[1], config.get('ship'), now): # Cambiar new test
        queue.push(topicValue[0], topicValue[1], config.get('ship'), now)
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