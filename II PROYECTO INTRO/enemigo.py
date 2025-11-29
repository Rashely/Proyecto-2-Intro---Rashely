# enemigo.py 

import pygame
import os
import random
from mapa import tam_tile

class Enemigo:
    """
    # Objetivo: Representar un enemigo que se mueve en el mapa
    # Entrada: fila_inicial, col_inicial - posición de inicio
    # Salida: Objeto Enemigo con sprite y comportamiento
    # Restricciones: No puede pasar por terrenos bloqueados
    """
    
    def __init__(self, fila_inicial, col_inicial):
        """
        # Objetivo: Inicializar el enemigo con posición y sprite
        # Entrada: fila_inicial, col_inicial - coordenadas de inicio
        # Salida: None (crea objeto Enemigo)
        # Restricciones: Posición debe estar dentro del mapa
        """
        # Posición inicial en el mapa
        self.fila = fila_inicial
        self.col = col_inicial
        
        # Velocidad de movimiento 
        self.velocidad = 1

        # Contador para controlar velocidad de movimiento
        self.contador_movimiento = 0
        self.velocidad_movimiento = 10  # Se mueve cada 10 frames 

        # Cargar y escalar sprite del enemigo
        ruta = os.path.join("assets", "enemigo.jpeg")  # Ruta de la imagen
        self.sprite = pygame.image.load(ruta)  # Cargar imagen
        self.sprite = pygame.transform.scale(self.sprite, (tam_tile, tam_tile))  # Ajustar tamaño

    def puede_mover(self, nueva_fila, nueva_col, mapa_objetos):
        """
        # Objetivo: Verificar si el enemigo puede moverse a una posición
        # Entrada: 
        #   nueva_fila, nueva_col - coordenadas destino
        #   mapa_objetos - matriz con objetos de terreno
        # Salida: True si puede moverse, False si no
        # Restricciones: No puede salir del mapa ni pasar terrenos bloqueados
        """
        # Verificar límites del mapa (no salirse)
        if nueva_fila < 0 or nueva_fila >= len(mapa_objetos):
            return False  # Fuera del mapa en filas
        if nueva_col < 0 or nueva_col >= len(mapa_objetos):
            return False  # Fuera del mapa en columnas
        
        # Obtener celda destino y verificar si permite enemigos
        celda = mapa_objetos[nueva_fila][nueva_col]
        return celda.permitir_enemigo()  # True si puede pasar

    def obtener_movimientos_posibles(self, mapa_objetos):
        """
        # Objetivo: Obtener todas las direcciones posibles para moverse
        # Entrada: mapa_objetos - matriz del mapa
        # Salida: movimientos - lista de tuplas (df, dc) posibles
        # Restricciones: Solo direcciones cardinales (no diagonales)
        """
        movimientos = []  # Lista para almacenar movimientos válidos
        
        # Definir las 4 direcciones posibles
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # arriba, abajo, izquierda, derecha
        
        # Verificar cada dirección
        for direccion in direcciones:
            df, dc = direccion  # Desplazamiento en fila y columna
            nueva_fila = self.fila + df  # Calcular nueva fila
            nueva_col = self.col + dc    # Calcular nueva columna
            
            # Si puede moverse a esa posición, agregar a lista
            if self.puede_mover(nueva_fila, nueva_col, mapa_objetos):
                movimientos.append((df, dc))
        
        return movimientos  # Devolver movimientos posibles

    def deberia_mover(self):
        """
        # Objetivo: Controlar la velocidad de movimiento del enemigo
        # Entrada: None
        # Salida: True si debe moverse en este frame, False si no
        # Restricciones: Usa contador de frames para ralentizar movimiento
        """
        self.contador_movimiento += 1  # Incrementar contador cada frame
        
        # Solo moverse cuando el contador alcanza la velocidad definida
        if self.contador_movimiento >= self.velocidad_movimiento:
            self.contador_movimiento = 0  # Reiniciar contador
            return True  # Puede moverse
        return False  # No moverse en este frame

    def mover_hacia(self, objetivo_f, objetivo_c, mapa_objetos):
        """
        # Objetivo: Mover el enemigo hacia el objetivo (jugador)
        # Entrada:
        #   objetivo_f, objetivo_c - coordenadas del objetivo
        #   mapa_objetos - matriz del mapa
        # Salida: None (modifica posición del enemigo)
        # Restricciones: 70% movimiento inteligente, 30% aleatorio
        """
        # Solo moverse si pasaron suficientes frames
        if not self.deberia_mover():
            return  # No moverse en este frame
            
        # Probabilidad: 70% movimiento inteligente, 30% aleatorio
        if random.random() < 0.7:
            self.mover_inteligente_hacia(objetivo_f, objetivo_c, mapa_objetos)
        else:
            self.mover_aleatorio(mapa_objetos)

    def mover_inteligente_hacia(self, objetivo_f, objetivo_c, mapa_objetos):
        """
        # Objetivo: Movimiento inteligente que reduces distancia al objetivo
        # Entrada:
        #   objetivo_f, objetivo_c - coordenadas del objetivo  
        #   mapa_objetos - matriz del mapa
        # Salida: None (modifica posición del enemigo)
        # Restricciones: Elige movimiento que más reduce distancia
        """
        # Obtener todos los movimientos posibles
        movimientos_posibles = self.obtener_movimientos_posibles(mapa_objetos)
        mejor_movimiento = None  # Mejor movimiento encontrado
        menor_distancia = 1000   # Distancia inicial grande
        
        # Evaluar cada movimiento posible
        for movimiento in movimientos_posibles:
            df, dc = movimiento  # Desplazamiento
            nueva_fila = self.fila + df  # Calcular nueva posición
            nueva_col = self.col + dc
            
            # Calcular distancia Manhattan al objetivo
            dist_filas = abs(nueva_fila - objetivo_f)      # Diferencia en filas
            dist_columnas = abs(nueva_col - objetivo_c)    # Diferencia en columnas
            distancia_total = dist_filas + dist_columnas   # Distancia total
            
            # Si esta posición está más cerca, es mejor movimiento
            if distancia_total < menor_distancia:
                menor_distancia = distancia_total
                mejor_movimiento = movimiento
        
        # Aplicar el mejor movimiento encontrado
        if mejor_movimiento:
            df, dc = mejor_movimiento
            self.fila += df  # Mover en fila
            self.col += dc   # Mover en columna

    def mover_lejos(self, objetivo_f, objetivo_c, mapa_objetos):
        """
        # Objetivo: Moverse lejos del objetivo (huir)
        # Entrada:
        #   objetivo_f, objetivo_c - coordenadas del objetivo
        #   mapa_objetos - matriz del mapa  
        # Salida: None (modifica posición del enemigo)
        # Restricciones: Elige movimiento que más aumenta distancia
        """
        # Solo moverse si pasaron suficientes frames
        if not self.deberia_mover():
            return  # No moverse en este frame
            
        # Obtener todos los movimientos posibles
        movimientos_posibles = self.obtener_movimientos_posibles(mapa_objetos)
        mejor_movimiento = None  # Mejor movimiento encontrado
        mayor_distancia = -1     # Distancia inicial pequeña
        
        # Evaluar cada movimiento posible
        for movimiento in movimientos_posibles:
            df, dc = movimiento  # Desplazamiento
            nueva_fila = self.fila + df  # Calcular nueva posición
            nueva_col = self.col + dc
            
            # Calcular distancia Manhattan al objetivo
            dist_filas = abs(nueva_fila - objetivo_f)      # Diferencia en filas
            dist_columnas = abs(nueva_col - objetivo_c)    # Diferencia en columnas
            distancia_total = dist_filas + dist_columnas   # Distancia total
            
            # Si esta posición está más lejos, es mejor movimiento
            if distancia_total > mayor_distancia:
                mayor_distancia = distancia_total
                mejor_movimiento = movimiento
        
        # Aplicar el mejor movimiento encontrado
        if mejor_movimiento:
            df, dc = mejor_movimiento
            self.fila += df  # Mover en fila
            self.col += dc   # Mover en columna
        else:
            # Si no hay movimiento bueno, mover aleatoriamente
            self.mover_aleatorio(mapa_objetos)

    def mover_aleatorio(self, mapa_objetos):
        """
        # Objetivo: Movimiento aleatorio simple
        # Entrada: mapa_objetos - matriz del mapa
        # Salida: None (modifica posición del enemigo)
        # Restricciones: Solo se mueve si hay movimientos posibles
        """
        # Obtener movimientos posibles
        movimientos_posibles = self.obtener_movimientos_posibles(mapa_objetos)
        
        # Si hay movimientos posibles, elegir uno al azar
        if movimientos_posibles:
            movimiento_elegido = random.choice(movimientos_posibles)
            df, dc = movimiento_elegido
            self.fila += df  # Mover en fila
            self.col += dc   # Mover en columna

    def dibujar(self, window):
        """
        # Objetivo: Dibujar el enemigo en la pantalla
        # Entrada: window - superficie de pygame donde dibujar
        # Salida: None (dibuja sprite en la ventana)
        # Restricciones: Usa posición actual del enemigo
        """
        # Calcular posición en píxeles
        x = self.col * tam_tile  # Coordenada X en píxeles
        y = self.fila * tam_tile # Coordenada Y en píxeles
        
        # Dibujar sprite en la posición calculada
        window.blit(self.sprite, (x, y))
