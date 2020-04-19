#!/usr/bin/python

from modsim import *
np.random.seed(7)       #se importa el objeto np de la libreria modsim, que a su vez importa desde la libreria NumPy (for basic numerical computation)
                        #La función numpy.random.seed proporciona la entrada (es decir, la semilla) al algoritmo que genera números pseudoaleatorios en NumPy.

def main():
    """
    La clase State definida en modsim.py contiene variables de estado y sus valores, y los almacena como filas.
    El objeto State que representa el número de bicicletas en cada estación.
    Cuando se visualiza un objeto State, enumera las variables de estado y sus valores por ej:
    bikeshare.olin --> 10
    bikeshare.wellesley --> 2"""

    bikeshare1 = State(olin=10, wellesley=2)  #se crea un objeto de la clase State de nombre bikeshare1, y se setean los valores de los atributos wellesley/olin
    bikeshare2 = State(olin=2, wellesley=10)  
    bike_to_olin(bikeshare1)                  #se llama a la funcion bike_to_olin, se le envia como parametro un objeto de la clase State, en este caso bikeshare1
    bike_to_wellesley(bikeshare2)
    print(bikeshare1)    #imprime los valores de las variables de estado del objeto bikeshare1
    print(bikeshare2)



    bikeshare = State(olin=10, wellesley=2)  #se agregan 2 parametros (olin_empty-wellesley_empty) para acumular los clientes disconformes
    run_simulation(bikeshare, 0.4, 0.2, 60)
    #print("clientes disconformes olin: ", bikeshare.olin_empty)
    #print("clientes disconformes wellesley: ", bikeshare.wellesley_empty)
    decorate_bikeshare()

def bike_to_wellesley(state):
    """Move one bike from Olin to Wellesley.
    state: bikeshare State object"""
    #if state.olin == 0:         #verificamos no tener bicicletas en negativo
    	#state.olin_empty += 1   #clientes disconformes por no encontrar bicicleta disponible
    	#return
    state.olin -= 1
    state.wellesley += 1

def bike_to_olin(state):
    """Move one bike from Wellesley to Olin.
    state: bikeshare State object"""
    #if state.wellesley == 0:          #verificamos no tener bicicletas en negativo
        #state.wellesley_empty += 1    #clientes disconformes por no encontrar bicicleta disponible
        #return
    state.wellesley -= 1
    state.olin += 1

def step(state, p1, p2):
    """Simulate one minute of time.
    state: bikeshare State object
    p1: probability of an Olin->Wellesley customer arrival
    p2: probability of a Wellesley->Olin customer arrival"""
    if flip(p1):                      #Supongamos que en un minuto dado, hay un X% de posibilidades de que un estudiante lleve una bicicleta de Olin a Wellesley
        bike_to_wellesley(state)
    if flip(p2):
        bike_to_olin(state)

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
    results = TimeSeries()             #TimeSeries es una versión especializada de Series, que está definida por Pandas.
    #results2 = TimeSeries()           #modsim.py proporciona un objeto llamado TimeSeries que puede contener una secuencia de valores que cambian con el tiempo, un array.
    for i in range(num_steps):         #Cuando ejecutamos una simulación, generalmente queremos guardar los resultados para un análisis posterior. La biblioteca
        step(state, p1, p2)            #modsim proporciona un objeto TimeSeries para este propósito. Un TimeSeries contiene una secuencia de marcas de tiempo y una
        results[i] = state.wellesley   #secuencia correspondiente de valores.
        #results2[i] = state.wellesley
        print(results[i],end="")       #results es un objeto vector del tipo TimeSeries
        #print(results2[i],end="")
        print(" ",end="")
    plot(results, label='Wellesley')
    #savefig('/home/fernando/Escritorio/Modelos y Simulacion/um_mys/olin.jpg')
    #plot(results2, label='Wellesley')
    savefig('/home/fernando/Escritorio/github/MODELOS Y SIMULACION/practica/wellesley-olin.jpg')

if __name__ == "__main__":
    main()

#flip(0.7) El resultado es uno de dos valores: verdadero con probabilidad 0.7 o falso con probabilidad 0.3. Si ejecuta esta función 100 veces, debería obtener True unas 70 veces y False unas 30 veces. Pero los resultados son aleatorios, por lo que podrían diferir de estas expectativas.

#El modelo no tiene en cuenta el tiempo de viaje de una estación de bicicletas a otra. El modelo no verifica si hay una bicicleta disponible, por lo que es posible que el número de bicicletas sea negativo 
