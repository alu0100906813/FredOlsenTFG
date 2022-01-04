
# https://github.com/influxdata/influxdb-client-python

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.exceptions import InfluxDBError
from influxdb_client.client.write_api import ASYNCHRONOUS

import json
import re

from .dbConnector import DBConnector

SEPARATE_TOPICS = '(\w+)'



class BatchingCallback(object):

    def success(self, conf: (str, str, str), data: str):
        print(f"Written batch: {conf}, data: {data}")

    def error(self, conf: (str, str, str), data: str, exception: InfluxDBError):
        print(f"Cannot write batch: {conf}, data: {data} due: {exception}")

    def retry(self, conf: (str, str, str), data: str, exception: InfluxDBError):
        print(f"Retryable error occurs for batch: {conf}, data: {data} retry: {exception}")




class InfluxDB():

  def __init__(self, config):
    self.__config = config
    self.connect()
    super()

  def connect(self):
    while True:
      try:
        self.__client = InfluxDBClient(
          url=self.__config['host'], 
          token=self.__config['token'],
          org=self.__config['organization']
        )
        print("Connected to InfluxDB Database!")
        callback = BatchingCallback()
        self.__writeAPI = self.__client.write_api(
            success_callback=callback.success,
            error_callback=callback.error,
            retry_callback=callback.retry,
            write_options=ASYNCHRONOUS
        )
        return
      except Exception as e:
        print(e)

  def __parse(self, mqttTopic, mqttMessage):
    topicValues = re.findall(SEPARATE_TOPICS, mqttTopic)
    mqttMessageJSON = json.loads(mqttMessage)
    return Point("".join(topicValues[1:])).tag('IOD_ID', topicValues[0]).field('value', mqttMessageJSON['value']).time(mqttMessageJSON['time'])

  def sendData(self, topic, message, bucket):
    self.__writeAPI.write(bucket=bucket, record=self.__parse(topic, message))