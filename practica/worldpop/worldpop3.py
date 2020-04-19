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


def run_simulation(system, update_func):
    """Simulate the system using any update function.

    system: System object
    update_func: function that computes the population next year

    returns: TimeSeries
    """
    results = TimeSeries()
    results[system.t_0] = system.p_0

    for t in linrange(system.t_0, system.t_end):
        results[t+1] = update_func(results[t], t, system)

    return results


def plot_results(census, un, timeseries, title):
    """Plot the estimates and the model.

    census: TimeSeries of population estimates
    un: TimeSeries of population estimates
    timeseries: TimeSeries of simulation results
    title: string
    """
    # primero limpiamos datos anteriores para graficar en blanco
    pyplot.clf()
    plot(census, ':', label='US Census')
    plot(un, '--', label='UN DESA')
    plot(timeseries, color='gray', label='Model')

    decorate(xlabel='Year',
             ylabel='World population (billion)',
             title=title)
    savefig('/tmp/grafico.jpg')


# estan las funciones run_simulation y plot_results igual que antes
# vamos a mejorar un poco la de calculo de step, o update_func
# ya hablamos sobre que algunos parámetros podemos calcularlos
# a tanteo, prueba y error, hasta dar en el clavo, o algo que se aproxime
# mejor al sistema real de lo que teníamos
# una forma de hacerlo fue usar dos valores de alpha para rangos de fechas
# vamos a ver otra, suponiendo un solo valor de alpha
# vamos a cambiar la forma de la curva llevandola a una función cuadrática
# un polinomio de grado 2

def update_func_quad(pop, t, system):
    """Compute the population next year with a quadratic model.
    
    pop: current population
    t: current year
    system: system object containing parameters of the model
    
    returns: population next year
    """

    net_growth = system.alpha * pop + system.beta * pop**2
    return pop + net_growth

"""
Ahí tenemos una función cuadratica de la poblacion
un parametro alpha multiplicado por la variable pop
un parametro beta multiplicado por la variable pop elevada al cuadrado
( ** es potencia en python )
La pregunta es: qué valor le damos a beta?
Y la respuesta: a prueba y error... si lo dejamos en 0, es lo mismo que no tenerlo.
Probemos algunos valores y vemos qué va pasando"""

# cargamos los datos iniciales (acá no los tengo en este archivo .py)
t_0 = get_first_label(census)
t_end = get_last_label(census)
p_0 = census[t_0]

system = System(t_0 = t_0,
        t_end = t_end,
        p_0 = p_0,
        alpha = 0.025,
        beta = -0.0018)

#beta en 1 por probar (ya se que va a dar culquier cosa xD

# simulamos:
results = run_simulation(system, update_func_quad)
plot_results(census, un, results, 'Modelo cuadratico')
















