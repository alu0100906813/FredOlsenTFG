
# https://github.com/influxdata/influxdb-python

from influxdb import InfluxDBClient
import json

from .dbConnector import DBConnector

class InfluxDB():

  def __init__(self, DBData):
    super()

  def connect(self, DBData):
    try 
      self.client = InfluxDBClient(DBData['host'], DBData['port'], DBData['username'], DBData['password'], DBData['bucker'])
    except Exception e:
      self.connect(DBData) # Cuidado de se puede quedar dentro de un loop infinito
      pass

  # ESTO HAY QUE VERLO MEJOR
  def __parse(self, mqttTopic, mqttMessage):
    mqttMessageJSON = json.loads(mqttMessage)
    return {
      'measurement' : mqttTopic,
      'tags' : {
        'IOT_ID' : mqttMessage['id']
      },
      'time' : mqttMessage['time'],
      'fields' : {
        'value' : mqttMessage['value']
      }
    }

  def sendDB(self, message):
    self.client.write_points(self.__parse(message))