
# Copiado de: https://refactoring.guru/es/design-patterns/singleton/python/example#example-1
# Produce un Singleton que es tolerante a multihilos

from threading import Lock, Thread

class SingletonMeta(type):

  _instances = {}

  _lock: Lock = Lock()

  def __call__(cls, *args, **kwargs):
    """
    Implementa un patrón Singleton compatible con multihilos
    """
    with cls._lock:
      if cls not in cls._instances:
        instance = super().__call__(*args, **kwargs)
        cls._instances[cls] = instance
    return cls._instances[cls]