# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 14:08:16 2026

@author: Neo-PC
"""

#Fichero con misiles
import pygame
import random
import math
import array
from config import *

def crear_sonido_misil(duracion = 0.45, volumen = 0.3):
    config_audio = pygame.mixer.get_init()
    if not config_audio:
        return None
    
    frecuencia_muestreo, formato, canales = config_audio
    total_muestras = int(frecuencia_muestreo * duracion)
    muestras = array.array('h')
    anterior = 0
    fase = 0
    
    for i in range(total_muestras):
        progreso = i / total_muestras
        anterior = anterior * 0.75 + random.uniform(-1, 1) * 0.25
        ataque = min(1, i / 600)
        envolvente = ataque * (1 - progreso) ** 1.5
        frecuencia = 120 + 160 * progreso
        fase += 2 * math.pi * frecuencia / frecuencia_muestreo
        mezcla = anterior * 0.9 + math.sin(fase) * 0.4
        valor = int(32767 * volumen * envolvente * mezcla)
        valor = max(-32768, min(32767, valor))
        for _ in range(canales):
            muestras.append(valor)
    
    return pygame.mixer.Sound(buffer = muestras.tobytes())

def crear_imagen_misil():
    imagen = pygame.Surface((34, 12), pygame.SRCALPHA)
    pygame.draw.rect(imagen, (170,170,180), (0,1,26,10))
    pygame.draw.rect(imagen, (120,120,130), (0,0,6,12))
    pygame.draw.polygon(imagen, (120,40,40), [(26,0), (34,6), (26,12)])
    return imagen

def disparar_misil(jugador):
    if jugador.tiempo_entre_misil > 0 or jugador.misiles <= 0:
        return None
    
    jugador.tiempo_entre_misil = 40
    jugador.misiles -= 1
    
    try:
        if jugador.sonido_misil is None:
            jugador.sonido_misil = crear_sonido_misil()
        if jugador.sonido_misil:
            jugador.sonido_misil.play()
    except pygame.error:
        pass
    
    angulo = jugador.angulo_apuntado
    velocidad = 10
    return {'x': jugador.x + jugador.ancho // 2 - 17,
            'y': jugador.y + jugador.alto // 2 - 6,
            'ancho': 34,
            'alto': 12,
            'velocidad_x': math.cos(angulo) * velocidad,
            'velocidad_y': math.sin(angulo) * velocidad,
            'color': (220,40,40),
            'angulo': angulo,
            'tipo':'misil',
            'daño': 3
            }

def dibujar_misil(pantalla, bala, imagen):
    angulo = bala['angulo']
    centro_x = bala['x'] + bala['ancho'] // 2
    centro_y = bala['y'] + bala['alto'] // 2
    
    llama_radio = 4 + (pygame.time.get_ticks() // 60) % 3
    llama_x = int(centro_x - math.cos(angulo) * 24)
    llama_y = int(centro_y - math.sin(angulo) * 24)
    pygame.draw.circle(pantalla, (255,140,0), (llama_x, llama_y), llama_radio + 2)
    pygame.draw.circle(pantalla, (255,230,80), (llama_x, llama_y), llama_radio)
    
    rotada = pygame.transform.rotate(imagen, - math.degrees(angulo))
    pantalla.blit(rotada, rotada.get_rect(center = (centro_x, centro_y)))
    