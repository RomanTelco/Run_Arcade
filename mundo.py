# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 19:39:33 2026

@author: Neo-PC
"""

import pygame
import random
import math
import array
from config import *

#Sonido del viento en el nivel 1
def crear_sonido_viento(duracion = 4.0, volumen = 0.02):
    config_audio = pygame.mixer.get_init()
    if not config_audio:
        return None
    
    frecuencia_muestreo, formato, canales = config_audio
    total_muestras = int(frecuencia_muestreo * duracion)
    ruido = [random.uniform(-1, 1) for _ in range(total_muestras)]
    valores = []
    suave1 = 0
    suave2 = 0
    
    for vuelta in range(2):
        for i in range(total_muestras):
            suave1 = suave1 * 0.93 + ruido[i] * 0.07
            suave2 = suave2 * 0.93 + suave1 * 0.07
            
            if vuelta == 1:
                fase = 2 * math.pi * i / total_muestras
                rachas = 0.65 + 0.35 * math.sin(fase) + 0.2 * math.sin(3*fase + 1)
                valores.append(suave2 * rachas)
                
    maximo = max(abs(v) for v in valores)
    muestras = array.array('h')
    for v in valores:
        valor = int(32767 * volumen * v/maximo)
        for _ in range(canales):
            muestras.append(valor)
            
    return pygame.mixer.Sound(buffer = muestras.tobytes())

#Sonido de la lluvia en el nivel 2
def crear_sonido_lluvia(duracion = 2.0, volumen = 0.02):
    config_audio = pygame.mixer.get_init()
    if not config_audio:
        return None
    frecuencia_muestreo, formato, canales = config_audio
    total_muestras = int(frecuencia_muestreo * duracion)
    ruido = [random.uniform(-1, 1) for _ in range(total_muestras)]
    gotas = [random.uniform(-1, 1) * 0.6 if random.random() < 0.0009 else 0 for _ in range(total_muestras)]
    muestras = array.array('h')
    anterior = 0
    
    for vuelta in range(2):
        for i in range(total_muestras):
            anterior = anterior * 0.89 + ruido[i] * 0.1
            mezcla = anterior * 1.2
            if vuelta == 1:
                valor = int(32767 * volumen * mezcla)
                valor = max(-32768, min(32767, valor))
                for _ in range(canales):
                    muestras.append(valor)
    return pygame.mixer.Sound(buffer = muestras.tobytes())

            

#Fichero del mundo del juego
class Mundo:
    sonido_lluvia = None
    canal_lluvia = None
    sonido_viento = None
    canal_viento = None
    
    def __init__(self,nivel_numero):
        self.nivel_numero = nivel_numero
        self.nivel_config = Niveles[nivel_numero]
        
        #Propiedades que va a tener el mundo del juego
        self.velocidad = self.nivel_config['Velocidad']
        self.distancia_recorrida = 0
        self.progreso = 0
        
        #Color de fondo
        self.color_fondo = self.nivel_config.get('Color_fondo', Colores['Cielo'])
        
        self.tiempo_inicio = pygame.time.get_ticks()
        self.tiempo_limite = self.nivel_config['Tiempo_limite']
        
        if nivel_numero == 0:
            self.distancia_total = 4000
        else:
            self.distancia_total = 7000
        
        #Elementos del escenario
        self.suelo_y = Ventana_alto - 150
        self.nubes = []
        self.decoraciones = []
        
        #Generacion de elementos iniciales
        self.generar_nubes()
        self.generar_decoraciones()
        
        #Viento en el nivel 1
        self.viento = (nivel_numero == 1)
        
        #Lluvia en el nivel 2
        self.lluvia = (nivel_numero == 2)
        self.gotas = []
        if self.lluvia:
            self.generar_lluvia()
            self.capa_lluvia = pygame.Surface((Ventana_ancho, Ventana_alto), pygame.SRCALPHA)
            self.capa_lluvia.fill((0,0,40,60))
            
        #Nieve en el nivel 5
        self.nieve = (nivel_numero == 5)
        self.copos = []
        if self.nieve:
            self.generar_nieve()
    
    
    def iniciar_cronometro(self):
        self.tiempo_inicio = pygame.time.get_ticks()
    
    def generar_nubes(self):
        for i in range(8):
            x = random.randint(0, Ventana_ancho*2)
            y = random.randint(50, 200)
            tamaño = random.randint(30, 60)
            velocidad = random.uniform(0.1, 0.3)
            self.nubes.append({'x':x, 'y':y, 'tamaño':tamaño, 'velocidad': velocidad})
    
    def generar_decoraciones(self):
        #Montañas
        for i in range(4):
            x = i*400
            altura = random.randint(100, 200)
            self.decoraciones.append({'tipo':'montaña', 'x':x, 'y':self.suelo_y-altura, 'ancho':300, 'alto':altura, 'color':Colores['Montaña']})
            
        #Arbustos
        for i in range(15):
            x= i*200 + random.randint(-50, 50)
            tamaño = random.randint(20,40)
            self.decoraciones.append({'tipo':'arbusto', 'x':x, 'y':self.suelo_y-tamaño, 'tamaño': tamaño, 'color': Colores['Arbusto']})
            
    def actualizar(self):
        #Actualizamos la posicion de todos los elementos
        
        #Distancia recorrida
        self.distancia_recorrida += abs(self.velocidad)
        
        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = (tiempo_actual - self.tiempo_inicio) / 1000
        
        self.progreso = min(100, (tiempo_transcurrido / self.tiempo_limite)*100)
        
        #Movimiento de las nubes
        for nube in self.nubes:
            nube['x'] += self.velocidad * nube['velocidad']
            if nube['x'] < -100:
                nube['x'] = Ventana_ancho + 100
                nube['y'] = random.randint(50, 200)
        
        #Movimiento decoraciones
        for decoracion in self.decoraciones:
            decoracion['x'] += self.velocidad
            #Reposicionamiento por si sale de la pantalla
            if decoracion['x'] < -500:
                decoracion['x'] = Ventana_ancho + 500
                if decoracion['tipo'] == 'arbusto':
                    decoracion['tamaño'] = random.randint(20, 40)
        
        #Lluvia
        if self.lluvia:
            self.actualizar_lluvia()
        
        #Nieve
        if self.nieve:
            self.actualizar_nieve()
            
    
    def dibujar(self,pantalla):
        #Cielo
        pantalla.fill(self.color_fondo)
        
        #Nubes
        for nube in self.nubes:
            #Nube principal
            pygame.draw.circle(pantalla, Colores['Nube'], (int(nube['x']), int(nube['y'])), nube['tamaño'])
            #Nube lateral
            pygame.draw.circle(pantalla, Colores['Nube'], (int(nube['x'] + nube['tamaño']*0.7),int(nube['y'] - nube['tamaño']*0.3)), nube['tamaño'] * 0.8)
            pygame.draw.circle(pantalla, Colores['Nube'], (int(nube['x'] - nube['tamaño']*0.7),int(nube['y'] - nube['tamaño']*0.3)), nube['tamaño'] * 0.8)
            
        #Montañas
        for decoracion in self.decoraciones:
            if decoracion['tipo'] == 'montaña':
                puntos = [(decoracion['x'], decoracion['y'] + decoracion['alto']),(decoracion['x'] + decoracion['ancho']//2, decoracion['y']),(decoracion['x'] + decoracion['ancho'], decoracion['y'] + decoracion['alto'])]
                pygame.draw.polygon(pantalla, decoracion['color'], puntos)
        
        #Suelo
        pygame.draw.rect(pantalla, Colores['Suelo'], (0,self.suelo_y,Ventana_ancho,150))
        
        #Hierba
        pygame.draw.rect(pantalla, Colores['Hierba'], (0,self.suelo_y - 10, Ventana_ancho, 20))
        
        #Linea del camino
        for i in range(0,Ventana_ancho, 60):
            if(i//60) % 2 == 0:
                pygame.draw.rect(pantalla, Colores['Camino'], (i, self.suelo_y + 50, 40, 10))
                
        #Arbustos
        for decoracion in self.decoraciones:
            if decoracion['tipo'] == 'arbusto':
                radio = decoracion['tamaño']
                centro_x = decoracion['x']
                centro_y = decoracion['y']
                
                pygame.draw.circle(pantalla,decoracion['color'], (centro_x, centro_y), radio)
                pygame.draw.circle(pantalla,decoracion['color'], (centro_x + radio*0.7, centro_y - radio*0.5), radio*0.8)
                pygame.draw.circle(pantalla,decoracion['color'], (centro_x - radio*0.7, centro_y - radio*0.5), radio*0.8)
                
        #LLuvia
        if self.lluvia:
            self.dibujar_lluvia(pantalla)
        
        #Nieve
        if self.nieve:
            self.dibujar_nieve(pantalla)
            
            
        
                
    def generar_lluvia(self):
        for i in range(150):
            self.gotas.append({'x': random.randint(0, Ventana_ancho + 200),'y': random.randint(-Ventana_alto, Ventana_alto), 'largo': random.randint(10, 20), 'velocidad_y': random.randint(12, 20), 'velocidad_x': random.uniform(-3, -1.5)})
            
    def generar_nieve(self):
        for i in range(120):
            self.copos.append({'x': random.randint(0, Ventana_ancho + 200),'y': random.randint(-Ventana_alto, Ventana_alto), 'radio': random.randint(2, 4), 'velocidad_y': random.uniform(1.5, 3.5), 'velocidad_x': random.uniform(-2, -0.5), 'fase': random.uniform(0, math.pi * 2)})
    
    def actualizar_lluvia(self):
        for gota in self.gotas:
            gota['y'] += gota['velocidad_y']
            gota['x'] += gota['velocidad_x']
            #Para que aparezcan de nuevo
            if gota['y'] > self.suelo_y + random.randint(0, 120) or gota['x'] < -20:
                gota['x'] = random.randint(0, Ventana_ancho + 200)
                gota['y'] = random.randint(-100, 0)
    
    def actualizar_nieve(self):
        for copo in self.copos:
            copo['fase'] += 0.05
            copo['y'] += copo['velocidad_y']
            copo['x'] += copo['velocidad_x'] + math.sin(copo['fase']) * 0.8
            #Para que aparezcan de nuevo
            if copo['y'] > self.suelo_y + random.randint(0, 100) or copo['x'] < -20:
                copo['x'] = random.randint(0, Ventana_ancho + 200)
                copo['y'] = random.randint(-100, 0)
    
    def dibujar_lluvia(self, pantalla):
        pantalla.blit(self.capa_lluvia, (0,0))
        for gota in self.gotas:
            x, y = int(gota['x']), int(gota['y'])
            cola_x = int(x - gota['velocidad_x'] *2)
            cola_y = y - gota['largo']
            pygame.draw.line(pantalla, (170,200,255), (cola_x, cola_y), (x,y), 1)
            
    def dibujar_nieve(self, pantalla):
        for copo in self.copos:
            pygame.draw.circle(pantalla, (255,255,255), (int(copo['x']),int(copo['y'])), copo['radio'])
            
    def controlar_sonido_lluvia(self, jugando):
        
        self.controlar_sonido_viento(jugando)
        
        try:
            if self.lluvia and jugando:
                if Mundo.sonido_lluvia is None:
                    Mundo.sonido_lluvia = crear_sonido_lluvia()
                if Mundo.sonido_lluvia and (Mundo.canal_lluvia is None or not Mundo.canal_lluvia.get_busy()):
                    Mundo.canal_lluvia = Mundo.sonido_lluvia.play(loops = -1)
            elif Mundo.canal_lluvia is not None:
                Mundo.canal_lluvia.stop()
                Mundo.canal_lluvia = None
        except pygame.error:
            pass
                 
    def controlar_sonido_viento(self, jugando):
        try:
            if self.viento and jugando:
                if Mundo.sonido_viento is None:
                    Mundo.sonido_viento = crear_sonido_viento()
                if Mundo.sonido_viento and (Mundo.canal_viento is None or not Mundo.canal_viento.get_busy()):
                    Mundo.canal_viento = Mundo.sonido_viento.play(loops = -1)
            elif Mundo.canal_viento is not None:
                Mundo.canal_viento.stop()
                Mundo.canal_viento = None
        except pygame.error:
            pass
                    
                    
                
                