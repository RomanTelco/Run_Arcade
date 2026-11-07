# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 13:33:36 2026

@author: Neo-PC
"""

#Jefe del nivel 6
import pygame
import random
import math
from config import *
from jefe import Jefe


class JefeCaballero(Jefe):
    def __init__(self, config_jefe, suelo_y):
        super().__init__(config_jefe, suelo_y)
        
        #Area de movimiento
        self.limite_izquierdo = 250
        
        #Fases
        self.fase = 'caminando'
        self.tiempo_fase = 0
        self.tiempo_embestida = 250
        
        #Sombras
        self.sombras = []
        self.tiempo_sombras = 300
        
    def rect_sombra(self, sombra):
        return pygame.Rect(sombra['x'], self.suelo_y - self.alto, self.ancho, self.alto)
    
    def mover(self, jugador):
        furioso = self.furioso()
        
        #1º Fase
        if self.fase == 'caminando':
            velocidad = 1.8 if furioso else 1.2
            objetivo = jugador.x + jugador.ancho / 2 - self.ancho / 2
            if objetivo < self.x:
                self.x -= velocidad
            else:
                self.x += velocidad
            self.x = max(self.limite_izquierdo, min(self.limite_derecho, self.x))
            
            self.tiempo_embestida -= 1
            if self.tiempo_embestida <= 0:
                self.fase = 'preparando'
                self.tiempo_fase = 40
                
        #2º Fase
        elif self.fase == 'preparando':
            self.tiempo_fase -= 1
            if self.tiempo_fase <= 0:
                self.fase = 'embistiendo'
        
        #3º Fase
        elif self.fase == 'embistiendo':
            self.x -= 20 if furioso else 16
            if self.x <= self.limite_izquierdo:
                self.x = self.limite_izquierdo
                self.fase = 'volviendo'
        
        #4º Fase
        elif self.fase == 'volviendo':
            self.x += 6
            if self.x >= self.limite_derecho:
                self.x = self.limite_derecho
                self.fase = 'caminando'
                self.tiempo_embestida = 150 if furioso else 220
    
    def disparar(self, jugador):
        furioso = self.furioso()
        
        #Ataque 1
        if self.fase == 'caminando':
            self.tiempo_disparo -= 1
            if self.tiempo_disparo <= 0:
                self.tiempo_disparo = 75 if furioso else 110
                velocidad = -11 if furioso else -9
                self.proyectiles.append({'x': self.x, 'y': self.suelo_y - 22, 'vx': velocidad, 'vy': 0, 'radio': 8, 'tipo': 'daga'})
                self.proyectiles.append({'x': self.x, 'y': self.suelo_y - 105, 'vx': velocidad, 'vy': 0, 'radio': 8, 'tipo': 'daga'})
                
        #Ataque 2
        self.tiempo_sombras -= 1
        if self.tiempo_sombras <= 0:
            self.tiempo_sombras = 300 if furioso else 420
            self.invocar_sombras()
                
        for sombra in self.sombras[:]:
            sombra['tiempo'] += 1
            if sombra['tiempo'] > 30:
                sombra['disparo'] -= 1
                if sombra['disparo'] <= 0:
                    sombra['disparo'] = 130
                    self.proyectiles.append({'x': sombra['x'], 'y': self.suelo_y - 9, 'vx': -9, 'vy': 0, 'radio': 8, 'tipo': 'daga'})
            if sombra['tiempo'] > 420:
                self.sombras.remove(sombra)
    
    def invocar_sombras(self):
        self.sombras = []
        posiciones = []
        for intento in range(50):
            if len(posiciones) >= 2:
                break
            x= random.randint(self.limite_izquierdo, int(self.limite_derecho))
            if abs(x - self.x) > 120 and all(abs(x - p) > 120 for p in posiciones):
                posiciones.append(x)
        for x in posiciones:
            self.sombras.append({'x': x, 'tiempo': 0, 'disparo': 60})
    
    def recibir_balas(self, balas):
        #Las balas destruyen sombras
        puntos = 0
        for bala in balas[:]:
            bala_rect = pygame.Rect(bala['x'], bala['y'], bala['ancho'], bala['alto'])
            for sombra in self.sombras[:]:
                if sombra['tiempo'] > 30 and self.rect_sombra(sombra).colliderect(bala_rect):
                    self.sombras.remove(sombra)
                    puntos += 50
                    break
        return puntos + super().recibir_balas(balas)
    
    def actualizar_proyectiles(self, jugador):
        super().actualizar_proyectiles(jugador)
        
        #Al tocar la sombra hace daño
        for sombra in self.sombras[:]:
            if sombra['tiempo'] <= 30:
                continue
            rect = self.rect_sombra(sombra)
            if not rect.colliderect(jugador.rect):
                continue
            if jugador.invencible_por_moneda:
                self.sombras.remove(sombra)
                jugador.puntuacion += 50
            elif jugador.invencible:
                continue
            elif jugador.velocidad_y > 0 and jugador.pies_rect.colliderect(pygame.Rect(rect.x, rect.y, rect.w, 25)):
                jugador.velocidad_y = -12
                self.sombras.remove(sombra)
                jugador.puntuacion += 50
            else:
                jugador.recibir_daño()
                
    def morir(self):
        self.sombras = []
        super().morir()
    
    def dibujar(self, pantalla):
        #Dagas
        for p in self.proyectiles:
            centro = (int(p['x']), int(p['y']))
            hoja = [(centro[0] - 18, centro[1]), (centro[0] + 8, centro[1] - 5), (centro[0] + 8, centro[1] + 5)]
            pygame.draw.polygon(pantalla, (210,210,230), hoja)
            pygame.draw.polygon(pantalla, (90,90,110), hoja, 2)
            pygame.draw.line(pantalla, (120,30,60), (centro[0] + 8, centro[1]), (centro[0] + 20, centro[1]), 4)
            
        if self.estado == 'muriendo':
            self.dibujar_muerte(pantalla)
            return
        #Aviso de la embestida
        if self.fase == 'preparando':
            if(self.tiempo_fase // 4) % 2 == 0:
                pygame.draw.line(pantalla, (255,60,60), (int(self.x), self.suelo_y - 4), (self.limite_izquierdo, self.suelo_y - 4), 4)
        
        
        #Sombras
        for sombra in self.sombras:
            if sombra['tiempo'] <= 30 and (sombra['tiempo'] // 3) % 2 == 1:
                continue
            self.dibujar_caballero(pantalla, int(sombra['x']), self.suelo_y - self.alto, True, 'caminando')
            
        self.dibujar_cuerpo(pantalla)
        self.dibujar_barra_vida(pantalla)
        self.dibujar_aviso(pantalla)
        
    def dibujar_cuerpo(self, pantalla, desplazamiento_x = 0, desplazamiento_y = 0):
        self.dibujar_caballero(pantalla, int(self.x) + desplazamiento_x, int(self.y) + desplazamiento_y, False, self.fase)
        
    def dibujar_caballero(self, pantalla, x, y, clon, fase):
        centro = x + self.ancho // 2
        furioso = self.furioso()
        
        if clon:
            armadura = (35,35,55)
            oscuro = (20,20,35)
            ojo = (190,90,255)
            capa = (60,15,45)
            plumas = (90,30,70)
            espada = (120,120,150)
        else:
            armadura = (95,50,70) if furioso else (65,65,90)
            oscuro = (35,25,45)
            ojo = (255,40,40)
            capa = (110,20,45)
            plumas = (170,20,40)
            espada = (205,205,225)
            if self.destello > 0 and self.destello % 4 < 2:
                armadura = (255,255,255)
        
        if furioso and not clon:
            pygame.draw.ellipse(pantalla, (200,40,60), (centro - 48, y - 8, 96, self.alto + 14), 2)
            
        #Capa
        forma_capa = [(centro + 10, y + 42), (centro + 40, y + 50), (centro + 52, y + self.alto - 5), (centro + 20, y + self.alto - 12)]
        pygame.draw.polygon(pantalla, capa, forma_capa)
        
        #Piernas
        paso = int(math.sin(self.animacion * 0.2) * 5) if fase in('caminando', 'volviendo', 'embistiendo') else 0
        for pierna_x, desvio in ((centro - 22, paso), (centro + 4, -paso)):
            pygame.draw.rect(pantalla, armadura, (pierna_x + desvio, y + 85, 18, 35))
            pygame.draw.rect(pantalla, oscuro, (pierna_x + desvio, y + 85, 18, 35), 3)
        
        #Torso y hombros
        pygame.draw.rect(pantalla, armadura, (centro - 28, y + 40, 56, 50))
        pygame.draw.rect(pantalla, oscuro, (centro - 28, y + 40, 56, 50), 3)
        pygame.draw.line(pantalla, oscuro, (centro - 28, y + 75), (centro + 28, y + 75), 4)
        for hombro_x in (centro - 30, centro + 30):
            pygame.draw.circle(pantalla, armadura, (hombro_x, y + 45), 12)
            pygame.draw.circle(pantalla, oscuro, (hombro_x, y + 45), 12, 3)
        
        #Casco
        pygame.draw.ellipse(pantalla, armadura, (centro - 20, y, 40, 46))
        pygame.draw.ellipse(pantalla, oscuro, (centro - 20, y, 40, 46), 3)
        pygame.draw.rect(pantalla, ojo, (centro - 17, y + 20, 26, 7))
        penacho = [(centro, y + 2), (centro + 22, y - 14), (centro + 30, y + 10), (centro + 8, y + 8)]
        pygame.draw.polygon(pantalla, plumas, penacho)
        
        #Espada
        mano = (centro - 30, y + 70)
        if fase == 'preparando':
            punta = (centro - 42, y - 35)
            pygame.draw.circle(pantalla, (255,80,60), punta, 9)
        elif fase == 'embistiendo':
            punta = (centro - 100, y + 66)
        else:
            punta = (centro - 70, y + 50 + paso)
        pygame.draw.line(pantalla, espada, mano, punta, 6)
        pygame.draw.line(pantalla, (140,110,40), (mano[0] - 4, mano[1] -8), (mano[0] - 4, mano[1] + 8), 4)
        
            
        
        
                            
        
        
           
        