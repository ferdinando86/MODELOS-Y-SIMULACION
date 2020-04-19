#!/usr/bin/python

#En la fincion bike_to_wellesley() y bike_to_olin() afregamos un if para verificar que las bicilcetas no sean negativas, y cuantos clientes disconformes hay, por no tener bicicleta

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
    if state.olin == 0:                 #verificamos no tener bicicletas en negativo
        state.olin_empty +=1            #clientes disconformes por no encontrar bicicleta disponible
        return

    state.olin -= 1
    state.wellesley += 1

def bike_to_olin(state):
    """Move one bike from Wellesley to Olin.
    state: bikeshare State object"""
    if state.wellesley == 0:            #verificamos no tener bicicletas en negativo
        state.wellesley_empty += 1      #clientes disconformes por no encontrar bicicleta disponible
        return
    state.wellesley -= 1
    state.olin += 1

def decorate_bikeshare():
    """Add a title and label the axes."""
    decorate(title='Olin-Wellesley Bikeshare',
             xlabel='Time step (min)',
             ylabel='Number of bikes')

def run_simulation(state, p1, p2, num_steps):
    """Simulate the given number of time steps.
    state: State object
    p1: probability of an Olin->Wellesley customer arrival
    p2: probability of a Wellesley->Olin customer arrival
    num_steps: number of time steps"""
    results_olin = TimeSeries()
    #results_wellesley = TimeSeries()
    for i in range(num_steps):
        step(state, p1, p2)
        results_olin[i] = state.olin
        #results_wellesley[i] = state.wellesley
        
    plot(results_olin, label='Olin')
    savefig('/home/fernando/Escritorio/github/MODELOS Y SIMULACION/practica/bikeshare_nonzero-both.jpg')


def main():

    bikeshare = State(olin=10, wellesley=2, olin_empty=0, wellesley_empty=0)  #se agregan 2 parametros (olin_empty-wellesley_empty) para acumular los clientes disconformes
    run_simulation(bikeshare, 0.4, 0.2, 60)               #conocemos los paramentros, p1=0.4 y p2=0.2 (en el ejemplo bikeshare_param conocemos solo p2=0.2)
    print("Bicicletas en Olin: ", bikeshare.olin)
    print("Bicicletas en Wellesley: ", bikeshare.wellesley)
    print("Clientes disconformes Olin: %d" % bikeshare.olin_empty)
    print("Clientes disconformes Wellesley: %d" % bikeshare.wellesley_empty)
    decorate_bikeshare()


if __name__ == "__main__":
    main()
