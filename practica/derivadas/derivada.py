
from sympy import *

alpha = symbols('alpha')
beta = symbols('beta')
t = Symbol('t')
f = Function('f')

C1, p_0 = symbols('C1 p_0')

dfdt = diff(f(t), t)

eq = Eq(dfdt, alpha*f(t)+beta*f(t)**2)    # definicion de la ecuacion, derivada de f con respecto a t = alpha*f(t)+beta*f(t)**2
print("Ecuacion: ", eq)

general = dsolve(eq)        # resuelve la ecuacion
print("Solucion general: ", general)

# Condiciones iniciales ---> f(t) = 0 && t = 0
# El valor de la derivada es: Eq(f(t), alpha*exp(alpha*(C1 + t))/(beta*(1 - exp(alpha*(C1 + t)))))
# rhs, righ hand side. Dejamos solo el lado derecho de la ecuacion, haciendo f(t) = 0
# subs, reemplaza t por 0, haciendo t = 0
# Dando como resultado: alpha*exp(C1*alpha)/(beta*(1 - exp(C1*alpha)))
general_t0 = general.rhs.subs(t, 0)

condicion_inicial = Eq(general_t0, p_0)               #p_0 C1 ?????
print("Condicion inicial: ", condicion_inicial)
particular_temp = solve(condicion_inicial, C1)

particular = general.subs(C1, particular_temp[0])
print("Solucion particular: ", particular)

particular_simple = simplify(particular)
print("Solucion particular simplificada: ", particular_simple)