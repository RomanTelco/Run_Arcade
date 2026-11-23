# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 22:41:01 2026

@author: Neo-PC
"""

#Menu Principal

import math
import random
import pygame
from config import *
import arte
from sprites import sprite_cacheado, _cuerpo_jugador, _andante, _volador, CHAQUETA

SUELO_MENU = Ventana_alto - 150

class Boton:
    def __init__(self, texto, accion, centro_y, ancho = 380, alto = 58):
        self.texto = texto
        self.accion = accion
        self.rect = pygame.Rect(0, 0, ancho, alto)
        self.rect.center = (Ventana_ancho // 2, centro_y)
        
    def etiqueta(self):
        return self.texto() if callable(self.texto) else self.texto
    
class MenuPrincipal:
    def __init__(self):
        self.f_titulo = pygame.font.Font(None, 130)
        self.f_boton = pygame.font.Font(None, 44)
        self.f_texto = pygame.font.Font(None, 34)
        self.f_pequeña = pygame.font.Font(None, 26)
        
        #Ajustes
        self.mostrar_fps = False
        
        #Pantalla actual
        self.pantalla_actual = 'principal'
        self.seleccion = 0
        
        self.botones_principal = [Boton('INICIAR', 'iniciar', 310), Boton('CONFIGURACION', 'config', 385), Boton('SALIR', 'salir', 460),]
        self.botones_config = [Boton(lambda: 'EFECTO CRT: ' + ('SI' if arte.EFECTO_CRT else 'NO'), 'crt', 260, 460), Boton(lambda: 'CONTADOR FPS: ' + ('SI' if self.mostrar_fps else 'NO'), 'fps', 320, 460), Boton('VOLVER', 'volver', 390, 460),]
        
        #Decoracion de fondo
        self.estrellas = [(random.randint(0, Ventana_ancho), random.randint(0, 330), random.random() * 6.28, random.choice((1,2,2,3))) for _ in range(70)]
        self.fondo = None
        self.escalados = {}
        
    def botones(self):
        return self.botones_principal if self.pantalla_actual == 'principal' else self.botones_config
    
    def _ejecutar(self, accion):
        #Devuelve iniciar o salir para que gestione el juego
        if accion == 'config':
            self.pantalla_actual = 'config'
            self.seleccion = 0
            return None
        if accion == 'volver':
            self.pantalla_actual = 'principal'
            self.seleccion = 1
            return None
        if accion == 'crt':
            arte.EFECTO_CRT = not arte.EFECTO_CRT
            return None
        if accion == 'fps':
            self.mostrar_fps = not self.mostrar_fps
            return None
        return accion
    
    def manejar_evento(self, evento, convertir):
        botones = self.botones()
        
        if evento.type == pygame.MOUSEMOTION:
            pos = convertir(evento.pos)
            for i, boton in enumerate(botones):
                if boton.rect.collidepoint(pos):
                    self.seleccion = i
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            pos = convertir(evento.pos)
            for i, boton in enumerate(botones):
                if boton.rect.collidepoint(pos):
                    self.seleccion = i
                    return self._ejecutar(boton.accion)
        elif evento.type == pygame.KEYDOWN:
            if evento.key in (pygame.K_UP, pygame.K_w):
                self.seleccion = (self.seleccion - 1) % len(botones)
            elif evento.key in (pygame.K_DOWN, pygame.K_s):
                self.seleccion = (self.seleccion + 1) % len(botones)
            elif evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                return self._ejecutar(botones[self.seleccion].accion)
            elif evento.key == pygame.K_ESCAPE:
                if self.pantalla_actual == 'config':
                    return self._ejecutar('volver')
                return 'salir'
        return None
    
    def dibujar(self, pantalla):
        t = pygame.time.get_ticks()
        self._dibujar_fondo(pantalla, t)
        self._dibujar_personajes(pantalla, t)
        self._dibujar_titulo(pantalla, t)
        
        for i, boton in enumerate(self.botones()):
            self._dibujar_boton(pantalla, boton, i == self.seleccion, t)
        
        if self.pantalla_actual == 'config':
            self._dibujar_controles(pantalla)
        
        pie = self.f_pequeña.render("Flechas o raton para moverte - ENTER o clic para elegir", True, (170,170,210))
        pantalla.blit(pie, (Ventana_ancho // 2 - pie.get_width() // 2, Ventana_alto - 36))
        
    def _dibujar_fondo(self, pantalla, t):
        #Cielo nocturno
        if self.fondo is None:
            self.fondo = pygame.Surface((Ventana_ancho, Ventana_alto))
            for y in range(Ventana_alto):
                k = y / Ventana_alto
                color = (int(14 + 70 * k), int(10 + 40 * k), int(40 + 90 * k))
                pygame.draw.line(self.fondo, color, (0,y), (Ventana_ancho, y))
        pantalla.blit(self.fondo, (0,0))
        
        #Estrellas que parpadean
        for x, y, fase , tam in self.estrellas:
            brillo = int(150 + 100 * math.sin(t * 0.003 + fase))
            pygame.draw.rect(pantalla, (brillo, brillo, min(255, brillo + 20)), (x, y, tam, tam))
            
        #Luna
        pygame.draw.circle(pantalla, (240,240,210), (1010, 120), 42)
        pygame.draw.circle(pantalla, (215, 215,185), (997,110), 9)
        pygame.draw.circle(pantalla, (215,215,185), (1024,134), 6)
        arte.resplandor(pantalla, 1010, 120, 110, (60,60,40), 0.7)
        
        #Montañas
        for velocidad, base, alto, ancho, color in ((0.02, 470,150,340,(44,32,92)), (0.05,520,110,240,(30,22,66))):
            desplazamiento = (t * velocidad) % ancho
            x = -ancho - desplazamiento + ancho
            while x < Ventana_ancho + ancho:
                pygame.draw.polygon(pantalla, color, [(x - ancho // 2, SUELO_MENU), (x, base - alto), (x+ ancho // 2, SUELO_MENU)])
                x += ancho
        
        #Suelo
        pygame.draw.rect(pantalla, arte.sombrear(Colores['Suelo'], 0.45), (0, SUELO_MENU, Ventana_ancho, Ventana_alto - SUELO_MENU))
        pygame.draw.rect(pantalla, arte.sombrear(Colores['Hierba'], 0.6), (0, SUELO_MENU, Ventana_ancho, 10))
        desplazamiento = (t * 0.35) % 60
        for x in range(-60, Ventana_ancho + 60, 60):
            pygame.draw.line(pantalla, arte.sombrear(Colores['Suelo'], 0.35), (x - desplazamiento, SUELO_MENU + 40), (x - desplazamiento + 30, SUELO_MENU + 40), 4)
    
    def _escalar(self, clave, sprite, factor=2):
        escalado = self.escalados.get(clave)
        if escalado is None:
            escalado = pygame.transform.scale(sprite, (sprite.get_width() * factor, sprite.get_height() * factor))
            self.escalados[clave] = escalado
        return escalado
    
    def _dibujar_personajes(self, pantalla, t):
        #Heroe
        frame = (t // 85) % 4
        sprite, ox, oy = sprite_cacheado(('jugador', 'correr', frame, 0, False), 40, 80, lambda s, x, y: _cuerpo_jugador(s, x, y, 'correr', frame, CHAQUETA), factor = 2, margen = 24)
        arte.sombra_suelo(pantalla, 180, SUELO_MENU, 110, 100)
        pantalla.blit(self._escalar(('jugador', frame), sprite), (140 - ox * 2, SUELO_MENU - 160 - oy * 2))
        
        #Andante
        f = (t // 100) % 4
        sprite, ox, oy = sprite_cacheado(('andante', f, True, False), 50, 70, lambda s, x, y: _andante(s,x,y,50,70,f), factor = 2, margen = 10, volteo = True)
        arte.sombra_suelo(pantalla, 950, SUELO_MENU, 110, 100)
        pantalla.blit(self._escalar(('andante', f), sprite), (900 - ox * 2, SUELO_MENU - 140 - oy * 2))
        
        #Volador
        f = (t // 100) % 4
        sprite, ox, oy = sprite_cacheado(('volador', f, False), 45, 45, lambda s, x, y: _volador(s, x, y, 45, 45, f), factor = 2, margen = 16)
        flota = int(math.sin(t * 0.003) * 14)
        px = 1040
        py = 300 + flota
        pantalla.blit(self._escalar(('volador', f), sprite), (px - ox * 2, py - oy * 2))
        arte.resplandor(pantalla, px + 45, py + 100, 46, (255,140,30), 0.6)
        
    def _dibujar_titulo(self,pantalla,t):
        texto = "RUN ARCADE"
        centro_x = Ventana_ancho // 2
        y = 70 + int(math.sin(t*0.003)*6)
        arte.resplandor(pantalla, centro_x, y+55, 280,(255,110,60), 0.35)
        arte.texto_contorno(pantalla, self.f_titulo, texto, centro_x, y+6, (20,6,40),(20,6,40),6)
        arte.texto_contorno(pantalla, self.f_titulo, texto, centro_x, y, (255,214,64), (60,10,60),5)
        
        #Parte de abajo del titulo en naranja
        naranja = self.f_titulo.render(texto, True, (255,120,40))
        bx = centro_x - naranja.get_width()//2
        pantalla.set_clip(pygame.Rect(bx, y + int(naranja.get_height()*0.55), naranja.get_width(), naranja.get_height()))
        pantalla.blit(naranja, (bx,y))
        pantalla.set_clip(None)
        
        subtitulo = "CORRE, SALTA Y DISPARA"
        arte.texto_contorno(pantalla, self.f_texto, subtitulo, centro_x, y+118, (200,225,255), (20,10,50),2)
        
    def _dibujar_boton(self, pantalla, boton, seleccionado, t):
        rect = boton.rect
        
        #Sombra
        pygame.draw.rect(pantalla, (8,4,20), rect.move(0,6), border_radius=12)
        
        if seleccionado:
            pulso = 0.5 + 0.5 * math.sin(t*0.008)
            borde = arte.mezclar((255,170,40), (255,240,120), pulso)
            pygame.draw.rect(pantalla, (70,32,100), rect, border_radius=12)
            pygame.draw.rect(pantalla, (110,60,140), (rect.x + 4, rect.y + 4, rect.w - 8, 10), border_radius=6)
            pygame.draw.rect(pantalla, borde, rect, 4, border_radius=12)
            color_texto = (255,232,110)
            
            #Flechas a los lados
            mov = int(math.sin(t*0.01) * 4)
            cy = rect.centery
            pygame.draw.polygon(pantalla, borde, [(rect.x - 34 + mov, cy - 12), (rect.x - 34 + mov, cy + 12), (rect.x - 14 + mov, cy)])
            pygame.draw.polygon(pantalla, borde, [(rect.right + 34 - mov, cy - 12), (rect.right + 34 - mov, cy + 12), (rect.right + 14 - mov, cy)])
        else:
            pygame.draw.rect(pantalla, (28,20,56), rect, border_radius=12)
            pygame.draw.rect(pantalla, (50,38,92), (rect.x + 4, rect.y + 4, rect.w - 8, 10), border_radius=6)
            pygame.draw.rect(pantalla, (100, 90, 170), rect, 3, border_radius=12)
            color_texto = (225,225,245)
        
        etiqueta = boton.etiqueta()
        arte.texto_contorno(pantalla, self.f_boton, etiqueta, rect.centerx, rect.centery - self.f_boton.get_height() // 2 + 2, color_texto, (15,8,30), 2)
    

    def _dibujar_controles(self, pantalla):
        #Panel con los controles del juego
        panel = pygame.Surface((560,200), pygame.SRCALPHA)
        panel.fill((10,6,24,190))
        pantalla.blit(panel, (Ventana_ancho // 2 - 280, 450))
        pygame.draw.rect(pantalla, (100,90,170), (Ventana_ancho // 2 - 280, 450, 560, 200), 3, border_radius=8)
        arte.texto_contorno(pantalla, self.f_texto, "CONTROLES", Ventana_ancho // 2, 458, (255,214,64), (20,8,30),2)
        lineas = ["Moverse: flechas o A D", "Saltar: ESPACIO, W o flecha arriba (doble salto)", "Disparar: click izquierdo   Misil: click derecho", "Pausa: P    Volver al menu: ESC",]
        for i, linea in enumerate(lineas):
            render = self.f_pequeña.render(linea, True, (225,225,245))
            pantalla.blit(render, (Ventana_ancho // 2 - render.get_width() // 2, 498 + i * 34))
    