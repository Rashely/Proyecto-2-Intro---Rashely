# jugador.py (con sprite)



import pygame
import os
from mapa import tam_tile

# Clase Jugador
# Objetivo:
#   Representar al jugador, su movimiento, energía
#   y su interacción básica con el mapa.
# Entradas:
#   posición inicial (fila, columna)
# Salidas:
#   movimiento del jugador en pantalla
# Restricciones:
#   No atravesar terrenos bloqueados
#   Energía no puede ser negativa

class Jugador:
    """
    Clase que representa al jugador.
    Mantiene su posición, energía y velocidad.
    """

    def __init__(self, fila_inicial, col_inicial):
        # Entrada de fila y columna inicial
        self.fila = fila_inicial
        self.col = col_inicial

        # Energía inicial del jugador
        self.energia = 100

        # Velocidad normal (tiles por movimiento)
        self.velocidad = 1

        # Velocidad al correr
        self.velocidad_correr = 2

        # Control para saber si está corriendo
        self.corriendo = False

        # Cargar sprite del jugador

        ruta = os.path.join("assets", "jugador.jpeg")
        self.sprite = pygame.image.load(ruta)
        self.sprite = pygame.transform.scale(self.sprite, (tam_tile, tam_tile))


    # Métodos del jugador




    def mover(self, df, dc, mapa_objetos):
        """
        Objetivo:
            Mover al jugador si el terreno lo permite.
        """
        
        nueva_fila = self.fila + df
        nueva_col = self.col + dc

        limite = len(mapa_objetos)  # tamaño real del mapa

        # Verificar límites reales
        if nueva_fila < 0 or nueva_fila >= limite:
            return
        if nueva_col < 0 or nueva_col >= limite:
            return

        celda = mapa_objetos[nueva_fila][nueva_col]

        if celda.permitir_jugador():
            self.fila = nueva_fila
            self.col = nueva_col


    def iniciar_correr(self):
        if self.energia > 0:
            self.corriendo = True

    def detener_correr(self):
        self.corriendo = False

    def consumir_energia(self):
        if self.corriendo:
            self.energia -= 1
            if self.energia <= 0:
                self.energia = 0
                self.corriendo = False

    def regenerar_energia(self):
        if not self.corriendo and self.energia < 100:
            self.energia += 0.5

    def dibujar(self, window):
        """
        Objetivo:
            Dibujar al jugador usando sprite.
        """
        x = self.col * tam_tile
        y = self.fila * tam_tile
        window.blit(self.sprite, (x, y))

    def actualizar(self):
        if self.corriendo:
            self.consumir_energia()
        else:
            self.regenerar_energia()

