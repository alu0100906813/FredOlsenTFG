
import re

def checkIfIsNotEmpty(string):
  """
  Comprueba si una cadena está o no está vacía
  """
  return re.search("\S+", string) is not None

def deleteSpacesStartEnd(string):
  """
  Elimina los espacios al final y al comienzo de un string
  """
  result = re.search("^\s*(\S*)\s*$", string)
  return result.group(1)