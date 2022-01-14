
# https://github.com/influxdata/influxdb-client-python

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.exceptions import InfluxDBError
from influxdb_client.client.write_api import ASYNCHRONOUS, SYNCHRONOUS

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
        self.__queryApi = self.__client.query_api()
        return
      except Exception as e:
        print(e)

  def query(self, queryString):
    return self.__queryApi.query(org=self.__config['organization'], query=queryString)