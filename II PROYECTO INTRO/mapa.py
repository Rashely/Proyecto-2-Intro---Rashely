# mapa.py 

import pygame
import random
import os
from terrenos import Camino, Muro, Liana, Tunel, inicializar_imagenes

# Tamaño del tile
# Entrada: ninguna
# Salida: valor entero
# Restricciones: usado en todo el mapa

tam_tile = 25
filas = 15
columnas = 15

img_salida = None

def cargar_imagen_salida():
    """Cargar la imagen de la salida."""
    ruta = os.path.join("assets", "salida.jpeg")
    return pygame.image.load(ruta)


def crear_matriz_vacia():
    """Objetivo: crear toda la matriz llena de muros (valor 1)."""
    return [[1 for _ in range(columnas)] for _ in range(filas)]


def generar_camino_principal(matriz):
    """
    Objetivo:
        Crear un camino garantizado desde (0,0) hasta (19,19).
    """
    fila = 0
    col = 0
    matriz[fila][col] = 0

    while fila != filas - 1 or col != columnas - 1:
        direccion = random.choice(["abajo", "derecha"])
        if direccion == "abajo" and fila < filas - 1:
            fila += 1
        elif direccion == "derecha" and col < columnas - 1:
            col += 1
        matriz[fila][col] = 0


def rellenar_terrenos(matriz):
    """Objetivo: asignar aleatoriamente tipos de terreno a celdas que no son camino."""
    for f in range(filas):
        for c in range(columnas):
            if matriz[f][c] != 0:
                matriz[f][c] = random.choice([1, 2, 3])


def generar_mapa():
    """Retorna una matriz 20x20 de números representando terrenos."""
    matriz = crear_matriz_vacia()
    generar_camino_principal(matriz)
    rellenar_terrenos(matriz)
    return matriz


def convertir_a_objetos(matriz):
    """
    Objetivo:
        Convertir la matriz numérica en objetos de clase Terreno.
    """
    nuevo = []
    for fila in matriz:
        nueva_fila = []
        for celda in fila:
            if celda == 0:
                nueva_fila.append(Camino())
            elif celda == 1:
                nueva_fila.append(Muro())
            elif celda == 2:
                nueva_fila.append(Liana())
            elif celda == 3:
                nueva_fila.append(Tunel())
        nuevo.append(nueva_fila)
    return nuevo


def colocar_salida(mapa_objetos):
    """Define la salida en la esquina inferior-derecha."""
    global img_salida
    img_salida = cargar_imagen_salida()
    return filas - 1, columnas - 1


def dibujar_salida(window, fila, col):
    """Dibuja la imagen de salida."""
    x = col * tam_tile
    y = fila * tam_tile
    img = pygame.transform.scale(img_salida, (tam_tile, tam_tile))
    window.blit(img, (x, y))


def dibujar_mapa(window, mapa_objetos):
    """Dibuja todo el mapa en pantalla."""
    for f in range(filas):
        for c in range(columnas):
            x = c * tam_tile
            y = f * tam_tile
            mapa_objetos[f][c].draw(window, x, y, tam_tile)

