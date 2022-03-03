
import pandas as pd

data = pd.read_csv('primerViaje.csv')

MAX_VALUE = 16.0
MIN_VALUE = MAX_VALUE * - 1

# Valores máximos y mínimos de la aceleración a calcular
print("Min G Value:", MIN_VALUE)
print("Max G Value:", MAX_VALUE)

# Máximo y mínimo valor de la columna SIN filtrado
print("\nCurrent max value: ", data['Value'].max())
print("Current min value: ", data['Value'].min())

NUMBER_DATA_ITEMS = len(data['Value'])

index = -1
invalidValues = 0

"""
  En la columna actual, vemos si el valor sobrepasa el máximo o mínimo
  En cuyo caso lo sustituimos por la media del anterior y el posterior valor
  Puede darse el caso de que el anterior o el siguiente valor también estén fuera de rango
  En cuyo caso la media puede dar fuera de rango también. Si eso ocurre, sustituimos por 0
"""
def filter(value):
  global index, invalidValues
  index += 1
  if value < MAX_VALUE and value > MIN_VALUE:
    return value
  invalidValues += 1
  lastValue = 0 if index == 0 else data['Value'][index - 1]
  nextValue = 0 if index >= NUMBER_DATA_ITEMS - 1 else data['Value'][index + 1]
  average = (lastValue + nextValue) / 2
  if average > MAX_VALUE or average < MIN_VALUE: # NOTA: Puede darse que el anterior o el siguiente también sea ruido
    average = 0
  message = "Item " + str(index) + ", has value " + str(value) + " changed to " + str(average)
  print(message)
  return average

data['Value'] = data['Value'].apply(filter)

index = 0

def changeTime(time):
  global index
  index += 1
  return index

#data['Time'] = data['Time'].apply(changeTime)

# Máximo y mínimo valor de la columna DESPUÉS del filtrado
print("\nNew max value: ", data['Value'].max())
print("New min value: ", data['Value'].min())

# Numero de valores cambiados
print("Values changed: ", invalidValues)

OUTPUT_NAME_FILE = 'filtrado.xlsx'

#data.to_csv(OUTPUT_NAME_FILE, index=False)

data.to_excel(OUTPUT_NAME_FILE, index=False)

print('Fichero de salida: ', OUTPUT_NAME_FILE)