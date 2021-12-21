
from main import main
from threading import Thread

def on_starting(server):
  """
  Este código se ejecuta nada más arrancar el servidor
  
  """
  Thread(target=lambda: main()).start()