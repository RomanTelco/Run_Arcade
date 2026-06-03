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
        
        #Generacion de obstaculos
        self.enemigos_restantes = {'Bloque': self.config['Enemigos']['Bloque'], 'Andante': self.config['Enemigos']['Andante'], 'Volador': self.config['Enemigos']['Volador']}
        
        #Timer para generacion continua
        self.ultimo_tiempo_generacion = pygame.time.get_ticks()
        self.tiempo_entre_generaciones = 2000 
        
        #Contador de oleadas
        self.oleada_actual = 0
        
        #Como se generan los elementos
        self.generar_monedas()
        
        #Para debugear
        print(f"\n=== NIVEL {self.config['Nombre']} ===")
        print(f"Enemigos por generar: {self.enemigos_restantes}")
        
        #Generamos la primera oleada
        self.generar_oleada()
        
        
    def generar_oleada(self):
        #Generamos enemigos para el nivel
        self.oleada_actual += 1
        
        #Calculo de cuantos enemigos se generan
        total_restantes = sum(self.enemigos_restantes.values())
        if total_restantes <= 0:
            return
        
        #Numero de enemigos por oleada
        num_enemigos = min(random.randint(2,5), total_restantes)
        print(f"\n --- Oleada {self.oleada_actual} ---")
        print(f"Generando {num_enemigos} enemigos")
        
        for i in range(num_enemigos):
            #Tipo de enemigo
            tipos_disponibles = []
            if self.enemigos_restantes['Bloque'] > 0:
                tipos_disponibles.append('Bloque')
            if self.enemigos_restantes['Andante'] > 0:
                tipos_disponibles.append('Andante')
            if self.enemigos_restantes['Volador'] > 0:
                tipos_disponibles.append('Volador')
                
            if not tipos_disponibles:
                break
            
            tipo = random.choice(tipos_disponibles)
            
            #Posiciones en los que aparecen los enemigos
            if len(self.obstaculos) > 0:
                #Aparicion despues del ultimo enemigo
                ultimo_x = max([o.x for o in self.obstaculos])
                x = ultimo_x + random.randint(300, 600)
            else:
                x = Ventana_ancho + random.randint(100, 300)
             
            #Bloque    
            if tipo == 'Bloque':
                if random.random() < 0.7:
                    y = self.mundo.suelo_y - Enemigos['Bloque']['Alto']
                else:
                    y = random.randint(200, 500)
            
            elif tipo == 'Andante':
                y = self.mundo.suelo_y - Enemigos['Andante']['Alto']
            
            #Volador
            else:
                y = random.randint(100, 400)
                
            #Se crea el enemigo
            self.obstaculos.append(Obstaculo(tipo, x, y, self.numero + 1))
            self.enemigos_restantes[tipo] -= 1
            print(f" - {tipo} en posicion x = {x: .0f}")
        
        #Se muestran enemigos resatntes
        print(f"Restantes: {self.enemigos_restantes}")
    
    def generar_monedas(self):
        #Generamos monedas a utilizar en el juego
        for i in range(self.config['Monedas']):
            x=random.randint(200, 5000)
            y=random.randint(150, 500)
            self.monedas.append({'x':x, 'y':y, 'radio': 12, 'animacion': 0, 'recolectada': False})
    
    def actualizar(self, jugador, balas):
        #Actualizamos el nivel
        
        #Tiempo
        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = (tiempo_actual - self.tiempo_inicio) // 1000
        self.tiempo_restante = max(0, self.tiempo_limite - tiempo_transcurrido)
        
        #Generacion de nuevas oleadas
        total_restantes = sum(self.enemigos_restantes.values())
        if total_restantes > 0:
            if tiempo_actual - self.ultimo_tiempo_generacion > self.tiempo_entre_generaciones:
                self.generar_oleada()
                self.ultimo_tiempo_generacion = tiempo_actual
                #Reducimos tiempo entre oleadas durante el nivel
                if self.tiempo_entre_generaciones > 800:
                    self.tiempo_entre_generaciones -= 50
        
        #Actualizamos obstaculos
        for obstaculo in self.obstaculos[:]:
            if not obstaculo.activo:
                self.obstaculos.remove(obstaculo)
                continue
            
            #Movemos el obstaculo segun la velocidad del nivel
            obstaculo.x += self.mundo.velocidad
            obstaculo.actualizar(self.mundo.velocidad)
            
            #Verificamos el daño hecho por las balas
            for bala in balas[:]:
                puntos = obstaculo.recibir_daño_bala(bala)
                if puntos > 0:
                    jugador.puntuacion += puntos
                    if bala in balas:
                        balas.remove(bala)
            
            #Verificamos la colision con el jugador
            if obstaculo.colisionar_jugador(jugador):
                if not obstaculo.activo:
                    if obstaculo in self.obstaculos:
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
        
        
        #Generar nuevas monedas
        if len(self.monedas) < 20:
            nuevas_monedas = random.randint(3, 8)
            for i in range(nuevas_monedas):
                x=self.mundo.distancia_recorrida + random.randint(400, 1000)
                y= random.randint(150, 500)
                self.monedas.append({'x':x, 'y':y, 'radio':12, 'animacion':0, 'recolectada': False})
        
        #Nivel completado?
        if self.mundo.progreso >= 100:
            self.completado = True
            jugador.puntuacion += self.tiempo_restante * 10
            print(f"\n Nivel Completado! Puntuacion: {jugador.puntuacion}")
        
        #Tiempo terminado?
        if self.tiempo_restante <= 0:
            jugador.morir()
            print("\n Tiempo Agotado!")
    
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
            