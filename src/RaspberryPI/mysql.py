
"""
Note: This class was created to catch 
"""

# sudo apt-get install python-dev libmysqlclient-dev

# pip install mysqlclient

# sudo mysql –u root –p

# The code to create and insert data in the database

"""
CREATE DATABASE RPI;
USE RPI;
CREATE TABLE SENSORHAT (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  sensor VARCHAR(32),
  value FLOAT,
  time DATETIME
);
CREATE USER 'rpi'@'localhost' IDENTIFIED BY 'fran5287';
GRANT ALL PRIVILEGES ON RPI.SENSORHAT TO 'rpi'@'localhost';
INSERT INTO SENSORHAT (value, sensor, time) VALUES (0.3454, 'a', STR_TO_DATE("10-17-2021 15:40:10", "%m-%d-%Y %H:%i:%s"));
"""

import MySQLdb

DEFAULT_CONFIG = {
  'user'     : 'rpi',
  'password' : 'fran5287',
  'host'     : 'localhost',
  'database' : 'RPI'
}

connection = None

class MySql():
  def __init__(self, config = DEFAULT_CONFIG):
    self.__connect(config)
    
  def __connect(self, config):
    while True: # Don't stop until the connection is successful
      try:
        self.__conection = MySQLdb.connect(**DEFAULT_CONFIG)
        self.__cursor = self.__conection.cursor()
        break
      except Exception as e:
        print(e)

  def insertData(self, sensor, value, time):
    query = 'INSERT INTO SENSORHAT  (sensor, value, time) VALUES (%s, %s, %s);'
    try:
      result = self.__cursor.execute(query, (sensor, value, time,))
      self.__conection.commit()
      print("Inserted!")
    except Exception as e:
      print("Query not inserted:", e)

  def close(self):
    self.__conection.close()