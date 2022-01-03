
from brokerConnector import BrokerConnector
import json

config = json.load(open('dbConfig.json'))

brokers = []

for brokerConfig in config['brokers']:
  #brokers.append(BrokerConnector(brokerConfig))
  pass

#BrokerConnector().run()