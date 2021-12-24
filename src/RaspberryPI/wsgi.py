
from threading import Thread

from main import main
from server import app

Thread(target=lambda: main()).start()