# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 21:10:22 2026

@author: Neo-PC
"""

#jefe del nivel 3
import pygame
import random
import math
from config import *
from jefe import Jefe

class JefeGolem(Jefe):
    def __init__(self, config_jefe, suelo_y):
        super().__init__(config_jefe, suelo_y)
        
        #Area del jefe del nivel 3
        self.limite_izquierdo = self.limite_derecho - 150
        
        #Ondas de choque y chispas del jefe
        self.ondas = []
        self.chispas = []
        
        #Fotogramas de la armadura abierta y preparacion
        self.tiempo_pisoton = 200
        self.preparando = 0
        self.abierto = 0
        
    def mover(self, jugador):
        #Empieza a caminar de un lado para otro para la preparacion
        if self.preparando > 0:
            return
        
        self.x += self.direccion * 0.8
        if self.x <= self.limite_izquierdo:
            self.x = self.limite_izquierdo
            self.direccion = 1
        elif self.x >= self.limite_derecho:
            self.x = self.limite_derecho
            self.direccion = -1
    
    def disparar(self, jugador):
        furioso = self.furioso()
        
        #Ataque 1: lanzamiento de rocas
        self.tiempo_disparo -= 1
        if self.tiempo_disparo <= 0:
            self.tiempo_disparo = 75 if furioso else 110
            self.lanzar_roca(jugador, random.randint(-30, 30))
            if furioso:
                self.lanzar_roca(jugador, random.choice([-90, 90]))
        
        #Ataque 2: pisoton que lanza chispas
        if self.preparando > 0:
            self.preparando -= 1
            if self.preparando == 0:
                self.ondas.append({'x': self.x, 'velocidad': 10 if furioso else 7, 'golpeo': False})
                #Cuando hace el pisoton se abre la armadura
                self.abierto = 120
                self.tiempo_pisoton = 200 if furioso else 280
        else:
            self.tiempo_pisoton -= 1
            if self.tiempo_pisoton <= 0:
                self.preparando = 40
        
        if self.abierto > 0:
            self.abierto -= 1
    
    def lanzar_roca(self, jugador, desvio):
        #Origen de la roca caida
        origen_x = self.x + 10
        origen_y = self.y + 60
        objetivo = jugador.x + jugador.ancho / 2 + desvio
        tiempo = 70
        radio = 16
        vx = (objetivo - origen_x) / tiempo
        vy = (self.suelo_y - radio - origen_y - 0.5 * 0.35 * tiempo * tiempo) / tiempo
        self.proyectiles.append({'x': origen_x, 'y': origen_y, 'vx': vx, 'vy': vy, 'radio': radio, 'objetivo': objetivo})
        
    def recibir_balas(self, balas):
        #Cuando se abre la armadura se le hace daño al jefe
        if self.abierto > 0:
            return super().recibir_balas(balas)
        
        #Cuando la armadura esta cerrada las balas rebotan
        for bala in balas[:]:
            bala_rect = pygame.Rect(bala['x'], bala['y'], bala['ancho'], bala['alto'])
            if self.rect.colliderect(bala_rect):
                balas.remove(bala)
                self.chispas.append({'x': bala['x'], 'y': bala['y'], 'tiempo': 10})
        return 0
    
    def actualizar_proyectiles(self, jugador):
        #Las rocas cuando caen desaparecen
        for p in self.proyectiles[:]:
            p['vy'] += 0.35
            if p['y'] + p['vy'] >= self.suelo_y - p['radio']:
                self.proyectiles.remove(p)
        super().actualizar_proyectiles(jugador)
        
        #Ondas que chocan contra el personaje principal hay que evitarlas
        for onda in self.ondas[:]:
            onda['x'] -= onda['velocidad']
            if onda['x'] < -40:
                self.ondas.remove(onda)
                continue
            rect_onda = pygame.Rect(onda['x'] - 18, self.suelo_y - 45, 36, 45)
            
            if not onda['golpeo'] and rect_onda.colliderect(jugador.rect):
                jugador.recibir_daño()
                onda['golpeo'] = True
                
        #Chispas
        for chispa in self.chispas[:]:
            chispa['tiempo'] -= 1
            if chispa['tiempo'] <= 0:
                self.chispas.remove(chispa)
                
    def morir(self):
        self.ondas = []
        self.chispas = []
        super().morir()
        
    def dibujar(self, pantalla):
        for p in self.proyectiles:
            centro = (int(p['x']), int(p['y']))
            radio = p['radio']
            pygame.draw.ellipse(pantalla, (70,60,50), (int(p['objetivo']) - 16, self.suelo_y - 4, 32, 8))
            pygame.draw.circle(pantalla, (60,60,65), centro, radio + 2)
            pygame.draw.circle(pantalla, (140,140,145), centro, radio)
            pygame.draw.circle(pantalla, (175,175,180), (centro[0] - 5, centro[1] - 5), 5)
         
        #Ondas de choque
        for onda in self.ondas:
            x = int(onda['x'])
            suelo = self.suelo_y
            puntos = [(x - 18, suelo), (x - 8, suelo - 45), (x + 4, suelo -30), (x + 12, suelo - 45), (x + 18, suelo)]
            pygame.draw.polygon(pantalla, (170,150,110), puntos)
            pygame.draw.polygon(pantalla, (100,85,60), puntos, 3)
         
        if self.estado == 'muriendo':
            self.dibujar_muerte(pantalla)
            return
        
        self.dibujar_cuerpo(pantalla)
        self.dibujar_barra_vida(pantalla)
        self.dibujar_aviso(pantalla)
         
        #Chispas
        for chispa in self.chispas:
            pygame.draw.circle(pantalla, (255,255,150), (int(chispa['x']),int(chispa['y'])), 3 + chispa['tiempo'] // 3)
            
    def dibujar_cuerpo(self, pantalla, desplazamiento_x = 0, desplazamiento_y = 0):
        x = int(self.x) + desplazamiento_x
        y = int(self.y) + desplazamiento_y
        centro = x + self.ancho // 2
        base = y + self.alto
        
        #Colores del jefe
        roca = (150,110,100) if self.furioso() else (125,125,135)
        if self.destello > 0 and self.destello % 4 < 2:
            roca = (255,255,255)
        roca_oscura = (max(0, roca[0] - 50), max(0, roca[1] - 50), max(0, roca[2] - 50))
        roca_clara = (min(255, roca[0] + 30), min(255, roca[1] + 30), min(255, roca[2] + 30))
        
        #Cuando prepara el pisoton el jefe levanta los brazos y empieza a temblar
        levantar = -40 if self.preparando > 0 else 0
        temblor = random.randint(-2, 2) if self.preparando > 0 else 0
        centro += temblor
        
        #Piernas
        for pierna_x in (centro - 42, centro + 12):
            pygame.draw.rect(pantalla, roca, (pierna_x, base - 60, 30, 60))
            pygame.draw.rect(pantalla, roca_oscura, (pierna_x, base - 60, 30, 60), 3)
            
        #Brazos
        for brazo_x in (centro - 88, centro + 58):
            pygame.draw.rect(pantalla, roca, (brazo_x, y + 65 + levantar, 30, 85))
            pygame.draw.rect(pantalla, roca_oscura, (brazo_x, y + 65 + levantar, 30, 85), 3)
            
        #Torso
        torso = pygame.Rect(centro - 55, y + 60, 110, 100)
        pygame.draw.rect(pantalla, roca, torso)
        pygame.draw.rect(pantalla, roca_oscura, torso, 4)
        pygame.draw.line(pantalla, roca_oscura, (centro - 40, y + 70), (centro - 28, y + 95), 3)
        pygame.draw.line(pantalla, roca_oscura, (centro + 38, y + 140), (centro + 25, y + 118), 3)
        
        #Cabeza
        cabeza = pygame.Rect(centro - 30, y, 60, 55)
        pygame.draw.rect(pantalla, roca_clara, cabeza)
        pygame.draw.rect(pantalla, roca_oscura, cabeza, 4)
        ojo = (255,60,40) if self.furioso() else (255,210,0)
        pygame.draw.rect(pantalla, ojo, (centro - 20, y + 20, 14, 8))
        pygame.draw.rect(pantalla, ojo, (centro + 6, y + 20, 14, 8))
        pygame.draw.line(pantalla, (0,0,0), (centro - 12, y + 40), (centro + 12, y + 40), 4)
        
        #Pecho: tapado o brillando cuandos e abre
        if self.abierto > 0:
            pulso = int(math.sin(self.animacion * 0.4) * 3)
            pygame.draw.circle(pantalla, (255,140,0), (centro, y + 110), 20 + pulso)
            pygame.draw.circle(pantalla, (255,230,80), (centro, y + 110), 13 + pulso)
            pygame.draw.circle(pantalla, (255,255,255), (centro, y + 110), 6)
        else:
            pygame.draw.circle(pantalla, (50,50,55), (centro, y + 110), 20)
            pygame.draw.rect(pantalla, roca_clara, (centro - 24, y + 90, 48, 40))
            pygame.draw.rect(pantalla, roca_oscura, (centro - 24, y + 90, 48, 40), 3)
            pygame.draw.line(pantalla, roca_oscura, (centro, y + 90), (centro, y + 130), 3)
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        