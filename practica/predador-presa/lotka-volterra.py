from tkinter import *
from PIL import Image, ImageTk
import numpy as np
from matplotlib import pyplot
from scipy.integrate import odeint
from modsim import *

root = Tk()
root.geometry('1340x615')
root.title('UM / MODELOS Y SIMULACION 2020 / MODELO PREDADOR PRESA DE LOTKA-VOLTERRA')

parametros = Label(root,text="Parametros",font=("Arial Bold", 16))
parametros.grid(row=1,column=1,sticky=W)

### Parametros: alpha, beta, gamma, delta ###
# parametro alpha
alpha_label = Label(root,text="α:",font=("Arial", 14))
alpha_label.grid(row=2,column=1,sticky=W)
a_default = StringVar()
a_default.set("0.1")
a = Entry(root,width=7,textvariable=a_default)
a.grid(row=2,column=2)

'''Importamos imagen con la ecuacion e lotka-volterra'''
load = Image.open("ecuacion.png")
render = ImageTk.PhotoImage(load)
img = Label(root, image=render)
img.grid(row=1,column=3)
img.image = render
img.place(x=340, y=0)

# parametro beta
beta_label= Label(root,text="β: ",font=("Arial", 14))
beta_label.grid(row=3,column=1,sticky=W)
b_default = StringVar()
b_default.set("0.02")
b = Entry(root,width=7,textvariable=b_default)
b.grid(row=3,column=2)

# parametro gamma
gamma_label = Label(root,text="ɣ: ",font=("Arial", 14))
gamma_label.grid(row=4,column=1,sticky=W)
c_default = StringVar()
c_default.set("0.3")
c = Entry(root,width=7,textvariable=c_default)
c.grid(row=4,column=2)

# parametro delta
delta_label = Label(root,text="δ: ",font=("Arial", 14))
delta_label.grid(row=5,column=1,sticky=W)
d_default = StringVar()
d_default.set("0.01")
d = Entry(root,width=7,textvariable=d_default)
d.grid(row=5,column=2)

parametros = Label(root,text="Condiciones Iniciales",font=("Arial Bold", 16))
parametros.grid(row=6,column=1,sticky=W)

### Condiciones Iniciales: numero de presas, numero de depredadores, tiempo ###
# presas
x0_label = Label(root,text="Presas: ",font=("Arial", 14))
x0_label.grid(row=7,column=1,sticky=W)
presas_default = StringVar()
presas_default.set("50")
x0 = Entry(root,width=7,textvariable=presas_default)
x0.grid(row=7,column=2)

# depredadores
y0_label = Label(root,text="Depredadores: ",font=("Arial", 14))
y0_label.grid(row=8,column=1,sticky=W)
depredadores_default = StringVar()
depredadores_default.set("10")
y0 = Entry(root,width=7,textvariable=depredadores_default)
y0.grid(row=8,column=2)

# tiempo
tiempo_label = Label(root,text="Tiempo: ",font=("Arial", 14))
tiempo_label.grid(row=9,column=1,sticky=W)
tf_default = StringVar()
tf_default.set("200")
tf = Entry(root,width=7,textvariable=tf_default)
tf.grid(row=9,column=2)

def df_dt(x, t, a, b, c, d):
    """Función del sistema en forma canónica"""
    dx = a * x[0] - b * x[0] * x[1]
    dy = - c * x[1] + d * x[0] * x[1]
    return np.array([dx, dy])

def simulacion():
    condiciones_iniciales = np.array([int(x0.get()), int(y0.get())])
    N = 1000
    '''La función numpy.linspace genera un array NumPy formado por n números equiespaciados entre dos dados.Su sintaxis es:
    numpy.linspace(valor - inicial, valor - final, número de valores)
    Ejemplo:
    m = np.linspace(10, 40, 4)
    array([10, 20, 30, 40])    crea un array con 4 valores comprendidos entre 10 y 40, y que ademas sean equidistantes'''
    t = np.linspace(0, float(tf.get()), N)
    solucion = odeint(df_dt, condiciones_iniciales, t, args=(float(a.get()), float(b.get()), float(c.get()), float(d.get())))

    pyplot.clf()  # borra la configuracion actual
    plot(t, solucion[:, 0], label='presa')
    plot(t, solucion[:, 1], label='depredador')
    decorate(xlabel='Tiempo', ylabel='', title="Predador Presa - Lotka Volterra")
    savefig('lotka-volterra.jpg', dpi=75)
    load = Image.open("lotka-volterra.jpg")
    render = ImageTk.PhotoImage(load)
    img = Label(root, image=render)
    img.grid(row=10, column=1)
    img.image = render
    img.place(x=340, y=250)

    pyplot.clf()  # borra la configuracion actual
    x_max = np.max(solucion[:, 0]) * 1.05
    y_max = np.max(solucion[:, 1]) * 1.05
    x = np.linspace(0, x_max, 25)
    y = np.linspace(0, y_max, 25)
    xx, yy = np.meshgrid(x, y)
    uu, vv = df_dt((xx, yy), 0, float(a.get()), float(b.get()), float(c.get()), float(d.get()))
    norm = np.sqrt(uu ** 2 + vv ** 2)
    uu = uu / norm
    vv = vv / norm
    pyplot.quiver(xx, yy, uu, vv, norm, cmap=plt.cm.gray)
    plot(solucion[:, 0], solucion[:, 1])
    decorate(xlabel='', ylabel='', title="Lotka Volterra - Diagrama de Fases")
    savefig('lotka-volterra2.jpg', dpi=75)
    load = Image.open("lotka-volterra2.jpg")
    render = ImageTk.PhotoImage(load)
    img = Label(root, image=render)
    img.grid(row=10, column=2)
    img.image = render
    img.place(x=857, y=250)

finish = Button(root,text="simular",font=("Arial Bold", 15),command=simulacion)
finish.grid(row=11,column=1)

root.mainloop()