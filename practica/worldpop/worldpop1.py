#!/usr/bin/python

from modsim import *
from matplotlib import pyplot
from pandas import read_html        #Pandas proporciona funciones para trabajar con datos. La función que usamos es read_html, para leer una página web y extraer los datos de cualquier tabla

fd = 'https://en.wikipedia.org/wiki/Estimates_of_historical_world_population'   #direccion de la pagina donde extraemos los valores de la tabla

tables = read_html(fd, header=0, index_col=0, decimal='M')
"""read_html guarda todas las tablas de la pagina web, en la variable tables
fd: desde donde leer (puede ser un site, puede ser un file)
header: qué fila vamos a considerar cabeceras
index_col: qué columna vamos a considerar índice de la tabla
decimals: esto es para decir si vamos a usar '.' o ',' para
separar decimales... en mi caso vamos a hacer un "truco" usando M de millones de personas para que los datos no sean tan grandes (ya van a ver cómo sale)"""

# cargamos la tercer tabla (index 2 de tables)
table2 = tables[2]    #tables[0] tiene los valores de la primer tabla del sitio, tables[1] tiene los valores de la segunda tabla del sitio, y asi..

# mostramos a ver qué sale:
# head muestra las primeras 5 filas por default
# se puede pasar un arg a head para mostrar más o menos.
print(table2.head())

# vamos a cambiar los nombres de las columnas (headers, cabeceras) porque en la wiki son muy largos y se va a complicar para usarlos aca:
table2.columns = [ 'census' , 'prb' , 'un' , 'maddison' ,'hyde' , 'tanton' , 'biraben' , 'mj' ,'thomlinson' , 'durand' , 'clark' ]

# ahora podemos extraer algunos datos puntuales:
# "census" es la primer columna, la de los datos de censo de USA
# "un" es la columna de los datos de naciones unidas
census = table2.census / 1e9
un = table2.un / 1e9
# dividirlo por 1e9 hace que no muestre la notación cientifica, son cifras muy grandes
# vamos a suponer que los valores son "miles de millones"
# por ejemplo: 2.525149e+09 equivale a decir:
# 2.525149 miles de millones de personas

print("Valores de USA..........................")
print(census)
print("Valores de NU...........................")
print(un)

# grafiquemos a ver qué sale:
pyplot.clf()   #borra la configuracion actual
plot(census, ':', label='Censo')   # el ":" es para hacer linea de puntos
plot(un, '--', label='NU')         # el "--" es para hacer linea de rayas
decorate(xlabel='Year', ylabel='World population (billion)', title="Poblacion")
savefig('/home/fernando/Escritorio/github/MODELOS Y SIMULACION/practica/worldpop.jpg')

"""
Las dos curvas van casi juntas, y en los primeros años, casi son lineales
podríamos considerarlo un sistema lineal, con crecimiento constante
y generar un modelo lineal que se intente aproximar lo mas posible a la curva
Podríamos calcular el crecimiento promedio anual, y con eso hacer una recta desde 1950 a ver qué sale... al final deberían coincidir en el 2016
pero no sabemos qué va a pasar en el medio, si se va a representar bien o no el modelo con la recta.
"""
total_growth = census[2016] - census[1950]   # esto seria el crecimiento total de la población mundial
print(total_growth)

# para evitar hardcodear datos, podemos ayudarnos con algunas funciones:
t_0 = get_first_label(census)   # tiempo inicial
t_end = get_last_label(census)  # tiempo final
elapsed_time = t_end - t_0      # diferencia de tiempos
print("Tiempos: %d %d" % (t_0, t_end))

# calculemos el crecimiento promedio anual ahora:
p_0 = get_first_value(census)   # población inicial: (por cierto, estamos usando censo como base ahora)
p_end = get_last_value(census)  # poblacion final
total_growth = p_end - p_0
print("Crecimiento total: " + str(total_growth))

# promedio:
annual_growth = total_growth / elapsed_time
print("Crecimiento anual: " + str(annual_growth))

results = TimeSeries()       # vamos a usar el TimeSeries que ya conocemos de las clases anteriores
results[t_0] = census[t_0]   # cargamos el valor inicial del timeseries, el valor de 1950

# ahora simulamos el sistema desde 1950, sumando a cada año el crecimiento promedio anual, durante todos los años hasta 2016
for t in linrange(t_0, t_end):                 #Devuelve una matriz de valores espaciados uniformemente en un intervalo, funcion declarada en modsim
    results[t+1] = results[t] + annual_growth

# graficamos a ver qué sale ahora:
plot(results, '-', label='Model') # el "-" es para linea continua
decorate(xlabel='Year', ylabel='World population (billion)', title="Crecimiento constante")
savefig('/home/fernando/Escritorio/github/MODELOS Y SIMULACION/practica/worldpop1.jpg')
# conclusion de la grafica: el modelo (linea recta) se aleja bastante de los datos del sistema entre 1950 - 1990

# vamos a graficar iniciando en el ano 1970 para ver si el modelo se acerca mejor a los datos del sistema
t_0 = 1970
t_end = get_last_label(census)
elapsed_time = t_end - t_0

p_0 = census[1970]
p_end = get_last_value(census)
total_growth = p_end - p_0
annual_growth = total_growth / elapsed_time

results1 = TimeSeries()
results1[t_0] = census[t_0]
for t in linrange(t_0, t_end):
    results1[t+1] = results1[t] + annual_growth

plot(results1, '-', label='Model+', color='red') # no me acuerdo el color xD
decorate(xlabel='Year', ylabel='World population (billion)', title="Crecimiento constante")
savefig('/home/fernando/Escritorio/github/MODELOS Y SIMULACION/practica/worldpop2.jpg')
# conclusion de la grafica: al iniciar desde el ano 1970, el modelo se aproxima mucho mas a los datos del sistema, casi se superponen las 2 graficas de los censos y la el modelo.


















