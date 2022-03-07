
import pandas as pd

import matplotlib.pyplot as plt

from math import sqrt

TIME_INCREMENT = 0.1

data = pd.read_excel('segundoViajeFiltrado.xlsx')

mean = data['Value'].mean()

timeAccumulator = 0.0
MSDVAccumulator = 0.0

data['MSDV'] = 0.0

def calculateMSDV(row):
  global index, timeAccumulator, TIME_INCREMENT, MSDVAccumulator
  MSDV = mean * sqrt(timeAccumulator)
  timeAccumulator += TIME_INCREMENT
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

data.plot(x = 'NewTime', y = 'MSDV', kind = 'line')

plt.xlabel("Tiempo (cs)")
plt.ylabel("MSDV")

plt.title("Resultados segundo viaje")

plt.show()

#print(data)

#print(mean)