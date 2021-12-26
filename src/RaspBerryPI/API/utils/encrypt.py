
from cryptography.fernet import Fernet

def generateKey():
  """
  Genera una key aleatoria para poder realizar la encriptación
  """
  return Fernet.generate_key()

class Encrypt():
  """
  Inicializa la clase. Obtiene la key y la añade a la clase
  """
  def __init__(self, key):
    self.key = Fernet(key)

  """
  Desencripta la contraseña pasada como parámetro
  """
  def decrypt(self, encryptedText):
    return self.key.decrypt(encryptedText).decode()

  """
  Encripta la contraseña que es pasada como parámetro
  Para ello, utiliza la key que tiene almacenada
  """
  def encrypt(self, plainText):
    return self.key.encrypt(plainText.encode())

  """
  Recibe dos contraseñas, una encriptada y otra desencriptada
  Compara si ambas contraseñas son las mismas
  """
  def check(self, encryptedText, plainText):
    return self.decrypt(encryptedText.encode()) == plainText