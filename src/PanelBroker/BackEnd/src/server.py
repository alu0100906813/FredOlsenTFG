
import eventlet
import json
import re
import threading
import copy

from flask import Flask, request
from flask_mqtt import Mqtt

from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap

# La mayor parte sacado de: https://github.com/stlehmann/Flask-MQTT

eventlet.monkey_patch()

brokerConfig = None

try:
  brokerConfig = json.loads(open('config.json').read())
except Exception as e:
  print("Error al intentar abrir el fichero de configuración: ", e)

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = brokerConfig['host']
app.config['MQTT_BROKER_PORT'] = brokerConfig['port']
#app.config['MQTT_USERNAME'] = 'user'
#app.config['MQTT_PASSWORD'] = 'secret'
app.config['MQTT_REFRESH_TIME'] = 1.0  # refresh time in seconds

mqtt = None

while True:
  try:
    mqtt = Mqtt(app)
    break
  except Exception as e:
    print(e)

socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")
bootstrap = Bootstrap(app)

Ships = []

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
  mqtt.subscribe('#')


@socketio.on('subscribe')
def handle_subscribe(json_str):
  data = json.loads(json_str)
  mqtt.subscribe(data)


@socketio.on('unsubscribe_all')
def handle_unsubscribe_all():
  mqtt.unsubscribe_all()


@mqtt.on_message()
def handle_mqtt_message(client, userdata, msg):
  global mqtt_data
  topics = re.findall('(\w+)', msg.topic)
  mqtt_data = dict()
  #print(msg.topic, msg.payload.decode())
  for topic in topics[:-1]:
    if not topic in mqtt_data:
      mqtt_data[topic] = dict()
    mqtt_data = mqtt_data[topic]
  mqtt_data['/'.join(topics[1:])] = json.loads(msg.payload.decode())
  global Ships
  if topics[0] not in Ships:
    Ships.append(topics[0])
  socketio.emit(topics[0], data=mqtt_data)


@app.route('/getShips')
def getShips():
  global Ships
  return json.dumps(Ships)

"""
@app.route('/getShipPosition')
def getShipPosition():
  ship = request.args.get('ship')
  if ship in mqtt_data and 'lat' in mqtt_data and 'lon' in mqtt_data:
    return {"lat" : mqtt_data[ship]["lat"], "lon" : mqtt_data[ship]["lon"]}
  return {}
"""

if (__name__ == '__main__'):
  socketio.run(app, host='127.0.0.1', port=5000, debug=True, use_reloader=False)