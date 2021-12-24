
from paho.mqtt import client as mqtt_client

# Gran parte del código ha sido copiado de: https://www.emqx.com/en/blog/how-to-use-mqtt-in-python (Suscriptor)

ALL_TOPICS = '#'

broker = '127.0.0.1'

port = 1883

topic = ALL_TOPICS

# generate client ID with pub prefix randomly
client_id = '1'


class BrokerConnector():
  
  def __init__(self):
    pass

  def connect_mqtt(self) -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    #client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


  def subscribe(self, client: mqtt_client):
    def on_message(client, userdata, msg):
      print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(ALL_TOPICS)
    client.on_message = on_message


  def run(self):
    client = self.connect_mqtt()
    self.subscribe(client)
    client.loop_forever()
