"""
MODELOS Y SIMULACION 2020
Profesor: Ing. Diego Cordoba
Alumno: Fernando Lopez
"""

import pygame       # Libreria para la creacion de juegos en Python, facilita mucho la creacion de grillas y eventos con el mouse

NEGRO = (0, 0, 0)          # Definimos algunos colores como constantes
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)

LARGO = 20        # Establecemos el LARGO y ALTO de cada celda de la grilla.
ALTO = 20
MARGEN = 5        # Establecemos el margen entre las celdas.
filas = 20
columnas = 20
estado = False    # Iteramos el bucle principal hasta que el usuario pulse el botón de salir

reloj = pygame.time.Clock()   # Pulsos de reloj para refrescar la pantalla
total_time = 0                # variable usada para verificar el tiempo en la carga del logo de la UM

DIMENSION_VENTANA = [700, 505]      # Establecemos el LARGO y ALTO de la pantalla
pantalla = pygame.display.set_mode(DIMENSION_VENTANA)
pygame.display.set_caption("MODELOS Y SIMULACION 2020")     # Establecemos el título de la pantalla.

displayLogo = pygame.image.load("images/logo.jpg")

img = pygame.image.load("images/boton.png")  # ruta para cargar la imagen del boton iterar
center = 600, 240
rect = img.get_rect()   # otenemos las dimensiones de la imagen del boton iterar
rect.center = center

grid = []         # Creamos un array bidimensional, o matriz
for y in range(20):
    for x in range(20):
        grid.append([])
        grid[y].append(0)  # Creamos las celdas con valor 0

pygame.init()     # Inicializamos pygame


##########################################BUCLE PRINCIPAL DEL PROGRAMA###############################################################################
while not estado:
    for evento in pygame.event.get():               # Captura eventos sobre la ventana del programa
        if evento.type == pygame.QUIT:              # Captura el evento para salir del programa
            estado = True
        elif evento.type == pygame.MOUSEBUTTONDOWN: # Captura el evento cuando presionamos el boton del mouse sobre la ventana activa
            pos = pygame.mouse.get_pos()            # Cuando se presiona el ratón, obtenemos la posicion donde clickeo
            clic_columna = pos[0] // (LARGO + MARGEN)  # Cambia las coordenadas x/y de la pantalla por coordenadas en la grilla, pudiendo encontrar el clic en la fila y columna
            clic_fila = pos[1] // (ALTO + MARGEN)
            if clic_fila < 20 and clic_columna < 20:   # Verificamos estar dentro de la grilla
                if grid[clic_fila][clic_columna]:   # Si la celda clickeada es TRUE, cambia el estado a FALSE
                    grid[clic_fila][clic_columna] = 0   # Si estamos dentro de la grilla, desactiva la celda clickeada con el mouse y la colorea en blanco
                else:
                    grid[clic_fila][clic_columna] = 1   # Si estamos dentro de la grilla, activa la celda clickeada con el mouse y la colorea en verde
            if rect.collidepoint(evento.pos):       # Verifica si se hizo clic sobre el rectangulo que se creo sobre la imagen del boton iterar, si es TRUE dispara la logica
                nuevo = []                          # Nueva matriz donde guarda las iteraciones, la crea en una matriz nueva para no perder el estado de la iteracion
                for i in range(filas):
                    nuevo.append([False] * columnas)    # Inicializamos en False o 0 al array 'nuevo' donde guardamos los nuevos valores despues de iterar
##########################################LOGICA DEL JUEGO DE LA VIDA##############################################################################
#               * * *  Como se ve en la imagen, una celda X, esta rodeada por 8 celdas *, con los 2 for que siguen a continuacion, recorremos
#               * X *  la grilla de 20 filas x 20 columnas. Dentro del for usamos varios if para verificar el estado de las 400 celdas (20x20).
#               * * *  Cuando el for esta en una celda X, por ej si tomamos la celda (5,2) los if analizan las 8 celdas * a su alrededor, analizaria:
#                      (4,1)(4,2)(4,3)
#                      (5,1)(5,2)(5,3)
#                      (6,1)(6,2)(6,3)
                for y in range(filas):       # recorremos las filas de la matriz
                    for x in range(columnas):    # recorremos las columnas de la matriz
                        n = 0                # n es una variable acumulador, donde va sumando las celdas activas alrededor de la celda que estamos analizando
                        if y > 0 and x > 0 and grid[y - 1][x - 1]:   # en el ejemplo de arriba este if analizaria la celsa (4,1)
                            n += 1    # si la comparacion del if es TRUE, incrementa en 1 la variable n
                        if x > 0 and grid[y][x - 1]:                 # (5,1)
                            n += 1
                        if y < filas - 1 and x > 0 and grid[y + 1][x - 1]:   # (6,1)  (y < filas - 1 and x > 0 comparacion para no salirse de la grilla)
                            n += 1
                        if y > 0 and grid[y - 1][x]:                 # (4,2)
                            n += 1
                        if y < filas - 1 and grid[y + 1][x]:         # (6,2)
                            n += 1
                        if y > 0 and x < columnas - 1 and grid[y - 1][x + 1]:   # (4,3)
                            n += 1
                        if x < columnas-1 and grid[y][x + 1]:        # (5,3)
                            n += 1
                        if y < filas-1 and x < columnas - 1 and grid[y + 1][x + 1]:   # (6,3)
                            n += 1

                        if grid[y][x] and (n == 2 or n == 3):   # Si la celda (5,2) es TRUE (activa en verde) y el acumulador encuentra 2 o 3 celdas activas a su alrededor
                            nuevo[y][x] = True                  # la celda sigue viva, y se guarda en la nueva matriz
                        elif not grid[y][x] and n == 3:         # Si la celda (5,2) es False (desactiva en blanco) y el acumulador encuentra 3 celdas activas a su alrededor
                            nuevo[y][x] = True                  # la celda revive, y se guarda en la nueva matriz
                        else:                                   # Si el acumulador es 0 o 1, o mayor a 3
                            nuevo[y][x] = False                 # la celda (5,2) muere

                grid = nuevo                     # Seteamos la grilla con los nuevos valores de la nueva matriz
#####################################################################################################################################################

    pantalla.fill(NEGRO)    # Establecemos el fondo de pantalla

    # Dibujamos la grilla, automagico de la libreria pygame XD
    for fila in range(filas):
        for columna in range(columnas):
            color = BLANCO
            if grid[fila][columna] == 1:
                color = VERDE
            pygame.draw.rect(pantalla,
                             color,
                             [(MARGEN + LARGO) * columna + MARGEN,
                              (MARGEN + ALTO) * fila + MARGEN,
                              LARGO,
                              ALTO])

    pantalla.blit(img, (515, 195))  # Cargamos en pantalla la imagen del boton iterar
    pygame.draw.rect(pantalla, ROJO, rect, 1)  # Dibujamos un rectangulo sobre la imagen del boton, como una capa, que al hacer clic sobre el rectangulo ejecuta la logica

    if (total_time < 4000):     # Se ejecuta el programa, y se muestra el logo de la UM solo durante 4 segundos, para evitar incrementar el ego de la misma XD
        display_logo_size = displayLogo.get_size()  # Obtiene las dimensiones del logo de la UM para poder ser centrado
        pantalla.blit(displayLogo, [700 / 2 - display_logo_size[0] / 2, 505 / 2 - display_logo_size[1] / 2])  # Dibuja el logo de la UM en la pantalla

    dt = reloj.tick(60)   # Se refresca la pantalla 60 fotogramas por segundo
    total_time += dt      # Acumulador para verificar que no supere los 4 segundos el logo de la UM

    pygame.display.flip()  # Actualizamos la pantalla con lo que hemos dibujado

pygame.quit()