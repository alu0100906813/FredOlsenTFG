
import numpy
import scipy.integrate as integrate
import math

aw = input("Introduzca el valor de AW: ")

try:
  aw = float(aw)
except:
  print("El valor de AW tiene que ser flotante")
  exit(-1)

time = input("Introduzca el intervalo de tiempo en centisegundos: ")

try:
  time = int(time)
except:
  print("El valor del tiempo tiene que ser entero")
  exit(-1)

time = int(time / 10) # Pasamos a segundos, ya que el muestreo es de 10 datos por segundo

awPowTwo = pow(aw, 2)
integralFromZeroToTime = integrate.quad(lambda x : awPowTwo, 0, time)

MSDV = math.sqrt(integralFromZeroToTime[0])

print("El valor de MSDV es de ", MSDV)