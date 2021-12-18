
from cryptography.fernet import Fernet

def generateKey():
  return Fernet.generate_key()

class Encrypt():

  def __init__(self, key):
    self.key = Fernet(key)

  def decrypt(self, encryptedText):
    return self.key.decrypt(encryptedText).decode()

  def encrypt(self, plainText):
    return self.key.encrypt(plainText.encode())

  def check(self, encryptedText, plainText):
    return self.decrypt(encryptedText.encode()) == plainText