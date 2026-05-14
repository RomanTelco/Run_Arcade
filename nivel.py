# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 19:33:14 2026

@author: Neo-PC
"""

import pygame
import random
import math
from config import *
from obstaculo import Obstaculo

#Fichero con niveles utilizados en el juego
class Nivel:
    def __init__(self, numero, mundo):
        self.numero = numero
        self.mundo = mundo
        self.config = Niveles[numero]
        
        #Estado del nivel
        self.completado = False
        self.tiempo_inicio = pygame.time.get_ticks()
        self.tiempo_limite = self.config['Tiempo_limite']
        self.tiempo_restante = self.tiempo_limite
        
        #Elementos que se encuentran en el nivel
        self.obstaculos = []
        self.monedas = []
        
        #generacion de obstaculos
        self.ultima_posicion_generada = 0
        self.distancia_entre_obstaculos = 350
        
        #Como se generan los elementos
        self.generar_enemigos()
        self.generar_monedas()
        
    def generar_enemigos(self):
        #Generamos enemigos para el nivel
        cantidad = self.config['Enemigos']
        
        #Bloque
        for i in range(15):
            x=random.randint(200, 8000)
            y=self.mundo.suelo_y - Enemigos['Bloque']['Alto']
                
            self.obstaculos.append(Obstaculo('Bloque', x, y, self.numero +1))
            
        #Andante
        for i in range(cantidad['Andante']):
            x=random.randint(500, 6000)
            y=self.mundo.suelo_y - Enemigos['Andante']['Alto']
            self.obstaculos.append(Obstaculo('Andante', x, y, self.numero +1))
            
        #Volador
        for i in range(cantidad['Volador']):
            x=random.randint(700, 8000)
            y=random.randint(100, 400)
            self.obstaculos.append(Obstaculo('Volador', x, y, self.numero +1))
            
        bloques_extra = 20
        for i in range(bloques_extra):
            x = random.randint(300, 9000)
            #Alterno suelo y cielo
            if i % 3 == 0:
                y = random.randint(300, 500)
            else:
                y = self.mundo.suelo_y - Enemigos['Bloque']['Alto']
            self.obstaculos.append(Obstaculo('Bloque', x, y, self.numero +1))    
    
    def generar_nuevo_obstaculo(self, posicion_x):
        rand= random.random()
        if rand < 0.6:
            tipo = 'Bloque'
            if random.random() < 0.8:
                y = self.mundo.suelo_y - Enemigos['Bloque']['Alto']
            else:
                y = random.randint(300, 500)
        elif rand < 0.8:
            tipo = 'Andante'
            y = self.mundo.suelo_y - Enemigos['Andante']['Alto']
        else:
            tipo = 'Volador'
            y=random.randint(100, 400)
            
        self.obstaculos.append(Obstaculo(tipo, posicion_x, y, self.numero + 1))
                    
    
    def generar_monedas(self):
        #Generamos monedas a utilizar en el juego
        for i in range(self.config['Monedas']):
            x=random.randint(200, 10000)
            y=random.randint(200, 500)
            self.monedas.append({'x':x, 'y':y, 'radio': 12, 'animacion': 0, 'recolectada': False})
    
    def actualizar(self, jugador, balas):
        #Actualizamos el nivel
        
        #Tiempo
        tiempo_transcurrido = (pygame.time.get_ticks()-self.tiempo_inicio) // 1000
        self.tiempo_restante = max(0, self.tiempo_limite - tiempo_transcurrido)
        
        distancia_actual = abs(self.mundo.distancia_recorrida)
        if distancia_actual - self.ultima_posicion_generada > self.distancia_entre_obstaculos:
            nueva_pos = distancia_actual + self.distancia_entre_obstaculos + random.randint(50, 200)
            self.generar_nuevo_obstaculo(nueva_pos)
            self.ultima_posicion_generada = distancia_actual
            
            if random.random() < 0.3:
                nueva_pos2 = nueva_pos + random.randint(100, 250)
                self.generar_nuevo_obstaculo(nueva_pos2)
        
        #Obstaculo
        for obstaculo in self.obstaculos[:]:
            if not obstaculo.activo:
                self.obstaculos.remove(obstaculo)
                continue
            obstaculo.actualizar(self.mundo.velocidad)
            
            #Verificamos daño por bala
            for bala in balas[:]:
                puntos = obstaculo.recibir_daño_bala(bala)
                if puntos > 0:
                    jugador.puntuacion += puntos
                    if bala in balas:
                        balas.remove(bala)
            
            #Verificamos daño con el jugador
            if obstaculo.colisionar_jugador(jugador):
                if not obstaculo.activo:
                    self.obstaculos.remove(obstaculo)
                
        #Monedas
        for moneda in self.monedas[:]:
            if moneda['recolectada']:
                self.monedas.remove(moneda)
                continue
            
            #Movimiento del mundo
            moneda['x'] += self.mundo.velocidad
            moneda['animacion'] = (moneda['animacion'] + 0.2) % (3.14 * 2)
            
            #Verificamos la recoleccion por parte del jugador
            moneda_rect = pygame.Rect(moneda['x'] - moneda['radio'], moneda['y'] - moneda['radio'], moneda['radio'] * 2, moneda['radio'] * 2)
            
            if moneda_rect.colliderect(jugador.rect):
                moneda['recolectada'] = True
                jugador.recolectar_moneda()
        
        #Nivel completado?
        if self.mundo.progreso >= 100:
            self.completado = True
            jugador.puntuacion += self.tiempo_restante * 10
        
        #Tiempo terminado?
        if self.tiempo_restante <= 0:
            jugador.morir()
    
    def dibujar(self,pantalla):
        #Elementos del nivel
        
        #Monedas
        for moneda in self.monedas:
            if not moneda['recolectada']:
                #Flotante
                y_offset = math.sin(moneda['animacion']) * 5
                
                #Moneda exterior
                pygame.draw.circle(pantalla, Colores['Moneda'], (int(moneda['x']),int(moneda['y'] + y_offset)), moneda['radio'])
                
                #Moneda interior
                pygame.draw.circle(pantalla, (255,230,0), (int(moneda['x']), int(moneda['y'] + y_offset)), moneda['radio']-4)
                #Centro de la moneda
                pygame.draw.circle(pantalla, (255,200,0), (int(moneda['x']), int(moneda['y'] + y_offset)), moneda['radio']-8)
                
        #Obstaculos
        for obstaculo in self.obstaculos:
            obstaculo.dibujar(pantalla)
            