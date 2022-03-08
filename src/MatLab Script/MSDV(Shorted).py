
import pandas as pd

import matplotlib.pyplot as plt

from math import sqrt

TIME_INCREMENT = 0.1

data = pd.read_excel('primerViajeFiltrado.xlsx')

#mean = data['Value'].mean()

mean = 0.01765

index = 0

timeAccumulator = 0.0
MSDVAccumulator = 0.0

data['MSDV'] = 0.0

def calculateMSDV(row):
  global index, timeAccumulator, TIME_INCREMENT, MSDVAccumulator, mean
  #mean = data['Value'][0:index].mean()
  MSDV = mean * sqrt(timeAccumulator)
  timeAccumulator += TIME_INCREMENT
  index += 1
  #MSDVAccumulator += MSDV
  return MSDV

data['MSDV'] = data['MSDV'].apply(calculateMSDV)

data['NewTime'] = 0.0

timeAccumulator = 0.0

def generateNewTime(row):
  global timeAccumulator, TIME_INCREMENT
  timeAccumulator += TIME_INCREMENT
  return timeAccumulator - TIME_INCREMENT

data['NewTime'] = data['NewTime'].apply(generateNewTime)

#newData = pd.DataFrame()
#newData['NewTime'] = data['NewTime'][2400:40000]
#newData['MSDV'] = data['MSDV'][2400:40000]

data.plot(x = 'NewTime', y = 'MSDV', kind = 'line')

plt.xlabel("Tiempo (s)")
plt.ylabel("MSDV")

plt.title("Viaje ida")

plt.show()

#print(data)
