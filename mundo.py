# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 19:39:33 2026

@author: Neo-PC
"""

import pygame
import random
import math
from config import *

#Fichero del mundo del juego
class Mundo:
    def __init__(self,nivel_numero):
        self.nivel_numero = nivel_numero
        self.nivel_config = Niveles[nivel_numero]
        
        #Propiedades que va a tener el mundo del juego
        self.velocidad = self.nivel_config['Velocidad']
        self.distancia_recorrida = 0
        self.progreso = 0
        
        #Elementos del escenario
        self.suelo_y = Ventana_alto - 150
        self.nubes = []
        self.decoraciones = []
        
        #Generacion de elementos iniciales
        self.generar_nubes()
        self.generar_decoraciones()
        
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
        self.distancia_recorrida -= self.velocidad
        self.progreso = min(100, (self.distancia_recorrida / 10000)*100)
        
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
    
    def dibujar(self,pantalla):
        #Cielo
        pantalla.fill(Colores['Cielo'])
        
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
                
                
                
                
                