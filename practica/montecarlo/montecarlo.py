import numpy as np # importando numpy
from scipy import stats # importando scipy.stats
import pandas as pd # importando pandas
import decimal

np.random.seed(0) # para poder replicar el random
datos = [33,18,27,36,25,24,30,23,29,38,23,22,19,21,18,28,12,20,22,22,22,34,32,15,14,16,32,17,22,37,11,22,37,15,29,11,36,24,18,19,23,12,21,7,30,6,26,31,24,31,25,21,25,21,24,30,29,18,19,16,17,20,24,18,19,43,9,37,32,26,25,18,16,14,23,37,31,34,21,22,26,16,24,22,25,32,11,30,30,17,18,36,14,31,24,35,12,19,17,21,28,14,22,39,27,18,33,39,30,32,26,32,19,35,26,20,23,23,23,23,11,20,15,19,33,23,40,25,18,16,20,23,20,31,23,20,38,30,19,15,6,23,23,21,17,27,19,23,44,19,23,20,24,22,18,23,21,16,10,23,26,27,29,21,13,32,22,27,28,35,24,16,14,25,32,22,32,24,33,32,32,25,24,28,23,16,27,27,10,32,13,29,27,22,17,25,33,46,17,35,17,20,22,30,31,27,21,32,18,19,25,26,20,33,19,30,11,34,34,32,24,30,26,28,29,19,21,21,30,26,25,18,22,21,37,24,25,35,18,16,29,25,20,26,28,32,16,15,42,29]
datos_random = np.random.rand(100) # genera un vector con datos random

 # ordena el vector con los 250 datos historicos del sitio web
acu=0
acu2=0
sum_acu=0
sum_acu2=0
datos2 = [] # en este vector se guardan los valores que resultan de la relacion entre los valores random contra la acumulada normalizada, que se correlaciona con el mayor inmediatamente superior del vector datos con los valores historicos
acu_nor_temp=[]

datos.sort()

for x in datos:
  sum_acu=sum_acu+x # sumataria de todos los valores del vector datos historicos

print("Val x  ", "P(x)    ", "Ac(x) Nor")
for x in datos:
  acu=acu+x # acumulada
  acu_nor = acu / sum_acu # acumulada normalizada
  acu_nor_temp.append(acu/sum_acu) # guarda los datos de la acumulada normalizada en el vector acu_nor_temp
  print(x, "{:.4f}".format(x/250), "{:.4f}".format(acu_nor), sep="      ")

# por cada valor random generado, barre el vector de la acumulada normalizada (acu_nor_temp) comparando cual es el inmediato superior y lo relaciona con el correspondiente Val x
print("Val Rand --->", "Val x    ")
for x in range(len(datos_random)):
    for y in range(len(acu_nor_temp)):
        if datos_random[x] > acu_nor_temp[y]:
            if datos_random[x] < acu_nor_temp[y+1]:
                print("{:.4f}".format(datos_random[x]), datos[y+1], sep="        ")
                datos2.append(datos[y+1])

datos2.sort()

for x in datos2:
  sum_acu2=sum_acu2+x

# Para el vector nuevo, se vuelven a calcular los promedios y la acumulada
print("Val x (Rand)", "P(x) (Rand)   ", "Ac(x) Nor (Rand)", sep="  ")
for x in datos2:
  acu2=acu2+x
  acu_nor2 = acu2 / sum_acu2
  print(x, "{:.4f}".format(x/100), "{:.4f}".format(acu_nor2), sep="           ")

