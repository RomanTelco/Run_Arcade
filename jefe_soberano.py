# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 15:26:46 2026

@author: Neo-PC
"""

#Jefe Final nivel 7
import pygame
import random
import math
from config import *
from jefe import Jefe

class JefeSoberano(Jefe):
    def __init__(self, config_jefe, suelo_y):
        super().__init__(config_jefe, suelo_y)
        
        #Area del juego final
        self.limite_izquierdo = 560
        self.altura_vuelo = 150
        self.y = self.altura_vuelo
        
        #Movimiento del jefe
        self.fase_mov = 'flotando'
        self.tiempo_fase = 0
        self.tiempo_caida = 300
        
        #Fases del combate
        self.fase_actual = 1
        self.transformacion = 0
        
        #Ataques
        self.tiempo_espiral = 140
        self.espiral_activa = 0
        self.giro = 0
        self.tiempo_rayos = 240
        self.rayos = []
        self.ondas = []
        
        self.direccion = 1
        
    def numero_fase(self):
        if self.vida > self.vida_maxima * 2 / 3:
            return 1
        elif self.vida > self.vida_maxima / 3:
            return 2
        else:
            return 3
    
    def furioso(self):
        return self.numero_fase() >= 3
    
    def color_fase(self):
        return [(0,220,255), (255,60,220), (255,50,50)][self.numero_fase() - 1]
    
    def mover(self, jugador):
        fase = self.numero_fase()
        
        #Cambio de fases del jefe
        if fase != self.fase_actual:
            self.fase_actual = fase
            self.transformacion = 90
            self.destello = 60
            self.proyectiles = []
            self.rayos = []
            self.fase_mov = 'subiendo'
            self.espiral_activa = 0
            self.tiempo_espiral = 100
            self.tiempo_rayos = 150
            self.tiempo_caida = 250
            jugador.recargar_balas(15)
            
        if self.transformacion > 0:
            self.transformacion -= 1
            if self.y > self.altura_vuelo:
                self.y -= 6
            return
        
        if self.fase_mov == 'flotando':
            self.x += self.direccion * (1.2 + 0.4 * (fase - 1))
            if self.x <= self.limite_izquierdo:
                self.direccion = 1
            elif self.x >= self.limite_derecho:
                self.direccion = -1
            altura = self.altura_vuelo + math.sin(self.animacion * 0.04) * 20
            self.y += (altura - self.y) * 0.1
            
            if fase >= 2:
                self.tiempo_caida -= 1
                if self.tiempo_caida <= 0:
                    self.fase_mov = 'preparando'
                    self.tiempo_fase = 45
        elif self.fase_mov == 'preparando':
            self.tiempo_fase -= 1
            self.y -= 1
            if self.tiempo_fase <= 0:
                self.fase_mov = 'cayendo'
        
        elif self.fase_mov == 'cayendo':
            self.y += 24
            if self.y >= self.suelo_y - self.alto:
                self.y = self.suelo_y - self.alto
                self.fase_mov = 'aturdido'
                self.tiempo_fase = 80 if fase >= 3 else 100
                velocidad = 10 if fase >= 3 else 8
                centro = self.x + self.ancho / 2
                self.ondas.append({'x': centro, 'dir': -1, 'velocidad':velocidad, 'golpeo':False})
                self.ondas.append({'x': centro, 'dir': 1, 'velocidad':velocidad, 'golpeo':False})
        
        elif self.fase_mov == 'aturdido':
            self.tiempo_fase -= 1
            if self.tiempo_fase <= 0:
                self.fase_mov = 'subiendo'
                
        elif self.fase_mov == 'subiendo':
            self.y -= 6
            if self.y <= self.altura_vuelo:
                self.y = self.altura_vuelo
                self.fase_mov = 'flotando'
                self.tiempo_caida = 220 if fase >= 3 else 300
                
        self.x = max(0, min(Ventana_ancho - self.ancho, self.x))
    
    def disparar(self, jugador):
        if self.transformacion > 0:
            return
        fase = self.numero_fase()
        
        #Ataque 1
        if self.fase_mov == 'flotando':
            if self.espiral_activa > 0:
                self.espiral_activa -= 1
                if self.espiral_activa % 5 == 0:
                    self.lanzar_orbes(fase)
            else:
                self.tiempo_espiral -= 1
                if self.tiempo_espiral <= 0:
                    self.espiral_activa = 60
                    self.tiempo_espiral = (140,110,90)[fase -1]
        #Ataque 2
        self.tiempo_rayos -= 1
        if self.tiempo_rayos <= 0:
            self.tiempo_rayos = (240,190,150)[fase - 1]
            self.lanzar_rayos(jugador, fase)
        
    def lanzar_orbes(self, fase):
        centro_x = self.x + self.ancho / 2
        centro_y = self.y + self.alto * 0.45
        self.giro += 0.4
        for brazo in range(fase):
            angulo = self.giro + brazo * 2 * math.pi / fase
            self.proyectiles.append({'x': centro_x, 'y': centro_y, 'vx': math.cos(angulo) * 5, 'vy': math.sin(angulo) * 5, 'radio': 9})
                
    def lanzar_rayos(self,jugador,fase):
        cantidad = (2,3,4)[fase - 1]
        columnas = list(range(60, Ventana_ancho - 60, 110))
        random.shuffle(columnas)
        elegidas = columnas[:cantidad]
        elegidas[0] = int(jugador.x + jugador.ancho / 2)
        for x in elegidas:
            self.rayos.append({'x':x, 'tiempo': 0, 'golpeo':False})
                
    def recibir_balas(self, balas):
        if self.transformacion > 0:
            return 0
        puntos = 0
        daño = 2 if self.fase_mov == 'aturdido' else 1
        for bala in balas[:]:
            bala_rect = pygame.Rect(bala['x'], bala['y'], bala['ancho'], bala['alto'])
            if self.rect.colliderect(bala_rect):
                balas.remove(bala)
                self.recibir_daño(daño)
                puntos += 25
        return puntos
        
    def actualizar_proyectiles(self, jugador):
        #Ataque con orbes
        for p in self.proyectiles[:]:
            if p['y'] >= self.suelo_y - 5:
                self.proyectiles.remove(p)
        super().actualizar_proyectiles(jugador)
            
        #Ataque con rayos
        for r in self.rayos[:]:
            r['tiempo'] += 1
            if 50 <= r['tiempo'] < 75:
                rect_rayo = pygame.Rect(r['x'] - 25, 0, 50, self.suelo_y)
                if not r['golpeo'] and rect_rayo.colliderect(jugador.rect):
                    jugador.recibir_daño()
                    r['golpeo'] = True
            elif r['tiempo'] >= 75:
                self.rayos.remove(r)
            
        #Ataque con ondas
        for onda in self.ondas[:]:
            onda['x'] += onda['dir'] * onda['velocidad']
            if onda['x'] < -40 or onda['x'] > Ventana_ancho + 40:
                self.ondas.remove(onda)
                continue
            rect_onda = pygame.Rect(onda['x'] - 18, self.suelo_y - 45, 36, 45)
            if not onda['golpeo'] and rect_onda.colliderect(jugador.rect):
                jugador.recibir_daño()
                onda['golpeo'] = True
            
    def morir(self):
        self.rayos = []
        self.ondas = []
        super().morir()
            
    def dibujar(self, pantalla):
        color = self.color_fase()
            
        #Rayos y su aviso
        for r in self.rayos:
            x = int(r['x'])
            if r['tiempo'] < 50:
                if (r['tiempo'] // 4) % 2 == 0:
                    pygame.draw.line(pantalla, color, (x,0), (x, self.suelo_y), 2)
                pygame.draw.ellipse(pantalla, color, (x - 20, self.suelo_y - 6, 40, 12))
            else:
                pygame.draw.rect(pantalla, color, (x - 25, 0, 50, self.suelo_y))
                pygame.draw.rect(pantalla, (255,255,255), (x - 10, 0, 20, self.suelo_y))
                    
        #Ondas de choque
        for onda in self.ondas:
            x = int(onda['x'])
            suelo = self.suelo_y
            puntos = [(x-18, suelo), (x-8, suelo - 45), (x + 4, suelo - 30), (x + 12, suelo - 45), (x + 18, suelo)]
            pygame.draw.polygon(pantalla, (150,80,220), puntos)
            pygame.draw.polygon(pantalla, (60,20,110), puntos, 3)
            
        #Orbes
        for p in self.proyectiles:
            centro = (int(p['x']), int(p['y']))
            pygame.draw.circle(pantalla, color, centro, p['radio'] + 3)
            pygame.draw.circle(pantalla, (255,255,255), centro, p['radio'] - 2)
                
        if self.estado == 'muriendo':
            self.dibujar_muerte(pantalla)
            return
            
        if self.transformacion > 0:
            centro = (int(self.x + self.ancho / 2), int(self.y + self.alto / 2))
            for k in range(3):
                radio = (90 - self.transformacion) * 6 - k * 40
                if radio > 0:
                    pygame.draw.circle(pantalla, color, centro, radio, 4)
            
        self.dibujar_cuerpo(pantalla)
        self.dibujar_barra_vida(pantalla)
        self.dibujar_aviso(pantalla)
            
        if self.transformacion > 0:
            if Jefe.fuente_aviso is None:
                Jefe.fuente_aviso = pygame.font.Font(None, 72)
                
            txt = 'FASE' + str(self.numero_fase()) + "!"
            sombra_txt = Jefe.fuente_aviso.render(txt, True, (60,60,60))
            texto = Jefe.fuente_aviso.render(txt, True, (0,0,0))
            texto_x = Ventana_ancho // 2 - texto.get_width() // 2
            pantalla.blit(sombra_txt, (texto_x + 3, 283))
            pantalla.blit(texto, (texto_x, 280))
                    
    def dibujar_cuerpo(self, pantalla, desplazamiento_x = 0, desplazamiento_y = 0):
        x = int(self.x) + desplazamiento_x
        y = int(self.y) + desplazamiento_y
        if self.fase_mov == 'preparando':
            x += random.randint(-3, 3)
        centro = x + self.ancho // 2
        color = self.color_fase()
            
        #Colores del cuerpo
        capa = (30,10,60)
        borde = (120,60, 200)
        if self.destello > 0 and self.destello % 4 < 2:
            capa = (255,255,255)
            borde = (255,255,255)
            
        #Ultima fase del jefe
        if self.numero_fase() >= 3:
            aura = int(math.sin(self.animacion * 0.3) * 4)
            pygame.draw.ellipse(pantalla, color, (centro - 85 - aura, y - 10 - aura, 170 + aura * 2, self.alto + 20 + aura * 2), 2)
                
        #Capa
        forma_capa = [(centro - 55, y + 60),(centro + 55, y + 60), (centro + 70, y + self.alto), (centro + 30, y + self.alto - 25), (centro, y + self.alto), (centro - 30, y + self.alto - 25), (centro - 70, y + self.alto)]
        pygame.draw.polygon(pantalla, capa, forma_capa)
        pygame.draw.polygon(pantalla, borde, forma_capa, 3)
            
        #Manos flotantes
        balanceo = int(math.sin(self.animacion * 0.08) * 8)
        for mano_x, signo in ((centro - 85, 1), (centro + 85, -1)):
            pygame.draw.circle(pantalla, capa, (mano_x, y + 95 + balanceo * signo), 14)
            pygame.draw.circle(pantalla, color, (mano_x, y + 95 + balanceo * signo), 14, 3)
            
        #Nucleo del pecho
        pulso = int(math.sin(self.animacion * 0.025) * 3)
        nucleo = (255,255,255) if (self.fase_mov == 'aturdido' and self.animacion % 6 < 3) else color
        pygame.draw.circle(pantalla, nucleo, (centro, y + 105), 20 + pulso)
        pygame.draw.circle(pantalla, (255,255,255), (centro, y + 105), 9)
            
        #Cabeza con corona
        pygame.draw.circle(pantalla, capa, (centro, y + 40), 34)
        pygame.draw.circle(pantalla, borde, (centro, y + 40), 34, 3)
            
        for k in range(5):
            angulo = math.pi + k * math.pi / 4
            base_x = centro + math.cos(angulo) * 34
            base_y = y + 40 + math.sin(angulo) * 34
            punta_x = centro + math.cos(angulo) * 52
            punta_y = y + 40 + math.sin(angulo) * 52
            pygame.draw.line(pantalla, color, (int(base_x), int(base_y)), (int(punta_x), int(punta_y)), 5)
                
        #Ojos brillantes
        pygame.draw.circle(pantalla, color, (centro - 14, y + 38), 8)
        pygame.draw.circle(pantalla, color, (centro + 14, y + 38), 8)
        pygame.draw.circle(pantalla, (255,255,255), (centro - 14, y + 38), 3)
        pygame.draw.circle(pantalla, (255,255,255), (centro + 14, y + 38), 3)
            
        #Orbes que giran alrededor
        for k in range(3):
            angulo = self.animacion * 0.05 + k * 2.1
            pygame.draw.circle(pantalla, color, (int(centro + math.cos(angulo) * 80), int(y + 70  + math.sin(angulo) * 50)), 5)
                
        #Estrellitas cuando esta aturdido
        if self.fase_mov == 'aturdido':
            for k in range(3):
                angulo = self.animacion * 0.15 + k * 2.1
                pygame.draw.circle(pantalla, (255,255,0), (int(centro + math.cos(angulo) * 30), int(y - 18 + math.sin(angulo) * 8)), 5)
            
        
                
        
        
        
            