
# Se ha utilizado el tutorial: https://www.emqx.com/en/blog/how-to-use-mqtt-in-python

from paho.mqtt import client as mqtt_client

# max_queued_messages_set(self, queue_size)

import json

"""
Puerto por defecto, en el caso de que no se envie un puerto como parámetro
"""
DEFAULT_PORT = 1883

class BrokerConnector():
  
  def __init__(self, config):
    self.__config = config
    self.__connected = False
  

  def __connect_mqtt(self):
    def on_connect(client, userdata, flags, rc):
      if rc == 0:
        print("Connected to MQTT Broker!")
        self.__connected = True
      else:
        print("Failed to connect, return code %d\n", rc)

    self.__client = mqtt_client.Client(str(self.__config['clientID']))
    #self.__client.username_pw_set(username, password)
    self.__client.on_connect = on_connect
    self.__client.connect(self.__config['host'], self.__config['port'])


  def publish(self, topic, value, ship, time):
    result = self.__client.publish(topic, json.dumps({'value' : value, 'ship' : ship, 'time' : str(time) }), qos=2)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{value}` to topic `{topic}` in `{time}`")
        self.__connected = True
    else:
        print(f"Failed to send message to topic {topic}")
        self.__connected = False


  def run(self):
    self.__connect_mqtt()
    self.__client.loop_start()


  def isConnected(self):
    return self.__connected