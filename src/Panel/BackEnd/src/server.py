
import json
import re

from flask import Flask, request
from influxdb import InfluxDB

from utils import parseQuery, sampleQuery

app = Flask(__name__)

database = InfluxDB({
  "host" : "192.168.1.59:8086",
  "token" : "StW2p6rNxhayzaGZ93aS-QA0GvR8WTwd9xAOXTCXfWDKcjaiWGCKEjdJSPj8kjCJN6I3azFRW8ApTDQShYPjkw==",
  "organization" : "FredOlsen"
})

@app.route('/getMetrics')
def getMetrics():
  metrics = request.args.get('metrics')
  # (\w+),?
  print(metrics)
  result = parseQuery(database.query(sampleQuery(metrics)))
  return json.dumps(result)

if (__name__ == '__main__'):
  app.run(debug=True)