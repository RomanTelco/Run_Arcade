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
        
        #Como se generan los elementos
        self.generar_enemigos()
        self.generar_monedas()
        
    def generar_enemigos(self):
        #Generamos enemigos para el nivel
        cantidad = self.config['Enemigos']
        
        #Bloque
        for i in range(cantidad['Bloque']):
            x=random.randint(300, 5000)
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
            