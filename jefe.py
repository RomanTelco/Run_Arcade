# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 20:29:37 2026

@author: Neo-PC
"""

#Jefe final

import pygame
import random
import math
from config import *
from jugador import crear_bip
from obstaculo import crear_explosion_nave

#Clase del jefe final
class Jefe:
    #Fuentes y sonidos
    fuente_nombre = None
    fuente_aviso = None
    sonido_golpe = None
    sonido_derrota = None
    
    def __init__(self, config_jefe, suelo_y):
        #Propiedades que va a tener el jefe final
        self.nombre = config_jefe['Nombre']
        self.vida_maxima = config_jefe['Vida']
        self.vida = self.vida_maxima
        self.puntos = config_jefe['Puntos']
        self.ancho = config_jefe['Ancho']
        self.alto = config_jefe['Alto']
        self.suelo_y = suelo_y
        
        #Posicion en la que se va a encontrar el jefe
        self.x = Ventana_ancho + 50
        self.y = suelo_y - self.alto
        self.velocidad_y = 0
        self.direccion = -1
        
        #Zona de la pantalla en la que se va a encontrar
        self.limite_izquierdo = Ventana_ancho // 2
        self.limite_derecho = Ventana_ancho - self.ancho - 20
        
        #Estados del jefe final
        self.estado = 'entrando'
        self.derrotado = False
        
        #Temporizadores
        self.tiempo_salto = 150
        self.tiempo_disparo = 90
        self.inmune = 0
        self.destello = 0
        self.tiempo_muerto = 0
        self.animacion = 0
        
        #Municion que dispara
        self.proyectiles = []
        
        #Angulo de colision
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        
    def furioso(self):
        #Cuando le queda la mitad de vida se pone mas dificil
        return self.vida <= self.vida_maxima / 2
    
    def actualizar(self, jugador, balas):
        #Devuelve puntos que gana el jugador principal
        puntos = 0
        self.animacion += 1
        
        if self.inmune > 0:
            self.inmune -= 1
        if self.destello > 0:
            self.destello -= 1
            
        if self.estado == 'entrando':
            self.x -= 4
            if self.x <= self.limite_derecho:
                self.x = self.limite_derecho
                self.estado = 'activo'
        elif self.estado == 'activo':
            self.mover(jugador)
            self.disparar(jugador)
        elif self.estado == 'muriendo':
            self.tiempo_muerto += 1
            if self.tiempo_muerto >= 120:
                self.derrotado = True
        
        #Rectangulo de colision
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        
        if self.estado == 'activo':
            puntos += self.recibir_balas(balas)
            puntos += self.colisionar_jugador(jugador)
            
            #Muerte del jefe
            if self.vida <= 0:
                self.morir()
                puntos += self.puntos
        self.actualizar_proyectiles(jugador)
        return puntos
    
    def mover(self, jugador):
        furioso = self.furioso()
        velocidad = 2.5 if furioso else 1.5
        en_suelo = self.y >= self.suelo_y - self.alto
        
        #Movimiento del jefe
        if en_suelo:
            self.x += self.direccion * velocidad
        else:
            self.x += self.direccion * velocidad * 3
            
        if self.x <= self.limite_izquierdo:
            self.x = self.limite_izquierdo
            self.direccion = 1
        elif self.x >= self.limite_derecho:
            self.x = self.limite_derecho
            self.direccion = -1
            
        #Salta hacia el jugador
        self.tiempo_salto -= 1
        if self.tiempo_salto <= 0 and en_suelo:
            self.velocidad_y = -16
            self.direccion = -1 if jugador.x < self.x else 1
            if furioso:
                self.tiempo_salto = random.randint(90,140)
            else:
                self.tiempo_salto = random.randint(130, 200)
        
        #Gravedad
        self.velocidad_y += Gravedad
        self.y += self.velocidad_y
        if self.y >= self.suelo_y - self.alto:
            self.y = self.suelo_y - self.alto
            self.velocidad_y = 0
    
    def disparar(self, jugador):
        self.tiempo_disparo -= 1
        if self.tiempo_disparo > 0:
            return
        
        furioso = self.furioso()
        self.tiempo_disparo = 60 if furioso else 100
        
        #La municion del jefe sale de la boca
        origen_x = self.x + 10
        origen_y = self.y + self.alto * 0.4
        objetivo_x = jugador.x + jugador.ancho / 2
        objetivo_y = jugador.y + jugador.alto / 2
        angulo_base = math.atan2(objetivo_y - origen_y, objetivo_x - origen_x)
        
        if furioso:
            angulos = [angulo_base - 0.25, angulo_base, angulo_base + 0.25]
        else:
            angulos = [angulo_base]
            
        for angulo in angulos:
            self.proyectiles.append({'x':origen_x, 'y':origen_y, 'vx': math.cos(angulo) * 6, 'vy': math.sin(angulo)* 6, 'radio': 12})
            
    def actualizar_proyectiles(self, jugador):
        for p in self.proyectiles[:]:
            p['x'] += p['vx']
            p['y'] += p['vy']
            
            #Fuera de la pantalla
            if p['x'] < -50 or p['x'] > Ventana_ancho + 50 or p['y'] < -50 or p['y'] > Ventana_alto + 50:
                self.proyectiles.remove(p)
                continue
            
            #Colisionan con el personaje principal
            radio = p['radio']
            rect_proyectil = pygame.Rect(p['x']- radio, p['y'] - radio, radio * 2, radio * 2)
            if rect_proyectil.colliderect(jugador.rect):
                jugador.recibir_daño()
                self.proyectiles.remove(p)
                
    def recibir_balas(self, balas):
        #Daño del jugador
        puntos = 0
        for bala in balas[:]:
            bala_rect = pygame.Rect(bala['x'], bala['y'], bala['ancho'], bala['alto'])
            if self.rect.colliderect(bala_rect):
                balas.remove(bala)
                self.recibir_daño(1)
                puntos += 25
        return puntos
    
    def recibir_daño(self, cantidad, inmunidad = 0):
        self.vida -= cantidad
        if inmunidad > 0:
            self.inmune = inmunidad
            self.destello = inmunidad
        else:
            self.destello = 6
        self.reproducir_golpe()
        
    def colisionar_jugador(self, jugador):
        if not self.rect.colliderect(jugador.rect):
            return 0
        
        #Jugador coge la moneda de invencibilidad y hace daño al jefe
        if jugador.invencible_por_moneda:
            if self.inmune == 0:
                self.recibir_daño(1, 20)
                return 25
            return 0
        
        if jugador.invencible:
            return 0
        
        #Salto sobre la cabeza del jefe hace daño
        zona_cabeza = pygame.Rect(self.x, self.y, self.ancho, 30)
        if jugador.velocidad_y > 0 and jugador.pies_rect.colliderect(zona_cabeza):
            jugador.velocidad_y = -12
            if self.inmune == 0:
                self.recibir_daño(3, 30)
                return 100
            return 0
        
        #Al chocar el jugador recibe daño
        jugador.recibir_daño()
        return 0
    
    def morir(self):
        self.estado = 'muriendo'
        self.vida = 0
        self.proyectiles = []
        self.reproducir_derrota()
        
    def reproducir_golpe(self):
        try:
            if Jefe.sonido_golpe is None:
                Jefe.sonido_golpe = crear_bip(160, 0.08, 0.3)
            if Jefe.sonido_golpe:
                Jefe.sonido_golpe.play()
        except pygame.error:
            pass
        
    def reproducir_derrota(self):
        try:
            if Jefe.sonido_derrota is None:
                Jefe.sonido_derrota = crear_explosion_nave(1.2, 0.4)
            if Jefe.sonido_derrota:
                Jefe.sonido_derrota.play()
        except pygame.error:
            pass
        
    def dibujar(self, pantalla):
        #Bolas de baba
        for p in self.proyectiles:
            centro = (int(p['x']), int(p['y']))
            pygame.draw.circle(pantalla, (40,120,40), centro, p['radio'] + 3)
            pygame.draw.circle(pantalla, (120,255,120), centro, p['radio'])
            pygame.draw.circle(pantalla, (220,255,220), (centro[0] - 4, centro[1] - 4), 4)
            
        if self.estado == 'muriendo':
            self.dibujar_muerte(pantalla)
            return
        
        self.dibujar_cuerpo(pantalla)
        self.dibujar_barra_vida(pantalla)
        self.dibujar_aviso(pantalla)
        
    def dibujar_cuerpo(self, pantalla, desplazamiento_x = 0, desplazamiento_y = 0):
        x = int(self.x) + desplazamiento_x
        y = int(self.y) + desplazamiento_y
        
        #Color
        color = (200,70,50) if self.furioso() else (60,180,60)
        if self.destello > 0 and self.destello % 4 < 2:
            color = (255,255,255)
        color_oscuro = (max(0, color[0] - 60), max(0, color[1] - 60), max(0, color[2] - 60))
        color_claro = (min(255, color[0] + 60), min(255, color[1] + 60), min(255, color[2] + 60))
        
        #Cuerpo se aplasta y se estira cuando esta en movimiento
        aplaste = int(math.sin(self.animacion * 0.15) * 5)
        cuerpo = pygame.Rect(x - aplaste, y + 10 + aplaste, self.ancho + aplaste * 2, self.alto - 10 - aplaste)
        pygame.draw.ellipse(pantalla, color, cuerpo)
        pygame.draw.ellipse(pantalla, color_oscuro, cuerpo, 4)
        pygame.draw.ellipse(pantalla, color_claro, (x + 25, y + 28, 40, 18))
        
        #Ojos enfadados
        ojo_y = y + int(self.alto * 0.4)
        for ojo_x in (x + int(self.ancho * 0.3), x + int(self.ancho * 0.68)):
            pygame.draw.circle(pantalla, (255,255,255), (ojo_x, ojo_y), 14)
            pygame.draw.circle(pantalla, (0,0,0), (ojo_x - 4, ojo_y), 6)
        pygame.draw.line(pantalla, (0,0,0), (x + int(self.ancho * 0.3) - 16, ojo_y - 20), (x + int(self.ancho * 0.3) + 10, ojo_y - 10), 4)
        pygame.draw.line(pantalla, (0,0,0), (x + int(self.ancho * 0.68) + 16, ojo_y - 20), (x + int(self.ancho * 0.68) - 10, ojo_y - 10), 4)
        
        #Boca con dientes
        boca = pygame.Rect(x + int(self.ancho * 0.3), y + int(self.alto * 0.65), int(self.ancho * 0.4), 24)
        pygame.draw.ellipse(pantalla, (40,0,0), boca)
        for i in range(4):
            pygame.draw.rect(pantalla, (255,255,255), (boca.x + 14 + i * 20, boca.y + 3, 8, 8))
            
        #Corona
        centro_x = x + self.ancho // 2 
        base = y + 16
        corona = [(centro_x - 40, base), (centro_x - 40, base - 28), (centro_x - 20, base - 12), (centro_x, base - 34), (centro_x + 20, base - 12),  (centro_x + 40, base - 28),  (centro_x + 40, base)]
        pygame.draw.polygon(pantalla, (255, 215, 0), corona)
        pygame.draw.polygon(pantalla, (200, 150, 0), corona, 3)
        pygame.draw.circle(pantalla, (220, 30, 30),(centro_x, base - 12), 5)
        
    def dibujar_muerte(self, pantalla):
        #Muerte del jefe
        if self.tiempo_muerto < 100 and self.tiempo_muerto % 8 < 5:
            self.dibujar_cuerpo(pantalla, random.randint(-4, 4), random.randint(-4, 4))
            
        if self.tiempo_muerto < 110:
            for i in range(4):
                centro_x = int(self.x + random.randint(0, self.ancho))
                centro_y = int(self.y + random.randint(0, self.alto))
                radio = random.randint(10, 10 + self.tiempo_muerto // 2)
                color = random.choice([(255,200,0), (255,120,0), (255,255,200)])
                pygame.draw.circle(pantalla, color, (centro_x, centro_y), radio)
    
    def dibujar_barra_vida(self, pantalla):
        if Jefe.fuente_nombre is None: 
            Jefe.fuente_nombre = pygame.font.Font(None, 28)
        
        barra_ancho = 400
        barra_alto = 18
        barra_x = Ventana_ancho // 2 - barra_ancho // 2
        barra_y = 115
        
        proporcion = max(0, self.vida) / self.vida_maxima
        color_barra = (220,50,50) if self.furioso() else (60,200,60)
        
        pygame.draw.rect(pantalla, (60,0,0), (barra_x, barra_y, barra_ancho, barra_alto))
        pygame.draw.rect(pantalla, color_barra, (barra_x, barra_y, int(barra_ancho * proporcion), barra_alto))
        pygame.draw.rect(pantalla, (255, 255, 255), (barra_x, barra_y, barra_ancho, barra_alto), 2)
        
        texto = Jefe.fuente_nombre.render(self.nombre, True, (255,255,255))
        pantalla.blit(texto, (barra_x, barra_y - 22))
        
    def dibujar_aviso(self, pantalla):
        #Mensaje de que aparece el jefe
        if self.animacion > 150:
            return
        
        if Jefe.fuente_aviso is None:
            Jefe.fuente_aviso = pygame.font.Font(None, 72)
            
        texto = Jefe.fuente_aviso.render("JEFE FINAL!", True, (255,255,255))
        sombra = Jefe.fuente_aviso.render("JEFE FINAL!", True, (0,0,0))
        x = Ventana_ancho // 2 - texto.get_width() // 2
        pantalla.blit(sombra, (x+3, 223))
        pantalla.blit(texto, (x,220))
        
            
    
            
            

            
            
            
            
            
            
            
            
            
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
            
        
    
        