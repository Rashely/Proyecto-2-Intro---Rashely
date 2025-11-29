# main.py (VERSIÓN COMPLETA CORREGIDA)

import pygame
import sys
import random
import time

from terrenos import inicializar_imagenes
from mapa import generar_mapa, convertir_a_objetos, dibujar_mapa, colocar_salida, dibujar_salida, tam_tile, filas, columnas
from trampas import TrampaManager
from jugador import Jugador
from enemigo import Enemigo

# Configuración del juego - TAMAÑOS CORREGIDOS
ancho_mapa = columnas * tam_tile  # Ancho solo del mapa
ancho_ui = 200  # Espacio para la interfaz
ancho_total = ancho_mapa + ancho_ui  # Ancho total de la ventana
alto_total = filas * tam_tile
fps = 30

def obtener_posicion_valida(mapa_objetos):
    """
    # Objetivo: Encontrar una posición aleatoria donde puede estar un enemigo
    # Entrada: mapa_objetos - matriz con objetos de terreno
    # Salida: (fila, columna) - tupla con coordenadas válidas
    # Restricciones: Evitar bucle infinito con máximo de intentos
    """
    intentos = 0
    # Intentar hasta 100 veces encontrar posición válida
    while intentos < 100:
        fila = random.randint(0, filas - 1)
        col = random.randint(0, columnas - 1)
        # Verificar si el enemigo puede estar en esta celda
        if mapa_objetos[fila][col].permitir_enemigo():
            return fila, col
        intentos += 1
    # Si no encuentra posición válida, usar posición por defecto
    return 0, 0

def crear_enemigos(mapa_objetos, cantidad):
    """
    # Objetivo: Crear múltiples enemigos en posiciones válidas del mapa
    # Entrada: 
    #   mapa_objetos - matriz del mapa
    #   cantidad - número de enemigos a crear
    # Salida: lista_enemigos - lista con objetos Enemigo
    # Restricciones: cantidad debe ser número positivo
    """
    lista_enemigos = []
    for i in range(cantidad):
        # Obtener posición válida para cada enemigo
        fila, col = obtener_posicion_valida(mapa_objetos)
        nuevo_enemigo = Enemigo(fila, col)
        lista_enemigos.append(nuevo_enemigo)
    return lista_enemigos

def mostrar_texto_simple(window, texto, tamaño, color, x, y):
    """
    # Objetivo: Mostrar texto en la pantalla en posición específica
    # Entrada:
    #   window - superficie de pygame donde dibujar
    #   texto - string a mostrar
    #   tamaño - tamaño de fuente
    #   color - color del texto (R, G, B)
    #   x, y - coordenadas en pantalla
    # Salida: None (dibuja directamente en la ventana)
    # Restricciones: Coordenadas deben estar dentro de la ventana
    """
    font = pygame.font.SysFont(None, tamaño)  # Crear objeto fuente
    texto_img = font.render(texto, True, color)  # Renderizar texto
    window.blit(texto_img, (x, y))  # Dibujar texto en posición

def dibujar_barra_energia(window, jugador):
    """
    # Objetivo: Dibujar barra visual de energía del jugador
    # Entrada:
    #   window - superficie de pygame
    #   jugador - objeto Jugador con atributo energia
    # Salida: None (dibuja directamente en la ventana)
    # Restricciones: Energía debe estar entre 0-100
    """
    # POSICIÓN CORREGIDA: Fuera del área del mapa
    pos_x = ancho_mapa + 10  # Después del último tile del mapa
    pos_y = 20
    
    # Título de la barra
    mostrar_texto_simple(window, "ENERGÍA", 16, (200, 200, 200), pos_x, pos_y)
    
    # Dibujar fondo de la barra (gris oscuro)
    pygame.draw.rect(window, (30, 30, 30), (pos_x, pos_y + 20, 104, 16))
    
    # Calcular ancho de la energía actual
    energia_ancho = jugador.energia
    if energia_ancho > 100:
        energia_ancho = 100
    
    # Dibujar barra de energía (verde cuando alta, amarillo cuando media, rojo cuando baja)
    if energia_ancho > 60:
        color_energia = (0, 255, 0)  # Verde
    elif energia_ancho > 30:
        color_energia = (255, 255, 0)  # Amarillo
    else:
        color_energia = (255, 0, 0)  # Rojo
        
    pygame.draw.rect(window, color_energia, (pos_x + 2, pos_y + 22, energia_ancho, 12))
    
    # Mostrar texto con valor numérico
    mostrar_texto_simple(window, f"{int(jugador.energia)}%", 14, (255, 255, 255), pos_x + 110, pos_y + 22)

def dibujar_contador_trampas(window, trampas):
    """
    # Objetivo: Mostrar cuántas trampas puede colocar el jugador
    # Entrada:
    #   window - superficie de pygame
    #   trampas - objeto TrampaManager con lista_trampas
    # Salida: None (dibuja directamente en la ventana)
    # Restricciones: Máximo 3 trampas simultáneas
    """
    # POSICIÓN CORREGIDA: Debajo de la barra de energía
    pos_x = ancho_mapa + 10
    pos_y = 60
    
    trampas_disponibles = 3 - len(trampas.lista_trampas)
    
    # Título
    mostrar_texto_simple(window, "TRAMPAS", 16, (200, 200, 200), pos_x, pos_y)
    
    # Contador con color según disponibilidad
    color_contador = (0, 255, 0) if trampas_disponibles > 0 else (255, 100, 100)
    mostrar_texto_simple(window, f"Disponibles: {trampas_disponibles}/3", 18, color_contador, pos_x, pos_y + 25)

def dibujar_puntuacion(window, puntuacion):
    """
    # Objetivo: Mostrar puntuación actual del jugador
    # Entrada:
    #   window - superficie de pygame
    #   puntuacion - número entero con puntos actuales
    # Salida: None (dibuja directamente en la ventana)
    # Restricciones: Puntuación debe ser número entero
    """
    # POSICIÓN CORREGIDA: Debajo del contador de trampas
    pos_x = ancho_mapa + 10
    pos_y = 120
    
    # Título
    mostrar_texto_simple(window, "PUNTUACIÓN", 16, (200, 200, 200), pos_x, pos_y)
    
    # Puntuación en grande
    mostrar_texto_simple(window, f"{puntuacion}", 32, (255, 255, 0), pos_x, pos_y + 25)

def dibujar_modo_actual(window, modo):
    """
    # Objetivo: Mostrar modo de juego actual
    # Entrada:
    #   window - superficie de pygame
    #   modo - string "escapa" o "cazador"
    # Salida: None (dibuja directamente en la ventana)
    # Restricciones: modo debe ser string válido
    """
    # POSICIÓN CORREGIDA: Debajo de la puntuación
    pos_x = ancho_mapa + 10
    pos_y = 180
    
    # Título
    mostrar_texto_simple(window, "MODO", 16, (200, 200, 200), pos_x, pos_y)
    
    # Modo con color diferente según tipo
    if modo == "escapa":
        color_modo = (100, 200, 255)  # Azul claro
        texto_modo = "ESCAPA"
    else:
        color_modo = (255, 200, 100)  # Naranja claro
        texto_modo = "CAZADOR"
        
    mostrar_texto_simple(window, texto_modo, 24, color_modo, pos_x, pos_y + 25)
    
def dibujar_dificultad(window, dificultad):
    """
    # Objetivo: Mostrar dificultad actual en la UI
    # Entrada: window - superficie de pygame, dificultad - string
    # Salida: None (dibuja en pantalla)
    # Restricciones: dificultad debe ser válida
    """
    pos_x = ancho_mapa + 10
    pos_y = 210
    
    # Título
    mostrar_texto_simple(window, "DIFICULTAD", 16, (200, 200, 200), pos_x, pos_y)
    
    # Color según dificultad
    if dificultad == "facil":
        color = (0, 255, 0)  # Verde
        texto = "FÁCIL"
    elif dificultad == "medio":
        color = (255, 255, 0)  # Amarillo  
        texto = "MEDIO"
    else:
        color = (255, 0, 0)  # Rojo
        texto = "DIFÍCIL"
        
    mostrar_texto_simple(window, texto, 20, color, pos_x, pos_y + 25)



def dibujar_toda_ui(window, jugador, trampas, puntuacion, modo, dificultad):
    """
    # Objetivo: Dibujar toda la interfaz de usuario
    # Entrada:
    #   window - superficie de pygame
    #   jugador - objeto Jugador
    #   trampas - objeto TrampaManager
    #   puntuacion - puntos actuales
    #   modo - modo de juego actual
    # Salida: None (dibuja todos los elementos UI)
    # Restricciones: Todos los parámetros deben ser válidos
    """
    dibujar_barra_energia(window, jugador)
    dibujar_contador_trampas(window, trampas)
    dibujar_puntuacion(window, puntuacion)
    dibujar_modo_actual(window, modo)
    dibujar_dificultad(window, dificultad)  # NUEVO

def pedir_nombre_jugador():
    """
    # Objetivo: Mostrar pantalla para que jugador ingrese nombre
    # Entrada: None (usa input del teclado)
    # Salida: nombre_ingresado - string con nombre del jugador
    # Restricciones: Nombre máximo 12 caracteres, no vacío
    """
    pygame.init()
    # Crear ventana pequeña para registro
    pantalla_chica = pygame.display.set_mode((400, 200))
    pygame.display.set_caption("Registro de Jugador")
    
    font = pygame.font.SysFont(None, 36)  # Fuente para texto
    nombre_ingresado = ""  # Variable para almacenar nombre
    terminado = False  # Control del bucle
    
    while not terminado:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if evento.type == pygame.KEYDOWN:
                # Enter para terminar
                if evento.key == pygame.K_RETURN and nombre_ingresado.strip():
                    terminado = True
                # Backspace para borrar
                elif evento.key == pygame.K_BACKSPACE:
                    nombre_ingresado = nombre_ingresado[:-1]
                else:
                    # Agregar caracter si no excede límite
                    if len(nombre_ingresado) < 12:
                        nombre_ingresado += evento.unicode
        
        # Dibujar pantalla de registro
        pantalla_chica.fill((30, 30, 60))  # Fondo azul oscuro
        
        # Texto instructivo
        texto_instruccion = font.render("Ingresa tu nombre:", True, (255, 255, 255))
        pantalla_chica.blit(texto_instruccion, (20, 30))
        
        # Cuadro de entrada de texto
        pygame.draw.rect(pantalla_chica, (255, 255, 255), (20, 80, 360, 40), 2)
        texto_nombre = font.render(nombre_ingresado, True, (255, 255, 255))
        pantalla_chica.blit(texto_nombre, (30, 85))
        
        # Texto para continuar
        texto_continuar = font.render("Presiona ENTER para continuar", True, (200, 200, 0))
        pantalla_chica.blit(texto_continuar, (20, 140))
        
        pygame.display.update()
    
    return nombre_ingresado.strip()  # Devolver nombre sin espacios

def elegir_modo_juego():
    """
    # Objetivo: Permitir al jugador elegir modo de juego
    # Entrada: None (usa click del mouse)
    # Salida: modo_elegido - string "escapa" o "cazador"
    # Restricciones: Debe elegir uno de los dos modos disponibles
    """
    pantalla = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Selección de Modo")
    
    font_grande = pygame.font.SysFont(None, 48)  # Fuente título
    font_normal = pygame.font.SysFont(None, 36)  # Fuente botones
    
    # Definir áreas de botones
    boton_escapa = pygame.Rect(100, 100, 200, 50)
    boton_cazador = pygame.Rect(100, 180, 200, 50)
    
    modo_elegido = None  # Variable para almacenar elección
    
    while modo_elegido is None:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                # Verificar click en botón escapa
                if boton_escapa.collidepoint(evento.pos):
                    modo_elegido = "escapa"
                # Verificar click en botón cazador
                elif boton_cazador.collidepoint(evento.pos):
                    modo_elegido = "cazador"
        
        # Dibujar pantalla de selección
        pantalla.fill((30, 30, 60))  # Fondo azul oscuro
        
        # Título
        titulo = font_grande.render("ELIGE MODO", True, (255, 255, 255))
        pantalla.blit(titulo, (100, 30))
        
        # Botón Modo Escapa (azul)
        color_escapa = (0, 100, 200)
        pygame.draw.rect(pantalla, color_escapa, boton_escapa)
        texto_escapa = font_normal.render("MODO ESCAPA", True, (255, 255, 255))
        # Centrar texto en botón
        pos_x_escapa = boton_escapa.centerx - texto_escapa.get_width() // 2
        pos_y_escapa = boton_escapa.centery - texto_escapa.get_height() // 2
        pantalla.blit(texto_escapa, (pos_x_escapa, pos_y_escapa))
        
        # Botón Modo Cazador (naranja)
        color_cazador = (200, 100, 0)
        pygame.draw.rect(pantalla, color_cazador, boton_cazador)
        texto_cazador = font_normal.render("MODO CAZADOR", True, (255, 255, 255))
        # Centrar texto en botón
        pos_x_cazador = boton_cazador.centerx - texto_cazador.get_width() // 2
        pos_y_cazador = boton_cazador.centery - texto_cazador.get_height() // 2
        pantalla.blit(texto_cazador, (pos_x_cazador, pos_y_cazador))
        
        pygame.display.update()
    
    return modo_elegido

def leer_puntajes_archivo(nombre_archivo):
    """
    # Objetivo: Leer puntajes guardados desde archivo de texto
    # Entrada: nombre_archivo - string con ruta del archivo
    # Salida: puntajes - lista de tuplas (nombre, puntos)
    # Restricciones: Archivo debe tener formato "nombre,puntos"
    """
    puntajes = []  # Lista para almacenar puntajes
    try:
        archivo = open(nombre_archivo, "r")  # CORREGIDO: nombre_archivo en lugar de puntaje
        for linea in archivo:
            partes = linea.strip().split(",")  # Dividir por coma
            if len(partes) == 2:  # Verificar formato correcto
                nombre = partes[0]
                puntos = int(partes[1])  # Convertir a número
                puntajes.append((nombre, puntos))
        archivo.close()
    except:
        # Si el archivo no existe, crear lista vacía
        puntajes = []
    
    return puntajes

def guardar_puntaje_archivo(nombre_archivo, nombre_jugador, puntuacion):
    """
    # Objetivo: Guardar nuevo puntaje en archivo (top 5)
    # Entrada:
    #   nombre_archivo - archivo donde guardar
    #   nombre_jugador - nombre del jugador
    #   puntuacion - puntos a guardar
    # Salida: None (guarda en archivo)
    # Restricciones: Solo guarda top 5 puntajes
    """
    # Leer puntajes existentes
    todos_puntajes = leer_puntajes_archivo(nombre_archivo)
    
    # Agregar nuevo puntaje
    todos_puntajes.append((nombre_jugador, puntuacion))
    
    # Ordenar de mayor a menor (algoritmo burbuja simple)
    for i in range(len(todos_puntajes)):
        for j in range(i + 1, len(todos_puntajes)):
            if todos_puntajes[j][1] > todos_puntajes[i][1]:
                # Intercambiar posiciones
                temp = todos_puntajes[i]
                todos_puntajes[i] = todos_puntajes[j]
                todos_puntajes[j] = temp
    
    # Mantener solo los 5 mejores
    if len(todos_puntajes) > 5:
        todos_puntajes = todos_puntajes[:5]
    
    # Guardar en archivo
    try:
        archivo = open(nombre_archivo, "w")  # Abrir archivo escritura
        for nombre, puntos in todos_puntajes:
            archivo.write(f"{nombre},{puntos}\n")  # Escribir línea
        archivo.close()
    except:
        print("Error guardando puntaje")

def mostrar_pantalla_final(window, mensaje, color, nombre_jugador, puntuacion, modo):
    """
    # Objetivo: Mostrar pantalla final con resultados del juego
    # Entrada:
    #   window - superficie de pygame
    #   mensaje - texto a mostrar ("GANASTE" o "PERDISTE")
    #   color - color del mensaje
    #   nombre_jugador - nombre del jugador
    #   puntuacion - puntos obtenidos
    #   modo - modo de juego
    # Salida: None (muestra pantalla y espera input)
    # Restricciones: Espera hasta que usuario presione tecla o click
    """
    window.fill((0, 0, 0))  # Fondo negro
    font_grande = pygame.font.SysFont(None, 48)  # Fuente grande
    font_normal = pygame.font.SysFont(None, 36)  # Fuente normal
    
    # Mensaje principal (GANASTE/PERDISTE)
    texto_mensaje = font_grande.render(mensaje, True, color)
    # Centrar mensaje en pantalla
    window.blit(texto_mensaje, (ancho_total//2 - texto_mensaje.get_width()//2, 50))
    
    # Información del jugador
    texto_jugador = font_normal.render(f"Jugador: {nombre_jugador}", True, (255, 255, 255))
    window.blit(texto_jugador, (ancho_total//2 - texto_jugador.get_width()//2, 120))
    
    # Puntuación obtenida
    texto_puntos = font_normal.render(f"Puntuación: {puntuacion}", True, (255, 255, 255))
    window.blit(texto_puntos, (ancho_total//2 - texto_puntos.get_width()//2, 160))
    
    # Instrucción para continuar
    texto_continuar = font_normal.render("Presiona cualquier tecla", True, (200, 200, 0))
    window.blit(texto_continuar, (ancho_total//2 - texto_continuar.get_width()//2, 220))
    
    pygame.display.update()
    
    # Esperar input del usuario para continuar
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                esperando = False  # Cualquier tecla
            if evento.type == pygame.MOUSEBUTTONDOWN:
                esperando = False  # Cualquier click

def verificar_colision_trampas(enemigos, trampas, mapa_objetos):
    """
    # Objetivo: Verificar si enemigos pisaron trampas y manejarlo
    # Entrada:
    #   enemigos - lista de objetos Enemigo
    #   trampas - objeto TrampaManager
    #   mapa_objetos - matriz del mapa
    # Salida: puntos_ganados - puntos por eliminar enemigos
    # Restricciones: Solo elimina un enemigo por trampa
    """
    puntos_ganados = 0  # Contador de puntos
    enemigos_eliminados = []  # Lista de enemigos que pisaron trampas
    
    # Revisar cada enemigo
    for enemigo in enemigos:
        # Revisar cada trampa activa
        for trampa in trampas.lista_trampas:
            if enemigo.fila == trampa[0] and enemigo.col == trampa[1]:
                # Enemigo pisó trampa - eliminarla
                trampas.eliminar_trampa(trampa[0], trampa[1])
                puntos_ganados += 50  # Bonus por eliminar enemigo
                enemigos_eliminados.append(enemigo)  # Marcar para respawn
                break  # Solo una trampa por enemigo
    
    # Reposicionar enemigos eliminados
    for enemigo in enemigos_eliminados:
        nueva_fila, nueva_col = obtener_posicion_valida(mapa_objetos)
        enemigo.fila = nueva_fila
        enemigo.col = nueva_col
    
    return puntos_ganados

def verificar_victoria_escapa(jugador, salida_fila, salida_col):
    """
    # Objetivo: Verificar si jugador llegó a la salida en modo escapa
    # Entrada:
    #   jugador - objeto Jugador con posición
    #   salida_fila, salida_col - coordenadas de la salida
    # Salida: True si ganó, False si no
    # Restricciones: Solo aplica para modo escapa
    """
    return jugador.fila == salida_fila and jugador.col == salida_col

def verificar_derrota_escapa(jugador, enemigos):
    """
    # Objetivo: Verificar si enemigo atrapó al jugador en modo escapa
    # Entrada:
    #   jugador - objeto Jugador
    #   enemigos - lista de objetos Enemigo
    # Salida: True si perdió, False si no
    # Restricciones: Solo aplica para modo escapa
    """
    for enemigo in enemigos:
        # Verificar colisión con cada enemigo
        if enemigo.fila == jugador.fila and enemigo.col == jugador.col:
            return True
    return False

def main():
    """
    # Objetivo: Función principal que ejecuta todo el juego
    # Entrada: None (inicia el programa)
    # Salida: None (ejecuta juego completo)
    # Restricciones: Controla flujo completo del juego
    """
    # Pantallas iniciales
    nombre_jugador = pedir_nombre_jugador()
    if not nombre_jugador:  # Si nombre vacío, usar por defecto
        nombre_jugador = "Jugador"
    
    modo_juego = elegir_modo_juego()  # Seleccionar modo
    dificultad = elegir_dificultad()  # Seleccionar dificultad
    
    # Configurar juego según dificultad
    if dificultad == "facil":
        cantidad_enemigos = 2
        velocidad_enemigos = 12  # frames entre movimientos (más lento)
        print("Dificultad: FÁCIL - 2 enemigos, velocidad lenta")
    elif dificultad == "medio":
        cantidad_enemigos = 3  
        velocidad_enemigos = 8   # frames entre movimientos (normal)
        print("Dificultad: MEDIO - 3 enemigos, velocidad normal")
    else:  # dificil
        cantidad_enemigos = 4
        velocidad_enemigos = 4   # frames entre movimientos (más rápido)
        print("Dificultad: DIFÍCIL - 4 enemigos, velocidad rápida")
    
    # Inicializar pygame y ventana principal
    pygame.init()
    ventana = pygame.display.set_mode((ancho_total, alto_total))
    titulo_ventana = f"Escapa del Laberinto - {nombre_jugador} - {dificultad.upper()}"
    pygame.display.set_caption(titulo_ventana)
    
    reloj = pygame.time.Clock()  # Para controlar FPS
    inicializar_imagenes()  # Cargar imágenes de terrenos

    # Crear mundo del juego
    matriz_mapa = generar_mapa()  # Matriz numérica
    mapa_objetos = convertir_a_objetos(matriz_mapa)  # Matriz de objetos
    salida_fila, salida_col = colocar_salida(mapa_objetos)  # Posición salida

    # Crear personajes y objetos del juego
    jugador = Jugador(0, 0)  # Jugador en esquina superior izquierda
    administrador_trampas = TrampaManager()  # Controlador de trampas
    lista_enemigos = crear_enemigos(mapa_objetos, cantidad_enemigos)  # Usa cantidad_enemigos
    
    # Configurar velocidad de enemigos según dificultad
    for enemigo in lista_enemigos:
        enemigo.velocidad_movimiento = velocidad_enemigos

    # Variables para modo cazador
    contador_atrapados = 0  # Contador de enemigos atrapados
    tiempo_inicio_cazador = 0  # Tiempo inicial modo cazador
    
    # Configurar juego según modo
    if modo_juego == "cazador":
        puntuacion_actual = 100  # Puntos iniciales modo cazador
        tiempo_inicio_cazador = time.time()  # Tiempo inicial
    else:
        puntuacion_actual = 0  # Puntos iniciales modo escapa
        tiempo_comienzo = time.time()  # Tiempo inicial para bonus
    
    juego_activo = True  # Control del bucle principal
    
    # BUCLE PRINCIPAL DEL JUEGO
    while juego_activo:
        reloj.tick(fps)  # Mantener 30 FPS

        # PROCESAR EVENTOS
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                juego_activo = False  # Salir del juego
            
            # NUEVO: Tecla ESC para salir durante el juego
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    juego_activo = False  # Salir con ESC
                    break  # Salir del bucle de eventos
                
                # Tecla T para colocar trampa
                if evento.key == pygame.K_t:
                    if administrador_trampas.puede_colocar():
                        administrador_trampas.colocar_trampa(jugador.fila, jugador.col)
                
                # MOVIMIENTO POR TECLAS PRESIONADAS (NO MANTENIDAS)
                if evento.key == pygame.K_LSHIFT or evento.key == pygame.K_RSHIFT:
                    jugador.iniciar_correr()
                
                # MOVIMIENTO EN 4 DIRECCIONES (UNA CELDA POR TECLA)
                if evento.key == pygame.K_UP:
                    jugador.mover(-1, 0, mapa_objetos)  # Arriba - 1 celda
                elif evento.key == pygame.K_DOWN:
                    jugador.mover(1, 0, mapa_objetos)   # Abajo - 1 celda
                elif evento.key == pygame.K_LEFT:
                    jugador.mover(0, -1, mapa_objetos)  # Izquierda - 1 celda
                elif evento.key == pygame.K_RIGHT:
                    jugador.mover(0, 1, mapa_objetos)   # Derecha - 1 celda
            
            # DETENER DE CORRER CUANDO SE SUELTA SHIFT
            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LSHIFT or evento.key == pygame.K_RSHIFT:
                    jugador.detener_correr()

        # ACTUALIZAR ENERGÍA DEL JUGADOR
        jugador.actualizar()

        # MOVIMIENTO DE ENEMIGOS
        for enemigo in lista_enemigos:
            if modo_juego == "escapa":
                enemigo.mover_hacia(jugador.fila, jugador.col, mapa_objetos)
            else:
                enemigo.mover_lejos(jugador.fila, jugador.col, mapa_objetos)

        # VERIFICAR TRAMPAS
        puntos_trampas = verificar_colision_trampas(lista_enemigos, administrador_trampas, mapa_objetos)
        puntuacion_actual += puntos_trampas

        # VERIFICAR CONDICIONES DE FIN DEL JUEGO
        if modo_juego == "escapa":
            # VICTORIA: Llegar a la salida
            if verificar_victoria_escapa(jugador, salida_fila, salida_col):
                tiempo_transcurrido = time.time() - tiempo_comienzo
                bonus_tiempo = max(0, 1000 - int(tiempo_transcurrido * 10))  # Más puntos por menos tiempo
                puntuacion_actual += bonus_tiempo
                
                # Mostrar pantalla de victoria
                mostrar_pantalla_final(ventana, "¡GANASTE!", (255, 255, 0), 
                                     nombre_jugador, puntuacion_actual, modo_juego)
                juego_activo = False
            
            # DERROTA: Enemigo atrapa al jugador
            if verificar_derrota_escapa(jugador, lista_enemigos):
                mostrar_pantalla_final(ventana, "PERDISTE", (255, 0, 0), 
                                     nombre_jugador, puntuacion_actual, modo_juego)
                juego_activo = False

        else:  # MODO CAZADOR
            """
            # Objetivo: Lógica específica del modo cazador
            # - Ganar puntos persiguiendo enemigos (estar cerca)
            # - Perder puntos si enemigos escapan
            # - Victoria: atrapar a todos los enemigos
            # - Derrota: quedarse sin puntos
            """
            
            # PUNTOS POR PERSEGUIR: Ganar puntos por estar cerca de enemigos
            for enemigo in lista_enemigos:
                distancia_filas = abs(enemigo.fila - jugador.fila)
                distancia_columnas = abs(enemigo.col - jugador.col)
                distancia_total = distancia_filas + distancia_columnas
                
                if distancia_total <= 1:  # Muy cerca - más puntos
                    puntuacion_actual += 3
                elif distancia_total <= 2:  # Cerca - puntos normales
                    puntuacion_actual += 1
            
            # PENALIZACIÓN POR TIEMPO: Ir perdiendo puntos gradualmente
            if random.random() < 0.02:  # 2% de probabilidad cada frame
                puntuacion_actual -= 2
            
            # PENALIZACIÓN POR ENEMIGOS EN SALIDA: Si enemigo llega a salida, perder muchos puntos
            for enemigo in lista_enemigos:
                if enemigo.fila == salida_fila and enemigo.col == salida_col:
                    puntuacion_actual -= 100  # Gran penalización
                    # Reposicionar enemigo que escapó
                    nueva_fila, nueva_col = obtener_posicion_valida(mapa_objetos)
                    enemigo.fila = nueva_fila
                    enemigo.col = nueva_col
            
            # BONUS POR ATRAPAR ENEMIGOS: Ganar puntos cuando atrapas un enemigo
            for enemigo in lista_enemigos:
                if enemigo.fila == jugador.fila and enemigo.col == jugador.col:
                    puntuacion_actual += 100  # Bonus por atrapar enemigo
                    contador_atrapados += 1  # Contar enemigo atrapado
                    # Reposicionar enemigo atrapado
                    nueva_fila, nueva_col = obtener_posicion_valida(mapa_objetos)
                    enemigo.fila = nueva_fila
                    enemigo.col = nueva_col
            
            # VICTORIA: Atrapar a cierta cantidad de enemigos (ej: 5)
            if contador_atrapados >= 5:
                tiempo_transcurrido = time.time() - tiempo_inicio_cazador
                bonus_tiempo = max(0, 500 - int(tiempo_transcurrido * 5))  # Bonus por rapidez
                puntuacion_actual += bonus_tiempo
                
                mostrar_pantalla_final(ventana, "¡GANASTE!", (255, 255, 0), 
                                     nombre_jugador, puntuacion_actual, modo_juego)
                juego_activo = False
            
            # DERROTA: Quedarse sin puntos
            if puntuacion_actual <= 0:
                mostrar_pantalla_final(ventana, "PERDISTE", (255, 0, 0), 
                                     nombre_jugador, puntuacion_actual, modo_juego)
                juego_activo = False

        # DIBUJAR TODO EN PANTALLA
        ventana.fill((0, 0, 0))  # Limpiar pantalla con negro
        
        # Dibujar elementos del juego en orden:
        dibujar_mapa(ventana, mapa_objetos)  # 1. Mapa de fondo
        dibujar_salida(ventana, salida_fila, salida_col)  # 2. Salida
        administrador_trampas.dibujar(ventana)  # 3. Trampas
        
        # 4. Enemigos
        for enemigo in lista_enemigos:
            enemigo.dibujar(ventana)
            
        jugador.dibujar(ventana)  # 5. Jugador (sobre otros)
        dibujar_toda_ui(ventana, jugador, administrador_trampas, puntuacion_actual, modo_juego, dificultad)  # 6. UI

        # Dibujar información adicional para modo cazador
        if modo_juego == "cazador":
            mostrar_texto_simple(ventana, f"Atrapados: {contador_atrapados}/5", 20, (255, 255, 255), ancho_mapa + 10, 220)

        pygame.display.update()  # Actualizar pantalla

    # GUARDAR PUNTAJE Y MOSTRAR TOP 5
    archivo_puntajes = f"top5_{modo_juego}.txt"
    guardar_puntaje_archivo(archivo_puntajes, nombre_jugador, puntuacion_actual)

    # NUEVO: Mostrar pantalla Top 5 y preguntar si quiere jugar otra vez
    decision = mostrar_pantalla_top5(ventana, modo_juego)

    if decision == "jugar":
        # Reiniciar el juego llamando a main() otra vez
        pygame.quit()
        main()  # Esto reinicia el juego completo
    else:
        # Salir del juego
        pygame.quit()
        sys.exit()

def verificar_victoria_cazador(jugador, enemigos):
    """
    # Objetivo: Verificar si el jugador atrapó a todos los enemigos en modo cazador
    # Entrada:
    #   jugador - objeto Jugador
    #   enemigos - lista de objetos Enemigo
    # Salida: True si ganó, False si no
    # Restricciones: Solo aplica para modo cazador
    """
    # Contar cuántos enemigos han sido atrapados (están en la misma posición que jugador)
    enemigos_atrapados = 0
    for enemigo in enemigos:
        if enemigo.fila == jugador.fila and enemigo.col == jugador.col:
            enemigos_atrapados += 1
    
    # Victoria: atrapar a todos los enemigos (3 en este caso)
    return enemigos_atrapados >= 3

def verificar_derrota_cazador(puntuacion):
    """
    # Objetivo: Verificar si el jugador perdió en modo cazador (puntos <= 0)
    # Entrada: puntuacion - puntos actuales del jugador
    # Salida: True si perdió, False si no
    # Restricciones: Solo aplica para modo cazador
    """
    return puntuacion <= 0

def elegir_dificultad():
    """
    # Objetivo: Permitir al jugador elegir nivel de dificultad
    # Entrada: None (usa click del mouse)
    # Salida: dificultad - string "facil", "medio", "dificil"
    # Restricciones: Debe elegir una de las tres opciones
    """
    pantalla = pygame.display.set_mode((400, 400))
    pygame.display.set_caption("Selección de Dificultad")
    
    font_titulo = pygame.font.SysFont(None, 48)
    font_boton = pygame.font.SysFont(None, 36)
    
    boton_facil = pygame.Rect(100, 100, 200, 50)
    boton_medio = pygame.Rect(100, 170, 200, 50)
    boton_dificil = pygame.Rect(100, 240, 200, 50)
    
    dificultad_elegida = None
    
    while dificultad_elegida is None:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_facil.collidepoint(evento.pos):
                    dificultad_elegida = "facil"
                elif boton_medio.collidepoint(evento.pos):
                    dificultad_elegida = "medio"
                elif boton_dificil.collidepoint(evento.pos):
                    dificultad_elegida = "dificil"
        
        pantalla.fill((30, 30, 60))
        
        # Título
        titulo = font_titulo.render("DIFICULTAD", True, (255, 255, 255))
        pantalla.blit(titulo, (80, 30))
        
        # Botón Fácil (verde)
        pygame.draw.rect(pantalla, (0, 150, 0), boton_facil)
        texto_facil = font_boton.render("FÁCIL", True, (255, 255, 255))
        pantalla.blit(texto_facil, (boton_facil.centerx - texto_facil.get_width()//2, 
                                  boton_facil.centery - texto_facil.get_height()//2))
        
        # Botón Medio (amarillo)
        pygame.draw.rect(pantalla, (200, 150, 0), boton_medio)
        texto_medio = font_boton.render("MEDIO", True, (255, 255, 255))
        pantalla.blit(texto_medio, (boton_medio.centerx - texto_medio.get_width()//2, 
                                  boton_medio.centery - texto_medio.get_height()//2))
        
        # Botón Difícil (rojo)
        pygame.draw.rect(pantalla, (150, 0, 0), boton_dificil)
        texto_dificil = font_boton.render("DIFÍCIL", True, (255, 255, 255))
        pantalla.blit(texto_dificil, (boton_dificil.centerx - texto_dificil.get_width()//2, 
                                    boton_dificil.centery - texto_dificil.get_height()//2))
        
        pygame.display.update()
    
    return dificultad_elegida


def mostrar_pantalla_top5(window, modo_juego):
    """
    # Objetivo: Mostrar el Top 5 de puntuaciones del modo actual
    # Entrada: window - superficie de pygame, modo_juego - string del modo
    # Salida: None (muestra pantalla y espera input)
    # Restricciones: Espera hasta que usuario presione tecla o click
    """
    archivo_puntajes = f"top5_{modo_juego}.txt"
    puntajes = leer_puntajes_archivo(archivo_puntajes)
    
    window.fill((0, 0, 0))  # Fondo negro
    font_titulo = pygame.font.SysFont(None, 48)
    font_item = pygame.font.SysFont(None, 36)
    font_instruccion = pygame.font.SysFont(None, 24)
    
    # Título
    titulo = font_titulo.render(f"TOP 5 - {modo_juego.upper()}", True, (255, 255, 0))
    window.blit(titulo, (ancho_total//2 - titulo.get_width()//2, 50))
    
    # Mostrar puntajes
    if not puntajes:
        texto_vacio = font_item.render("No hay puntajes aún", True, (255, 255, 255))
        window.blit(texto_vacio, (ancho_total//2 - texto_vacio.get_width()//2, 150))
    else:
        for i, (nombre, puntos) in enumerate(puntajes):
            color = (255, 255, 255)  # Blanco normal
            if i == 0:  # Primer lugar en dorado
                color = (255, 215, 0)
            elif i == 1:  # Segundo lugar en plata
                color = (192, 192, 192)
            elif i == 2:  # Tercer lugar en bronce
                color = (205, 127, 50)
                
            texto_puntaje = font_item.render(f"{i+1}. {nombre}: {puntos} pts", True, color)
            window.blit(texto_puntaje, (ancho_total//2 - texto_puntaje.get_width()//2, 120 + i * 40))
    
    # Instrucción para continuar
    instruccion = font_instruccion.render("Presiona ESC para salir o cualquier otra tecla para jugar otra vez", 
                                         True, (200, 200, 0))
    window.blit(instruccion, (ancho_total//2 - instruccion.get_width()//2, 350))
    
    pygame.display.update()
    
    # Esperar input del usuario
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return "salir"  # Salir del juego
                else:
                    return "jugar"  # Jugar otra vez
            if evento.type == pygame.MOUSEBUTTONDOWN:
                return "jugar"  # Jugar otra vez



main()  # Ejecutar juego
