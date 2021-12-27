
def getCurrentTime():
  """
  Devuelve el tiempo actual parseado. Mostrando la fecha y hora completa
  """
  return datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")