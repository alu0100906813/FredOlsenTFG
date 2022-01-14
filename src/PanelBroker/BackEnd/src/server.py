
import json
import re
import threading

from flask import Flask, request
from brokerConnector import BrokerConnector

app = Flask(__name__)

brokerConfig = {
  'host' : '192.168.1.59',
  'clientID' : '48394',
  'port' : 1883,
  'topic' : '#'
}


brokerConnectorInstance = BrokerConnector(brokerConfig)
threading.Thread(target=brokerConnectorInstance.run, args=()).start()

@app.route('/getShips')
def getShips():
  return json.dumps(list(brokerConnectorInstance.getRecivedMsgQuery().keys()))

@app.route('/getMetrics')
def getMetrics():
  metrics = request.args.get('metric')
  ship = request.args.get('ship')
  return brokerConnectorInstance.getRecivedMsgQuery()[ship][metric]
  return json.dumps(result)

@app.route('/getAllMetrics')
def getAllMetrics():
  ship = request.args.get('ship')
  return brokerConnectorInstance.getRecivedMsgQuery()[ship]

@app.route('/getAllMetricsAndShips')
def getAllMetricsAndShips():
  data = brokerConnectorInstance.getRecivedMsgQuery()
  return data


if (__name__ == '__main__'):
  app.run(debug=True)