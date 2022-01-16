
import json
import re
import threading

from flask import Flask, request
from flask_mqtt import Mqtt

#from brokerConnector import BrokerConnector

brokerConfig = {
  'host' : '192.168.1.59',
  'clientID' : '48394',
  'port' : 1883,
  'topic' : '#'
}

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = brokerConfig['host']
app.config['MQTT_BROKER_PORT'] = brokerConfig['port']
#app.config['MQTT_USERNAME'] = 'user'
#app.config['MQTT_PASSWORD'] = 'secret'
app.config['MQTT_REFRESH_TIME'] = 1.0  # refresh time in seconds
mqtt = Mqtt(app)

mqtt_data = dict()

#brokerConnectorInstance = BrokerConnector(brokerConfig)
#threading.Thread(target=brokerConnectorInstance.run, args=()).start()


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
  mqtt.subscribe('#')


@mqtt.on_message()
def handle_mqtt_message(client, userdata, msg):
  topics = re.findall('(\w+)', msg.topic)
  copy_mqtt_data = mqtt_data
  for topic in topics[:-1]:
    if not topic in copy_mqtt_data:
      copy_mqtt_data[topic] = dict()
    copy_mqtt_data = copy_mqtt_data[topic]
  copy_mqtt_data[topics[-1]] = json.loads(msg.payload.decode())


@app.route('/getShips')
def getShips():
  return json.dumps(list(mqtt_data.keys()))


@app.route('/getMetrics')
def getMetrics():
  metrics = request.args.get('metric')
  ship = request.args.get('ship')
  return mqtt_data[ship][metric]
  return json.dumps(result)


@app.route('/getAllMetrics')
def getAllMetrics():
  ship = request.args.get('ship')
  return mqtt_data[ship]


@app.route('/getAllMetricsAndShips')
def getAllMetricsAndShips():
  return mqtt_data


if (__name__ == '__main__'):
  app.run(debug=True, use_reloader=False)