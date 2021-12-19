
# Se ha utilizado el tutorial: https://www.emqx.com/en/blog/how-to-use-mqtt-in-python

from paho.mqtt import client as mqtt_client

import json

DEFAULT_PORT = 1880

class BrokerConnector:
  
  def __init__(self, config = None):
    self.__config = config
    self.__client = None

  def setConfig(self, config):
    self.__config = config

  def __connect_mqtt(self):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    try:
      client = mqtt_client.Client(str(self.__config['clientID']))
      if 'username' in self.__config:
        client.username_pw_set(self.__config.username, self.__config.password)
      client.on_connect = on_connect
      client.connect(self.__config['host'], int(self.__config['port']))
      self.__client = client
      return True
    except Exception as e:
      self.client = None
      return False

  def publish(self, topic, msg):
    if not self.__client:
      if not self.run():
        return False
    newMessage = msg
    if not isinstance(msg, str): 
      newMessage = json.dumps(msg)
    result = self.__client.publish(topic, newMessage)
    status = result[0]
    if status != 0:
      #print(f"Failed to send message to topic {topic}")
      return False
    return True

  def run(self):
    self.__connect_mqtt()
    if self.__client:
      self.__client.loop_start()
      return True
    return False