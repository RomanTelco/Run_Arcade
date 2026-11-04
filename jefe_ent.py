# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 12:02:19 2026

@author: Neo-PC
"""

import pygame
import random
import math
from config import*
from jefe import Jefe

#Jefe del nivel 2
class JefeEnt(Jefe):
    def __init__(self, config_jefe, suelo_y):
        super().__init__(config_jefe, suelo_y)
        
        #Raices que salen del suelo
        self.raices = []
        self.tiempo_raiz = 200
        
    #Movimiento del Ent
    def mover(self, jugador):
        pass
    
    #Ataque del Ent
    def disparar(self, jugador):
        furioso = self.furioso()
        
        #Ataque 1: lluvia de bellotas
        self.tiempo_disparo -= 1
        if self.tiempo_disparo <= 0:
            self.tiempo_disparo = 65 if furioso else 100
            cantidad = 5 if furioso else 3
            for i in range(cantidad):
                if i == 0:
                    x= jugador.x + random.randint(-60, 60)
                else:
                    x= random.randint(60, int(self.x) - 30)
                x = max(30, min(int(self.x)-30, x))
                self.proyectiles.append({'x': x, 'y': -20, 'vx': 0, 'vy': random.uniform(6,9), 'radio': 11})
                
        #Ataque 2: raices que atacan al personaje principal
        self.tiempo_raiz -= 1
        if self.tiempo_raiz <= 0:
            self.tiempo_raiz = 170 if furioso else 250
            centro_jugador = jugador.x + jugador.ancho / 2
            self.raices.append({'x': centro_jugador, 'tiempo': 0, 'golpeo': False})
            if furioso:
                lado = random.choice([-110, 110])
                self.raices.append({'x': centro_jugador + lado, 'tiempo': 0, 'golpeo': False})
                
    def colisionar_jugador(self, jugador):
        #El ataque al Ent solo se puede mediante disparo
        if not self.rect.colliderect(jugador.rect):
            return 0
        
        #Si el jugador se come una moneda de invencibilidad puede hacer daño al jugador
        if jugador.invencible_por_moneda:
            if self.inmune == 0:
                self.recibir_daño(1,20)
                return 25
            return 0
        
        if jugador.invencible:
            return 0
        
        jugador.recibir_daño()
        return 0
    
    def actualizar_proyectiles(self,jugador):
        for p in self.proyectiles[:]:
            if p['y'] >= self.suelo_y - p['radio']:
                self.proyectiles.remove(p)
        super().actualizar_proyectiles(jugador)
        
        for r in self.raices[:]:
            r['tiempo'] += 1
            if 50 <= r['tiempo'] < 80:
                crecimiento = min(1, (r['tiempo'] - 50) /  6)
                alto = int(115 * crecimiento)
                rect_raiz = pygame.Rect(r['x'] - 20, self.suelo_y - alto, 40, alto)
                if not r['golpeo'] and rect_raiz.colliderect(jugador.rect):
                    jugador.recibir_daño()
                    r['golpeo'] = True
            elif r['tiempo'] >= 80:
                self.raices.remove(r)
    
    def morir(self):
        self.raices = []
        super().morir()
    
    def dibujar(self, pantalla):
        for p in self.proyectiles:
            centro = (int(p['x']), int(p['y']))
            radio = p['radio']
            pygame.draw.ellipse(pantalla, (70,55,35), (centro[0]- radio, self.suelo_y - 4, radio * 2, 8))
            pygame.draw.circle(pantalla, (60,35,10), centro, radio + 2)
            pygame.draw.circle(pantalla, (150,95,40), centro, radio)
            pygame.draw.circle(pantalla, (90,60,25), (centro[0], centro[1] - 5), radio - 3)
            
        if self.estado == 'muriendo':
            self.dibujar_muerte(pantalla)
            return
        
        self.dibujar_raices(pantalla)
        self.dibujar_cuerpo(pantalla)
        self.dibujar_barra_vida(pantalla)
        self.dibujar_aviso(pantalla)
        
    def dibujar_raices(self, pantalla):
        for r in self.raices:
            x= int(r['x'])
            suelo = self.suelo_y
            
            if r['tiempo'] < 50:
                color = (180, 60, 30) if (r['tiempo'] // 5) % 2 == 0 else (120,40,20)
                pygame.draw.ellipse(pantalla, color, (x - 24, suelo - 6, 48, 12))
                pygame.draw.line(pantalla, (60,20,10), (x - 18, suelo), (x - 6, suelo + 6), 3)
                pygame.draw.line(pantalla, (60,20,10), (x + 18, suelo), (x + 6, suelo + 6), 3)
            else:
                #La raiz sael del suelo
                f = min(1, (r['tiempo'] - 50) / 6)
                puntos = [(x - 22, suelo), (x -10, suelo - 60 * f), (x - 14, suelo - 90 * f), (x + 2, suelo - 115 * f), (x + 12, suelo - 80 * f), (x + 8, suelo - 55 * f), (x + 22, suelo)]
                pygame.draw.polygon(pantalla, (95, 60, 25), puntos)
                pygame.draw.polygon(pantalla, (50,30,10), puntos, 3)
                
    def dibujar_cuerpo(self, pantalla, desplazamiento_x = 0, desplazamiento_y = 0):
        x = int(self.x) + desplazamiento_x
        y = int(self.y) + desplazamiento_y
        centro = x + self.ancho // 2
        base = y + self.alto
        
        #Colores
        hojas = (200,110,40) if self.furioso() else (50, 140,60)
        tronco = (110,70,30)
        if self.destello > 0 and self.destello % 4 < 2:
            hojas = (255,255,255)
            tronco = (255,255,255)
        hojas_oscuras = (max(0,hojas[0] - 40), max(0, hojas[1] - 40), max(0, hojas[2] - 40))
        
        #Raices de la base
        pygame.draw.ellipse(pantalla, (70,45,20), (centro - 65, base - 28, 130, 32))
        
        #Brazos
        balanceo = int(math.sin(self.animacion * 0.06) * 10)
        pygame.draw.line(pantalla, tronco, (centro - 30, y + 125), (centro - 85, y + 100 + balanceo), 14)
        pygame.draw.line(pantalla, tronco, (centro + 30, y + 125), (centro + 85, y + 100 - balanceo), 14)
        
        #Tronco
        puntos_tronco = [(centro - 32, y + 85), (centro + 32, y + 85), (centro + 45, base - 10), (centro - 45, base - 10)]
        pygame.draw.polygon(pantalla, tronco, puntos_tronco)
        pygame.draw.polygon(pantalla, (60,35,10), puntos_tronco, 3)
        for i in range(4):
            pygame.draw.line(pantalla, (80,50,20), (centro - 21 + i * 14, y + 105), (centro - 25 + i * 14, base - 40),2)
            
        #Copa del arbol
        for cx, cy, radio in [(centro, y + 55, 62), (centro - 48, y + 85, 45), (centro + 48, y + 85, 45), (centro, y + 25, 42)]:
            pygame.draw.circle(pantalla, hojas, (cx,cy), radio)
            pygame.draw.circle(pantalla, hojas_oscuras, (cx,cy), radio, 3)
            
        #Cara enfadada
        ojo = (255,60,40) if self.furioso() else (255,230,80)
        for ojo_x in (centro - 15, centro + 15):
            pygame.draw.circle(pantalla, ojo, (ojo_x, y + 140), 8)
            pygame.draw.circle(pantalla, (0,0,0), (ojo_x - 2, y + 140), 3)
        pygame.draw.line(pantalla, (0,0,0), (centro - 25, y + 126), (centro - 8, y + 133), 4)
        pygame.draw.line(pantalla, (0,0,0), (centro + 25, y + 126), (centro + 8, y + 133), 4)
        pygame.draw.ellipse(pantalla, (30,10,0), (centro - 18, y + 158, 36, 26))


        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
                    
    