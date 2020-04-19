#!/usr/bin/python

from modsim import *
np.random.seed(7)

def step(state, p1, p2):
    """Simulate one minute of time.
    state: bikeshare State object
    p1: probability of an Olin->Wellesley customer arrival
    p2: probability of a Wellesley->Olin customer arrival"""
    if flip(p1):
        bike_to_wellesley(state)

    if flip(p2):
        bike_to_olin(state)

def bike_to_wellesley(state):
    """Move one bike from Olin to Wellesley.
    state: bikeshare State object"""
    if state.olin == 0:
        state.olin_empty +=1
        return

    state.olin -= 1
    state.wellesley += 1

def bike_to_olin(state):
    """Move one bike from Wellesley to Olin.
    state: bikeshare State object"""
    if state.wellesley == 0:
        state.wellesley_empty += 1
        return
    state.wellesley -= 1
    state.olin += 1

def decorate_bikeshare():
    """Add a title and label the axes."""
    decorate(title='Olin-Wellesley Bikeshare',
             xlabel='Time step (min)',
             ylabel='Number of bikes')

def run_simulation(p1, p2, num_steps):
    """Simulate the given number of time steps.
    p1: probability of an Olin->Wellesley customer arrival
    p2: probability of a Wellesley->Olin customer arrival
    num_steps: number of time steps"""
    state = State(olin=10, wellesley=2, olin_empty=0, wellesley_empty=0)
    for i in range(num_steps):
        step(state, p1, p2)
    
    return state

def main():
    """Si observamos el sistema y notamos que varias veces nos quedamos sin bicicletas en un momento determinado, podríamos usar el modelo para descubrir por qué sucede eso.
    Y si estamos considerando agregar más bicicletas u otra estación, podríamos evaluar el efecto de varios escenarios de "qué pasaría si".
    Como ejemplo, supongamos que tenemos suficientes datos para estimar que p2 es aproximadamente 0.2, pero no tenemos ninguna información sobre p1.
    Podríamos ejecutar simulaciones con un rango de valores para p1 y ver cómo varían los resultados."""

    p1_array = linspace(0,1,15)      #La función NumPy linspace (a veces llamada np.linspace) es una herramienta en Python para crear secuencias numéricas.
    p2 = 0.2                         #linspace(start = 0, stop = 1, num = 11)   inicia en 0, se detiene en 1, o se detiene en el index 11
    num_steps = 60

    """ sweeping de parametros """
    sweep= SweepSeries()       #un objeto SweepSeries, es similar a un TimeSeries; la diferencia es que las etiquetas en una SweepSeries son valores de parámetros en lugar de valores de tiempo.
    for p1 in p1_array:
        bikeshare = run_simulation(p1, p2, num_steps)
        sweep[p1] = bikeshare.wellesley_empty    #analisis de las veces que wellesley y olin se queda sin bicicletas o tenemos usuarios disconformes, conociendo p2 y simulando con un rango de valores en p1

    plot(sweep, label='Wellesley')
    savefig('/home/fernando/Escritorio/github/MODELOS Y SIMULACION/practica/bikeshare_param-wellesley_empty.jpg')

    print(sweep)

if __name__ == "__main__":
    main()
