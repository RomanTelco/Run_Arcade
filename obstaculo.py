# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 19:52:42 2026

@author: Neo-PC
"""

import pygame
import random
import math
from config import *

#Fichero con las clases de los obstaculos
class Obstaculo:
    def __init__(self, tipo, x, y, nivel = 1):
        self.tipo = tipo
        self.nivel = nivel
        
        #Configuracion segun el tipo de obstaculo
        config = Enemigos[tipo]
        
        #Propiedades del obstaculo
        self.ancho = config['Ancho']
        self.alto = config['Alto']
        self.color = config['Color']
        self.velocidad = config['Velocidad']
        self.vida = config['Vida']
        self.puntos = config['Puntos'] * nivel
        
        #Movimiento y posicion de los obstaculos
        self.x = x
        self.y = y
        self.velocidad_x = self.velocidad
        self.velocidad_y = 0
        
        #Estados en los que se encuentra el obstaculo
        self.activo = True
        self.daño_tiempo = 0
        
        #Tipo de obstaculo que se encuentran por el camino
        self.estatico = (config['Tipo'] == 'estatico')
        self.terrestre = (config['Tipo'] == 'terrestre')
        self.aereo = (config['Tipo'] == 'aereo')
        
        #Animacion de los obstaculos
        self.animacion_frame = 0
        self.animacion_tiempo = 0
        
        #Obstaculos voladores
        self.tiempo_vuelo = 0
        self.altura_inicial = y
        
        #Obstaculos andantes
        self.direccion = -1
        self.tiempo_cambio = 0
        
        #Cuando el personaje pricipal colisiona con el obstaculo
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        
    def actualizar(self, velocidad_mundo):
        #Actualizacion de la posicion del obstaculo
        if not self.activo:
            return
        
        #Movimiento en la pantalla principal
        self.x += velocidad_mundo
        
        #Movimiento estatico
        if self.estatico:
            pass
        
        #Movimiento terrestre
        elif self.terrestre:
            self.x += self.velocidad_x
            #Cambio de direccion
            self.tiempo_cambio += 1
            if self.tiempo_cambio > 120:
                self.velocidad_x *= -1
                self.tiempo_cambio = 0
                
            #Gravedad para el obstaculo
            self.velocidad_y += Gravedad * 0.5
            self.y += self.velocidad_y
            
            #Obstaculo en el suelo
            suelo_y = Ventana_alto - 150
            if self.y >= suelo_y -self.alto:
                self.y = suelo_y - self.alto
                self.velocidad_y = 0
        
        #Movimiento volador
        elif self.aereo:
            self.x += self.velocidad_x
            self.tiempo_vuelo += 0.1
            amplitud = 50
            frecuencia = 0.05
            self.y = self.altura_inicial + math.sin(self.tiempo_vuelo * frecuencia) * amplitud
            
            #Cambio aleatorio de altura
            if random.random() < 0.005:
                self.altura_inicial = random.randint(100, 400)
            
        #Actualizacion de animacion
        self.animacion_tiempo += 1
        if self.animacion_tiempo > 5:
            self.animacion_frame = (self.animacion_frame + 1) % 4
            self.animacion_tiempo = 0
            
        #Actualizacion del tiempo de daño
        if self.daño_tiempo > 0:
            self.daño_tiempo -= 1
            
        #Actualizacion de colision
        self.rect.x = self.x
        self.rect.y = self.y
            
        #Cuando sale de la pantalla se elimina el obstaculo
        if self.x < -100 or self.x > Ventana_ancho + 100:
            self.activo = False
    
    #Dibujamos el obstaculo
    def dibujar(self,pantalla):
        if not self.activo:
            return
        color = self.color
        if self.daño_tiempo > 0 and self.daño_tiempo % 4 < 2:
            color = (255,255,255)
            
        #Tipos de obstaculos
        #Cubo simple
        if self.tipo == 'Bloque':
            pygame.draw.rect(pantalla, color, self.rect)
            pygame.draw.rect(pantalla, (70,70,70), (self.x + 5, self.y + 5,self.ancho - 10,self.alto - 10), 2)
            
            #Grietas en el cubo
            for i in range(3):
                x_grieta = self.x + random.randint(10, self.ancho - 10)
                y_grieta = self.y + random.randint(10, self.alto - 10)
                largo = random.randint(5, 15)
                pygame.draw.line(pantalla, (50,50,50), (x_grieta,y_grieta), (x_grieta + largo, y_grieta),2)
        
        #Andante
        elif self.tipo == 'Andante':
            cuerpo_rect = pygame.Rect(self.x, self.y, self.ancho, self.alto - 20)
            pygame.draw.rect(pantalla, (200,150,150), cuerpo_rect)
            
            direccion = 1 if self.velocidad_x > 0 else -1
            
            ojo_offset = 5 * direccion
            ojo_izquierdo = (self.x + 15 + ojo_offset, self.y + 10)
            ojo_derecho = (self.x + self.ancho - 15 + ojo_offset, self.y + 10)
            pygame.draw.circle(pantalla, (0,0,0), ojo_izquierdo, 4)
            pygame.draw.circle(pantalla, (0,0,0), ojo_derecho, 4)
            
            brazo_offset = math.sin(self.animacion_frame * 0.8) * 10
            pygame.draw.line(pantalla, color, (self.x + 5, self.y + 30), (self.x - 10 - brazo_offset, self.y + 40), 6)
            pygame.draw.line(pantalla, color, (self.x + self.ancho - 5, self.y + 30), (self.x + self.ancho + 10 + brazo_offset, self.y + 40),6)
            
            pierna_offset = math.sin(self.animacion_frame * 0.8) * 15
            pygame.draw.line(pantalla, (150,50,50), (self.x + 10, self.y + self.alto - 10), (self.x + 5 - pierna_offset, self.y + self.alto + 10), 8)
            pygame.draw.line(pantalla, (150,50,50), (self.x + self.ancho - 10, self.y + self.alto - 10), (self.x + self.ancho - 5 + pierna_offset, self.y + self.alto + 10), 8)
            
        #Volador
        elif self.tipo == 'Volador':
            puntos=[(self.x + self.ancho//2,self.y), (self.x + self.ancho, self.y + self.alto // 3), (self.x + self.ancho * 0.8, self.y + self.alto), (self.x + self.ancho * 0.2, self.y + self.alto), (self.x, self.y + self.alto // 3)]
            pygame.draw.polygon(pantalla, color, puntos)
            ventana_rect = pygame.Rect(self.x + self.ancho // 2 - 10, self.y + 5, 20, 15)
            pygame.draw.ellipse(pantalla, (200,200,255), ventana_rect)
            
            ala_offset = math.sin(self.animacion_frame) * 5
            pygame.draw.ellipse(pantalla, (150,0,200), (self.x - 5, self.y + 10 - ala_offset,self.ancho + 10, 10))
            pygame.draw.ellipse(pantalla, (150, 0,200), (self.x - 5, self.y + self.alto - 20 + ala_offset, self.ancho + 10, 10))
            
            propulsor_color = (255,100,0) if self.animacion_frame % 2 == 0 else(255,200,0)
            pygame.draw.circle(pantalla, propulsor_color, (self.x + self.ancho//2, self.y + self.alto), 8)
            
        #Vida
        if self.vida > 1 and self.vida < 999:
            fuente = pygame.font.Font(None,20)
            texto = fuente.render(str(self.vida), True, (255,255,255))
            pantalla.blit(texto, (self.x + self.ancho//2 - 5, self.y - 15))
            
    def recibir_daño_bala(self,bala):
        if not self.activo:
            return 0
        
        bala_rect = pygame.Rect(bala['x'], bala['y'], bala['ancho'], bala['alto'])
        
        #Verificacion del alcance por parte de la bala al enemigo
        if self.rect.colliderect(bala_rect):
            if self.tipo == 'Bloque':
                return 0
            
            self.vida -= 1
            self.daño_tiempo = 20
            
            if self.vida <= 0:
                self.activo = False
                return self.puntos
            else:
                return self.puntos // 2
            
        return 0
            
                
    def colisionar_jugador(self,jugador):
        #Manejar colision conj el jugador
        if not self.activo:
            return False
        
        if self.rect.colliderect(jugador.rect):
            #Comportamientos de los obstaculos
            
            #Bloque: salto por encima
            if self.tipo == 'Bloque':
                if(jugador.velocidad_y > 0 and jugador.pies_rect.colliderect(pygame.Rect(self.x,self.y,self.ancho,10))):
                    #Rebote
                    jugador.velocidad_y = -8
                    return True
                else:
                    #Colision lateral
                    if jugador.x < self.x:
                        jugador.x = self.x - jugador.ancho - 5
                    else:
                        jugador.x = self.x + self.ancho + 5
                    jugador.velocidad_x =  0
                    return True
                
            #Andante: salto por encima
            elif self.tipo == 'Andante':
                if(jugador.velocidad_y > 0 and jugador.pies_rect.colliderect(pygame.Rect(self.x, self.y, self.ancho, 15))):
                    #Salto por encima del enemigo
                    jugador.velocidad_y = -10
                    puntos = self.recibir_daño_salto()
                    if puntos > 0:
                        jugador.puntuacion += puntos
                        return True
                    else:
                        #Colision con el personaje principal
                        jugador.recibir_daño()
                        return True
           
            #Volador: Daño permanente
            elif self.tipo =='Volador':
                jugador.recibir_daño()
                return True
        return False

    
    def recibir_daño_salto(self):
        #Se recibe daño por el salto del jugador
        if self.tipo == 'Andante':
            self.vida -= 1
            self.daño_tiempo = 20
            if self.vida <= 0:
                self.activo = False
                return self.puntos
            else:
                #Rebote 
                self.velocidad_y = -5
                return self.puntos // 2
        return 0
            
        
           
        