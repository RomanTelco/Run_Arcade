# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 14:39:33 2026

@author: Neo-PC
"""


#Jefe final nivel 5
import pygame 
import random
import math
from config import *
from jefe import Jefe

class JefeReina(Jefe):
    def __init__(self, config_jefe, suelo_y):
        super().__init__(config_jefe, suelo_y)
        
        #Sitios a los que se teletrasporta la jefa del nivel 5
        suelo = suelo_y - self.alto
        self.posiciones = [(1050, suelo), (1000, 150), (650, 260), (550,130), (400, suelo), (850, 200)]
        self.pos_x = None
        self.pos_y = None
        
        #Fases de los ataques de la jefa
        self.fase = 'flotando'
        self.tiempo_fase = 0
        self.tiempo_tp = 200
        self.contador_tp = 0
        
        #Carambanos de la jefa
        self.carambanos = []
        self.tiempo_ventisca = 150
        self.giro = 0
        
    def intangible(self):
        return self.fase != 'flotando'
    
    def mover(self, jugador):
        furioso = self.furioso()
        
        #Primera vez
        if self.pos_x is None:
            self.pos_x = self.x
            self.pos_y = self.y
        
        if self.fase == 'flotando':
            self.x = self.pos_x
            self.y = self.pos_y - 6 - math.sin(self.animacion * 0.08) * 6
            self.tiempo_tp -= 1
            if self.tiempo_tp <= 0:
                self.fase = 'desvaneciendo'
                self.tiempo_fase = 20
                
        elif self.fase == 'desvaneciendo':
            self.tiempo_fase -= 1
            if self.tiempo_fase <= 0:
                #Aparece en sitio random
                opciones = [p for p in self.posiciones if abs(p[0] - self.pos_x) > 50 or abs(p[1] - self.pos_y)> 50]
                self.pos_x, self.pos_y = random.choice(opciones)
                self.x = self.pos_x
                self.y = self.pos_y
                self.contador_tp += 1
                self.fase = 'reapareciendo'
                self.tiempo_fase = 20
        
        elif self.fase == 'reapareciendo':
            self.tiempo_fase -= 1
            if self.tiempo_fase <= 0:
                if self.contador_tp % 3 == 0:
                    self.fase = 'ventisca'
                    self.tiempo_fase = 180
                    self.tiempo_ventisca = 60
                else:
                    self.fase = 'flotando'
                    self.tiempo_tp = 140 if furioso else 200
                    self.tiempo_disparo = min(self.tiempo_disparo, 25)
        
        elif self.fase == 'ventisca':
            self.x = self.pos_x
            self.y = self.pos_y - 6 - math.sin(self.animacion * 0.08) * 6
            self.tiempo_fase -= 1
            if self.tiempo_fase <= 0:
                self.fase = 'flotando'
                self.tiempo_tp = 140 if furioso else 200
        
    
    def disparar(self, jugador):
        furioso = self.furioso()
        
        #Ataque 1: lanzamiento de esqurlas
        if self.fase == 'flotando':
            self.tiempo_disparo -= 1
            if self.tiempo_disparo <= 0:
                self.tiempo_disparo = 75 if furioso else 110
                self.lanzar_esquirlas()
        
        #Ataque 2: ventisca
        if self.fase == 'ventisca':
            self.tiempo_ventisca -= 1
            if self.tiempo_ventisca <= 0:
                self.tiempo_ventisca = 180 if furioso else 260
                self.lanzar_ventisca(jugador)
    
    def lanzar_esquirlas(self):
        cantidad = 12 if self.furioso() else 8
        centro_x = self.x + self.ancho / 2
        centro_y = self.y + self.alto * 0.4
        self.giro += 0.3
        for i in range(cantidad):
            angulo = self.giro + i * 2 * math.pi / cantidad
            self.proyectiles.append({'x': centro_x, 'y': centro_y, 'vx': math.cos(angulo) * 5, 'vy': math.sin(angulo) * 5, 'radio': 9, 'tipo': 'esquirla'})
    
    def lanzar_ventisca(self, jugador):
        cantidad = 7 if self.furioso() else 5
        columnas = list(range(60, Ventana_ancho - 60, 100))
        random.shuffle(columnas)
        elegidas = columnas[:cantidad]
        #Uno cae justo donde esta el jugador
        elegidas[0] = int(jugador.x + jugador.ancho / 2)
        for x in elegidas:
            self.carambanos.append({'x': x, 'y': -60, 'tiempo': 0, 'golpeo': False})
            
    def recibir_balas(self, balas):
        #Las balas atraviesan a la jefa
        if self.intangible():
            return 0
        return super().recibir_balas(balas)
    
    def colisionar_jugador(self, jugador):
        if self.intangible():
            return 0
        return super().colisionar_jugador(jugador)
    
    def actualizar_proyectiles(self, jugador):
        #La municion desaparece al llegar al suelo
        for p in self.proyectiles[:]:
            if p['y'] >= self.suelo_y - 5:
                self.proyectiles.remove(p)
        super().actualizar_proyectiles(jugador)
        
        #Fotogramas de aviso
        for c in self.carambanos[:]:
            c['tiempo'] += 1
            if c['tiempo'] > 45:
                c['y'] += 26
                rect_carambano = pygame.Rect(c['x'] - 10, c['y'], 20, 60)
                if not c['golpeo'] and rect_carambano.colliderect(jugador.rect):
                    jugador.recibir_daño()
                    c['golpeo'] = True
                if c['y'] + 60 >= self.suelo_y:
                    self.carambanos.remove(c)
    def morir(self):
        self.carambanos = []
        super().morir()
    
    def dibujar(self, pantalla):
        #Los carambanos y su aviso
        for c in self.carambanos:
            x = int(c['x'])
            if c['tiempo'] <= 45:
                if (c['tiempo'] // 4) % 2 == 0:
                    pygame.draw.line(pantalla, (150,220,255), (x,0), (x, self.suelo_y), 2)
                    pygame.draw.ellipse(pantalla, (120, 200, 255), (x - 14, self.suelo_y - 5, 28, 10))
                else:
                    y = int(c['y'])
                    puntos = [(x - 10, y), (x + 10, y), (x, y + 60)]
                    pygame.draw.polygon(pantalla, (170, 230, 255), puntos)
                    pygame.draw.polygon(pantalla, (90,170,220), puntos, 3)
                    
        #Esquirlas
        for p in self.proyectiles:
            centro = (int(p['x']), int(p['y']))
            radio = p['radio']
            pygame.draw.circle(pantalla, (90,170,230), centro, radio + 2)
            pygame.draw.circle(pantalla, (200,240,255), centro, radio)
            pygame.draw.circle(pantalla, (255,255,255), centro, radio // 2)
            
        if self.estado == 'mueriendo':
            self.dibujar_muerte(pantalla)
            return
        
        if self.fase == 'reapareciendo':
            centro = (int(self.x + self.ancho / 2), int(self.y + self.alto / 2))
            pygame.draw.circle(pantalla, (200,240,255), centro, (20- - self.tiempo_fase) * 5 + 5, 3)
           
        self.dibujar_cuerpo(pantalla)
        self.dibujar_barra_vida(pantalla)
        self.dibujar_aviso(pantalla)
            
    def dibujar_cuerpo(self, pantalla, desplazamiento_x = 0, desplazamiento_y = 0):
        #Parpadea mientras desaparece
        if self.estado == 'activo' and self.fase == 'desvaneciendo' and (self.tiempo_fase // 2) % 2 == 1:
            return
        
        x = int(self.x) + desplazamiento_x
        y = int(self.y) + desplazamiento_y
        centro = x + self.ancho // 2
        
        #Colores
        vestido = (160, 120, 230) if self.furioso() else (140,200,240)
        vestido_claro = (210,185,250) if self.furioso() else (200,235,255)
        piel = (235,245,255)
        ojo = (255,60,160) if self.furioso() else (0,200,255)
        if self.destello > 0 and self.destello % 4 < 2:
            vestido = (255,255,255)
            vestido_claro = (255,255,255)
        oscuro = (max(0, vestido[0] - 60), max(0, vestido[1] - 60), max(0, vestido[2] - 40))
        
        #Cuando lanza los ataques de esquirlas
        lanzado = self.fase == 'flotando' and self.tiempo_disparo <= 20
        if lanzado:
            pygame.draw.circle(pantalla, (200,240,255), (centro, y + 60), 55 + int(math.sin(self.animacion * 0.5) * 4), 3)
            
            #Copos que giran alrededor
            for k in range(4):
                angulo = self.animacion * 0.05 + k * 1.57
                pygame.draw.circle(pantalla, (255,255,255), (int(centro + math.cos(angulo) * 48), int(y + 62 + math.sin(angulo) * 36)), 3)
                
        #Vestido largo
        vestido_forma = [(centro - 12, y + 55), (centro + 12, y + 55), (centro + 38, y + self.alto), (centro - 38, y + self.alto)]
        pygame.draw.polygon(pantalla, vestido, vestido_forma)
        pygame.draw.polygon(pantalla, oscuro, vestido_forma, 3)
        pygame.draw.polygon(pantalla, vestido_claro, [(centro - 4, y + 70), (centro + 4, y + 70), (centro + 10, y + self.alto - 6), (centro - 10, y + self.alto - 6)])
            
        #Torso
        pygame.draw.ellipse(pantalla, vestido, (centro - 14, y + 40, 28, 34))
        pygame.draw.ellipse(pantalla, oscuro, (centro - 14, y + 40, 28, 34), 3)
        
        #Brazos
        brazo = int(math.sin(self.animacion * 0.1) * 6)
        altura = 15 if lanzado else 35
        pygame.draw.line(pantalla, piel, (centro - 12, y + 52), (centro - 34, y + altura + brazo), 6)
        pygame.draw.line(pantalla, piel, (centro + 12, y + 52), (centro + 34, y + altura - brazo), 6)
            
        #Pelo y cabeza
        pygame.draw.ellipse(pantalla, vestido_claro, (centro - 20, y + 4, 40, 36))
        pygame.draw.circle(pantalla, piel, (centro, y + 25), 16)
        pygame.draw.circle(pantalla, ojo, (centro - 6, y + 25), 3)
        pygame.draw.circle(pantalla, ojo, (centro + 6, y + 25), 3)
        
        #Corona de hielo
        corona = [(centro - 16, y + 10), (centro - 14, y - 8), (centro - 6, y + 4), (centro, y - 14), (centro + 6, y + 4), (centro + 14, y - 8), (centro + 16, y + 10)]
        pygame.draw.polygon(pantalla, (210,245,255), corona)
        pygame.draw.polygon(pantalla, (120,190,230), corona, 3)
        
        
            