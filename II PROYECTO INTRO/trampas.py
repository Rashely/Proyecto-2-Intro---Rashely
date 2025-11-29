# trampas.py

import pygame
import os
import time

tam_tile = 25
img_trampa = None


def cargar_imagen_trampa():
    """Cargar imagen de la trampa."""
    ruta = os.path.join("assets", "trampa.jpeg")
    return pygame.image.load(ruta)


class TrampaManager:
    """
    Objetivo:
        Controlar cuántas trampas hay, cuándo pueden colocarse,
        y dibujarlas en pantalla.
    """
    def __init__(self):
        global img_trampa
        img_trampa = cargar_imagen_trampa()
        self.lista_trampas = []
        self.ultimo_tiempo = 0

    def puede_colocar(self):
        """Regresa True si se puede poner una trampa ahora."""
        if len(self.lista_trampas) >= 3:
            return False
        if time.time() - self.ultimo_tiempo < 5:
            return False
        return True

    def colocar_trampa(self, fila, col):
        """Coloca una trampa en la posición dada."""
        if self.puede_colocar():
            self.lista_trampas.append((fila, col))
            self.ultimo_tiempo = time.time()

    def eliminar_trampa(self, fila, col):
        """Elimina una trampa si está en la posición dada."""
        if (fila, col) in self.lista_trampas:
            self.lista_trampas.remove((fila, col))

    def dibujar(self, window):
        """Dibuja todas las trampas activas."""
        for fila, col in self.lista_trampas:
            x = col * tam_tile
            y = fila * tam_tile
            img = pygame.transform.scale(img_trampa, (tam_tile, tam_tile))
            window.blit(img, (x, y))

