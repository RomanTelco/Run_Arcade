# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 11:48:56 2026

@author: Neo-PC
"""

#Jefe final del nivel 4
import pygame
import random
import math
from config import *
from jefe import Jefe

class JefeDragon(Jefe):
    def __init__(self, config_jefe, suelo_y):
        super().__init__(config_jefe, suelo_y)
        
        #Zona de vuelo del dragon
        self.limite_izquierdo = 250
        self.altura_vuelo = 150
        self.y = self.altura_vuelo
        
        #Fases del vuelo
        self.fase = 'volando'
        self.tiempo_fase = 0
        self.tiempo_embestida = 240
        self.objetivo_x = 0
        
        #Meteoritos
        self.tiempo_meteoro = 90
    
    def mover(self, jugador):
        furioso = self.furioso()
        
        if self.fase == 'volando':
            self.x += self.direccion * (2.2 if furioso else 1.5)
            if self.x <= self.limite_izquierdo:
                self.direccion = 1
            elif self.x >= self.limite_derecho:
                self.direccion = -1
            altura = self.altura_vuelo + math.sin(self.animacion * 0.05) * 25
            self.y += (altura - self.y) * 0.1
            
            #Se avisa de la embestida del dragon
            self.tiempo_embestida -= 1
            if self.tiempo_embestida <= 0:
                self.fase = 'avisando'
                self.tiempo_fase = 50
                self.objetivo_x = max(0, min(Ventana_ancho - self.ancho - 10, jugador.x + jugador.ancho / 2 - self.ancho / 2))
        elif self.fase == 'avisando':
            self.tiempo_fase -= 1
            self.x += (self.objetivo_x - self.x) * 0.1
            self.y += (self.altura_vuelo - 30 - self.y) * 0.1
            if self.tiempo_fase <= 0:
                    self.fase = 'embistiendo'
        elif self.fase == 'embistiendo':
            self.y += 22
            if self.y >= self.suelo_y - self.alto:
                self.fase = 'aturdido'
                self.tiempo_fase = 70 if furioso else 100
        elif self.fase == 'aturdido':
            self.tiempo_fase -= 1
            if self.tiempo_fase <= 0:
                self.fase = 'subiendo'
        elif self.fase == 'subiendo':
            self.y -= 6
            if self.y <= self.altura_vuelo:
                self.y = self.altura_vuelo
                self.fase = 'volando'
                self.tiempo_embestida = 200 if furioso else 280
        self.x = max(0, min(Ventana_ancho - self.ancho, self.x))
    def disparar(self, jugador):
        furioso = self.furioso()
        
        #Ataque 1: bolas de fuego
        if self.fase == 'volando':
            self.tiempo_disparo -= 1
            if self.tiempo_disparo <= 0:
                self.tiempo_disparo = 80 if furioso else 120
                self.lanzar_bolas(jugador)
                
        #Ataque 2: lluvia de meteoritos
        if furioso:
            self.tiempo_meteoro -= 1
            if self.tiempo_meteoro <= 0:
                self.tiempo_meteoro = 90
                for i in range(2):
                    x = random.randint(60, Ventana_ancho - 60)
                    self.proyectiles.append({'x': x, 'y': -20, 'vx': 0, 'vy': random.uniform(7, 10), 'radio': 14, 'tipo': 'meteoro'})
                    
    def lanzar_bolas(self, jugador):
        origen_x = self.x + 5
        origen_y = self.y + self.alto * 0.55
        objetivo_x = jugador.x + jugador.ancho / 2
        objetivo_y = jugador.y + jugador.alto / 2
        angulo_base = math.atan2(objetivo_y - origen_y, objetivo_x - origen_x)
        
        if self.furioso():
            angulos = [angulo_base - 0.35, angulo_base - 0.17, angulo_base, angulo_base + 0.17, angulo_base + 0.35]
        else:
            angulos = [angulo_base - 0.25, angulo_base, angulo_base + 0.25]
        
        for angulo in angulos:
            self.proyectiles.append({'x': origen_x, 'y': origen_y, 'vx': math.cos(angulo) * 7, 'vy': math.sin(angulo) * 7, 'radio' : 11, 'tipo': 'bola'})
            
    def recibir_balas(self, balas):
        #Las balas hacen el doble de daño cuando el dragon esta aturdido
        puntos = 0
        daño = 2 if self.fase == 'aturdido' else 1
        for bala in balas[:]:
            bala_rect = pygame.Rect(bala['x'], bala['y'], bala['ancho'], bala['alto'])
            if self.rect.colliderect(bala_rect):
                balas.remove(bala)
                self.recibir_daño(daño)
                puntos += 25
        return puntos
    
    def actualizar_proyectiles(self, jugador):
        #La municion del dragon desaparece cuando cae al suelo
        for p in self.proyectiles[:]:
            if p['y'] >= self.suelo_y - p['radio']:
                self.proyectiles.remove(p)
        super().actualizar_proyectiles(jugador)
    
    def dibujar(self, pantalla):
        for p in self.proyectiles:
            centro = (int(p['x']), int(p['y']))
            radio = p['radio']
            if p['tipo'] == 'meteoro':
                pygame.draw.ellipse(pantalla, (60,40,30), (centro[0] - radio, self.suelo_y - 4, radio * 2, 8))
                pygame.draw.circle(pantalla, (255,100,0), centro, radio + 4)
                pygame.draw.circle(pantalla, (70,45,35), centro, radio)
                pygame.draw.circle(pantalla, (255,160,40), (centro[0] - 4, centro[1] - 4), 4)
            else:
                pygame.draw.circle(pantalla, (255,80,0), centro, radio + 3)
                pygame.draw.circle(pantalla, (255,200,0), centro, radio)
                pygame.draw.circle(pantalla, (255,255,200), centro, radio // 2)
            
        if self.estado == 'muriendo':
            self.dibujar_muerte(pantalla)
            return
            
        if self.fase == 'avisando':
            centro_x = int(self.objetivo_x + self.ancho / 2)
            if (self.tiempo_fase // 4) % 2 == 0:
                pygame.draw.line(pantalla, (255,60,0), (centro_x, int(self.y + self.alto)), (centro_x, self.suelo_y), 4)
            pygame.draw.ellipse(pantalla, (200,40,0), (centro_x - 40, self.suelo_y - 6, 80, 12))
                
        self.dibujar_cuerpo(pantalla)
        self.dibujar_barra_vida(pantalla)
        self.dibujar_aviso(pantalla)
            
    def dibujar_cuerpo(self, pantalla, desplazamiento_x = 0, desplazamiento_y = 0):
        x = int(self.x) + desplazamiento_x
        y = int(self.y) + desplazamiento_y
        centro = x + self.ancho // 2
        
        #Colores
        cuerpo = (120,25,20) if self.furioso() else (190,60,30)
        ala = (80,15,15) if self.furioso() else(140,35,25)
        barriga = (230,150,60)
        if self.destello > 0 and self.destello % 4 < 2:
            cuerpo = (255,255,255)
            ala = (255,255,255)
            barriga = (255,255,255)
        oscuro = (max(0,cuerpo[0] - 60), max(0,cuerpo[1] - 30), max(0,cuerpo[2] - 30))
        
        #Ala
        aleteo = int(math.sin(self.animacion * 0.2) * 25)
        puntos_ala = [(centro, y + 40), (centro + 10, y - 35 + aleteo), (centro + 40, y - 10 + int(aleteo * 0.8)), (centro + 60, y - 40 + aleteo), (centro + 75, y + 40)]
        pygame.draw.polygon(pantalla, ala, puntos_ala)
        pygame.draw.polygon(pantalla, oscuro, puntos_ala, 3)
        
        #Cola
        cola = [(x + 105, y + 60), (x + 148, y + 50), (x + 132, y + 70), (x + 148, y + 85), (x + 105, y + 85)]
        pygame.draw.polygon(pantalla, cuerpo, cola)
        pygame.draw.polygon(pantalla, oscuro, cola, 3)
        
        #Patas
        for pata_x in (x + 50, x + 95):
            pygame.draw.rect(pantalla, oscuro, (pata_x, y + 95, 12, 20))
            pygame.draw.polygon(pantalla, (240,230,200), [(pata_x - 2, y + 115), (pata_x + 6, y + 108), (pata_x + 14, y + 115)])
            
        #Cuerpo y barriga
        pygame.draw.ellipse(pantalla, cuerpo, (x + 25, y + 35, 105, 65))
        pygame.draw.ellipse(pantalla, oscuro, (x + 25, y + 35, 105, 65), 3)
        pygame.draw.ellipse(pantalla, barriga, (x + 40, y + 62, 80, 30))
        
        if self.furioso():
            for i in range(3):
                pygame.draw.line(pantalla, (255,140,0), (x + 55 + i * 25, y + 58), (x + 65 + i * 25, y + 58), 3)
                
        #Cabeza con cuernos
        pygame.draw.ellipse(pantalla, cuerpo, (x, y + 30, 60, 45))
        pygame.draw.ellipse(pantalla, oscuro, (x, y + 30, 60, 45), 3)
        pygame.draw.polygon(pantalla, (240, 230, 200), [(x + 30, y + 32), (x + 38, y + 8), (x + 44, y + 34)])
        pygame.draw.polygon(pantalla, (240,230,200), [(x + 18, y + 33), (x + 20, y + 12), (x + 28, y + 34)])
        
        #Ojo enfadado
        pygame.draw.circle(pantalla, (255,230,0), (x + 32, y + 46), 7)
        pygame.draw.circle(pantalla, (0,0,0), (x + 30, y + 46), 3)
        pygame.draw.line(pantalla, (0,0,0), (x + 24, y + 38), (x + 42, y + 43), 4)
        
        #Boca
        pygame.draw.line(pantalla, (40,0,0), (x + 2, y + 62), (x + 30, y + 64), 3)
        if self.fase == 'volando' and self.tiempo_disparo <= 20:
            pygame.draw.circle(pantalla, (255,140,0), (x + 4, y + 62), 12)
            pygame.draw.circle(pantalla, (255,230,80), (x + 4, y + 62), 6)
            
        #Estrellitas cuando esta aturdido
        if self.fase == 'aturdido':
            for k in range(3):
                angulo = self.animacion * 0.15 + k * 2.1
                pygame.draw.circle(pantalla, (255,255,0), (int(x + 30 + math.cos(angulo) * 22), int(y - 8 + math.sin(angulo) * 8)), 5)
                
        