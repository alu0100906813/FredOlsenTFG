
# https://www.emqx.com/en/blog/how-to-use-mqtt-in-python

from paho.mqtt import client as mqtt_client

class Broker():

  def __init__(self, config):
    self.__client = None
    self.__config = config
    self.__connect()

  def __connect(self):
    def on_connect(client, userdata, flags, rc):
      if rc == 0:
        print("Connected to MQTT Broker!")
      else:
        print("Failed to connect, return code %d\n", rc)

    self.__client = mqtt_client.Client(str(self.__config['clientID']))
    #self.__client.username_pw_set(username, password)
    self.__client.on_connect = on_connect
    self.__client.connect(self.__config['host'], self.__config['port'])

  def __run(self):
    self.__connect()
    self.__client.loop_start()

  def publish(self, topic, msg):
    result = self.__client.publish(topic, str(msg))
    status = result[0] # result: [0, 1]
    if status == 0:
      print(f"Send `{msg}` to topic `{topic}`")
    else:
      print(f"Failed to send message to topic {topic}")