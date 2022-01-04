
from brokerConnector import BrokerConnector
import threading
import json

from dbConnector.influxdb import InfluxDB

config = json.load(open('dbConfig.json'))

database = InfluxDB(config['database'])

brokers = []

for brokerConfig in config['brokers']:
  currentBroker = BrokerConnector(brokerConfig, database.sendData)
  threading.Thread(target=currentBroker.run())
  brokers.append(currentBroker)

#BrokerConnector().run()