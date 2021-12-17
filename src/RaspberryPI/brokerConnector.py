
import requests

HOST = 'http://localhost'
PORT = 1880
DIR = 'SenseHat'

URL = HOST + ':' + str(PORT) + '/' + DIR

class BrokerConnector:
  
  def __init__(self, url = None):
    self.setHost(url if url is not None else URL)

  def setHost(self, url):
    self.url = url

  def sendData(self, data):
    try:
      result = requests.post(self.url, data = data)
    except requests.exceptions.ReadTimeout: 
      pass