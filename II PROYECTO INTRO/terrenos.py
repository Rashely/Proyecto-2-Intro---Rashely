# terrenos.py 


import pygame
import os

# Objetivo:
#   Cargar las imágenes para cada tipo de terreno
#   y definir clases que representen las propiedades
#   de movimiento permitidas.

# Entrada: nombre del archivo de imagen
# Salida: superficie de pygame cargada
# Restricciones: la imagen debe existir dentro de assets/terrenos

def cargar_imagen(nombre):
    """
    Objetivo:
        Cargar una imagen desde la carpeta de terrenos.
    """
    ruta = os.path.join("assets", "terrenos", nombre)
    return pygame.image.load(ruta)

# Variables globales en minuscula
img_camino = None
img_muro = None
img_liana = None
img_tunel = None


def inicializar_imagenes():
    """
    Objetivo:
        Cargar las imágenes globales para cada tipo de terreno.
    """
    global img_camino, img_muro, img_liana, img_tunel
    img_camino = cargar_imagen("camino.jpeg")
    img_muro = cargar_imagen("muro.jpeg")
    img_liana = cargar_imagen("liana.jpeg")
    img_tunel = cargar_imagen("tunel.jpeg")


class Terreno:
    """
    Objetivo:
        Clase base que representa un tipo de terreno.
    """
    def __init__(self, imagen, puede_jugador, puede_enemigo):
        self.imagen = imagen
        self.puede_jugador = puede_jugador
        self.puede_enemigo = puede_enemigo

    def permitir_jugador(self):
        """Retorna True si el jugador puede pasar."""
        return self.puede_jugador

    def permitir_enemigo(self):
        """Retorna True si el enemigo puede pasar."""
        return self.puede_enemigo

    def draw(self, window, x, y, size):
        """
        Objetivo:
            Dibujar el terreno en la pantalla.
        """
        img = pygame.transform.scale(self.imagen, (size, size))
        window.blit(img, (x, y))


class Camino(Terreno):
    """Terreno transitable por jugador y enemigo."""
    def __init__(self):
        super().__init__(img_camino, True, True)


class Muro(Terreno):
    """Terreno bloqueado para ambos."""
    def __init__(self):
        super().__init__(img_muro, False, False)


class Liana(Terreno):
    """Terreno exclusivo de enemigos."""
    def __init__(self):
        super().__init__(img_liana, False, True)


class Tunel(Terreno):
    """Terreno exclusivo del jugador."""
    def __init__(self):
        super().__init__(img_tunel, True, False)

