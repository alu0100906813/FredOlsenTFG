
# Se ha utilizado el tutorial: https://www.emqx.com/en/blog/how-to-use-mqtt-in-python

from paho.mqtt import client as mqtt_client
import json

from singletonMeta import SingletonMeta

"""
Puerto por defecto, en el caso de que no se envie un puerto como parámetro
"""
DEFAULT_PORT = 1880

class BrokerConnector(metaclass=SingletonMeta):
  
  def __init__(self, config = None):
    """
    Inicializa la clase. Recibe un objeto que contiene la configuración del IOT
    En este se encuentra la ID del cliente, y la dirección junto con el puerto
    """
    self.__config = config
    self.__client = None
    self.__isConnected = False

  def setConfig(self, config):
    """
    Permite cambiar el objeto del que se obtiene la configuración.
    """
    self.__config = config


  def __connect_mqtt(self):
    """
    Realiza la conexión al servidor MQTT.
    Para ello, asigna los parámetros de configuración al objeto MQTT
    Y se encarga también de realizar la conexión a este
    """
    result = None
    def on_connect(client, userdata, flags, rc):
      self.__isConnected = True

    def on_disconnect(client, userdata, rc):
      self.__isConnected = False

    try:
      self.__client = mqtt_client.Client(str(self.__config['clientID']))
      if 'username' in self.__config:
        client.username_pw_set(self.__config.username, self.__config.password)
      self.__client.on_connect = on_connect
      self.__client.on_disconnect = on_disconnect
      self.__client.connect(self.__config['host'], int(self.__config['port']))
    except Exception as e:
      pass

  def publish(self, topic, msg):
    """
    Publica un "Topic" hacia el servidor MQTT
    En caso de que no esté conectado el servidor, retorna False
    En caso contrario retorna True
    """
    if not self.__isConnected:
      return False
    newMessage = msg
    if not isinstance(msg, str): 
      newMessage = json.dumps(msg)
    result = self.__client.publish(topic, newMessage)
    status = result[0]
    if status != 0:
      #print(f"Failed to send message to topic {topic}")
      return False
    return True

  def run(self):
    """
    Se encarga de arrancar el servidor MQTT
    Genera un bucle infinito que permite que en caso de que se desconecte
    Se intente conectar constantemente
    """
    self.__connect_mqtt()
    self.__client.loop_start()

  def disconnect(self):
    """
    Se desconecta del servidor, y para ello, cierra el bucle creado en run
    """
    self.__client.loop_stop()
    self.__client.disconnect()

  def reboot(self):
    """
    Se encarga de reiniciar la conexión con el servidor MQTT
    """
    self.disconnect()
    self.run()

  def brokerIsConnected(self):
    """
    Devuelve si está conectado al broker o no
    En caso de que NO haya conexión al broker, pues devolverá False
    En caso contrario, devolverá True
    """
    return self.__isConnected