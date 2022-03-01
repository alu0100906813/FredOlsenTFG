
import pandas as pd

data = pd.read_csv('primerViaje.csv')

MAX_VALUE = 16.0
MIN_VALUE = MAX_VALUE * - 1

print("Min G Value:", MIN_VALUE)
print("Max G Value:", MAX_VALUE)

print("\nCurrent max value: ", data['Value'].max())
print("Current min value: ", data['Value'].min())

NUMBER_DATA_ITEMS = len(data['Value'])

index = -1

def filter(value):
  global index
  index = index + 1
  if value < MAX_VALUE and value > MIN_VALUE:
    return value
  lastValue = 0 if index == 0 else data['Value'][index - 1]
  nextValue = 0 if index >= NUMBER_DATA_ITEMS - 1 else data['Value'][index + 1]
  average = (lastValue + nextValue) / 2
  if average > MAX_VALUE or average < MIN_VALUE: # NOTA: Puede darse que el anterior o el siguiente también sea ruido
    average = 0
  message = "Item " + str(index) + ", has value " + str(value) + " changed to " + str(average)
  print(message)
  return average

data['Value'] = data['Value'].apply(filter)

print("\nNew max value: ", data['Value'].max())
print("New min value: ", data['Value'].min())
