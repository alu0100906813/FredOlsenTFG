
from paho.mqtt import client as mqtt_client

# Gran parte del código ha sido copiado de: https://www.emqx.com/en/blog/how-to-use-mqtt-in-python (Suscriptor)

ALL_TOPICS = '#'

class BrokerConnector():
  
  def __init__(self, config, databaseInsertFunction):
    self.__config = config
    self.__databaseInsertFunction = databaseInsertFunction

  def connect_mqtt(self) -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(str(self.__config['clientID']))
    #client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(self.__config['host'], self.__config['port'])
    return client


  def subscribe(self, client: mqtt_client):
    def on_message(client, userdata, msg):
      print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
      self.__databaseInsertFunction(msg.topic, msg.payload.decode(), self.__config['bucket'])

    client.subscribe(ALL_TOPICS)
    client.on_message = on_message


  def run(self):
    client = self.connect_mqtt()
    self.subscribe(client)
    client.loop_forever()
