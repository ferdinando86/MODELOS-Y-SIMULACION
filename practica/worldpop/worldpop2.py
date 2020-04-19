#!/usr/bin/python

from modsim import *
from matplotlib import pyplot
from pandas import read_html

fd = 'https://en.wikipedia.org/wiki/Estimates_of_historical_world_population'

tables = read_html(fd, header=0, index_col=0, decimal='M')

table2 = tables[2]

table2.columns = [ 'census' , 'prb' , 'un' , 'maddison' ,'hyde' , 'tanton' , 'biraben' , 'mj' ,'thomlinson' , 'durand' , 'clark' ]

census = table2.census /1e9
un = table2.un /1e9

t_0 = get_first_label(census)
t_end = get_last_label(census)
elapsed_time = t_end - t_0
p_0 = get_first_value(census)
p_end = get_last_value(census)
total_growth = p_end - p_0
annual_growth = total_growth / elapsed_time

"""Hasta acá todo lo de arriba es lo mismo que ya teniamos antes recolección de datos, settings de variables principales, etc
No está la simulacion porque vamos a "intentar" mejorarla
Vamos a usar algunos objetos nuevos de modsym:
    State: para gestionar las variables de estado, el estado va a ir cambiando segun evolucione el modelo
    System: contiene variables del sistema, no suelen cambiar a lo largo del modelado, como los parametros"""

# creamos un objeto System:
system = System(t_0 = t_0,
                t_end = t_end,
                p_0 = p_0,
                annual_growth = annual_growth)
# ese seria el system de nuestro modelo, los parametros que vamos a considerar por el momento (luego agregamos mas)


# creamos una funcion también para graficar:
def plot_results(census, un, timeseries, title, save):
    """Plot the estimates and the model.
    census: TimeSeries of population estimates
    un: TimeSeries of population estimates
    timeseries: TimeSeries of simulation results
    title: string"""
    # primero limpiamos datos anteriores para graficar en blanco
    pyplot.clf()
    plot(census, ':', label='US Census')
    plot(un, '--', label='UN DESA')
    plot(timeseries, color='gray', label='Model')

    decorate(xlabel='Year',
             ylabel='World population (billion)',
             title=title)
    savefig(save)


def run_simulation1(system):
    """Runs the constant growth model.                                                                                                 
    system: System object
    returns: TimeSeries"""
    results = TimeSeries()
    results[system.t_0] = system.p_0
    
    for t in linrange(system.t_0, system.t_end):
        results[t+1] = results[t] + system.annual_growth
    
    return results

# es mas o menos lo que habiamos hecho antes, pero ahora encapsulado en una funcion
# le pasamos los parametros por argumento
# la funcion calcula el crecimiento constante/lineal igual que antes
# retorna el resultado (objeto timeseries)

# lo mismo, ordenamos todo lo que tiene que ver con graficacion en una fc.
# le pasamos los datos a graficar, el timeseries, y el titulo del grafico
# veamos si esto está funcionando:
# noten el run_simulation1 <- (ese 1 vamos a modificarlo mas adelante)
results = run_simulation1(system)
plot_results(census, un, results, "Modelo de crecimiento constante", '/home/fernando/Escritorio/github/MODELOS Y SIMULACION/practica/worldpop-simulation1.jpg')


# hasta ahora igual que antes, modelo lineal, crecimiento constante
# veamos cómo podemos redefinir la funcion run_simulation1 para que
# considere las tasas de nacimiento y de mortalidad
# las tasas van a venir dentro del objeto system del parametro
# v2
def run_simulation2(system):
    """Runs the constant growth model.
    system: System object
    returns: TimeSeries"""
    results = TimeSeries()
    results[system.t_0] = system.p_0

    for t in linrange(system.t_0, system.t_end):
        births = system.birth_rate * results[t]         # nacimientos como producto de la poblacion actual y la tasa
        deaths = system.death_rate * results[t]         # lo mismo con las muertes
        results[t + 1] = results[t] + births - deaths   # las tasas ahora las creamos en el obj system (mas abajo)

    return results

# cargamos los valores para probar la simulación
# estos son valores tipicos que se supone que calculamos teniendo en cuenta los datos historicos
system.death_rate = 0.01
system.birth_rate = 0.027

# probamos simular:
results = run_simulation2(system)
plot_results(census, un, results, "Crecimiento proporcional (tasas)", '/home/fernando/Escritorio/github/MODELOS Y SIMULACION/practica/worldpop-simulation2.jpg')


# hagamos una funcion similar al "step" que teniamos con las bicis
# algo que nos facilite el calculo de cada nuevo valor de la poblacion
# acá tambien la voy a numerar 1, 2, etc, así optimizamos eso tambien

def update_func1(pop, t, system):
    """ Calcular la poblacion de un año al siguiente
    pop: poblacion actual
    t: año actual
    system: objeto con los parametros del sistema
    returns: poblacion en el siguiente año"""
    births = system.birth_rate * pop
    deaths = system.death_rate * pop
    return pop + births - deaths

# esa seria la funcion que calcula un step en la simulacion
# si bien no está usando el t, lo vamos a dejar porque puede servirnos
# para calcular poblaciones con varios sistemas en paralelo (en adelante)
# veamos si funciona con update_func1
results = run_simulation(system, update_func1)
plot_results(census, un, results, 'Crecimiento proporcional (refactored)', '/home/fernando/Escritorio/github/MODELOS Y SIMULACION/practica/worldpop-simulation3.jpg')


# refactorizamos un poquito más
# vamos a combinar los nacimientos y las muertes en una sola tasa
# en modelos poblacionales a esta tasa en general se la denomina "alpha"
system.alpha = system.birth_rate - system.death_rate   # con eso tenemos las dos tasas combinadas en una, alpha, por lo que el cambio poblacional ahora depende solamente de alpha

# nueva versión de update_func:
def update_func2(pop, t, system):
    """ Calcular la poblacion de un año al siguiente
    pop: poblacion actual
    t: año actual
    system: objeto con los parametros del sistema
    returns: poblacion en el siguiente año"""
    # calculamos el crecimiento/disminucion neta de la poblacion
    # crecimiento o disminucion depende de qué tasa sea mayor
    net_growth = system.alpha * pop
    return pop + net_growth

# veamos si funciona con update_func2
results = run_simulation(system, update_func2)
plot_results(census, un, results, 'Crecimiento proporcional (refactored)', '/home/fernando/Escritorio/github/MODELOS Y SIMULACION/practica/worldpop-simulation4.jpg')


# la nueva versión de la funcion run_simulation sería algo asi (final)
def run_simulation(system, update_func):
    """Simulate the system using any update function.
    system: System object
    update_func: function that computes the population next year
    returns: TimeSeries"""
    results = TimeSeries()
    results[system.t_0] = system.p_0

    for t in linrange(system.t_0, system.t_end):
        results[t + 1] = update_func(results[t], t, system)   # acá estamos llamando a la funcion de step

    return results