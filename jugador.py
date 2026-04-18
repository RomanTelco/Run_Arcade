# -*- coding: utf-8 -*-
"""
Created on Wed Feb  4 19:17:48 2026

@author: Neo-PC
"""

import pygame
import math
from config import *

#Fichero del jugador principal
class Jugador:
    def __init__(self,x,y):
        #Posicion y tamaño del personaje principal
        self.x = x
        self.y = y
        self.ancho = Config_Jugador['Ancho']
        self.alto = Config_Jugador['Alto']
        
        #Salto del jugador
        self.saltando = False
        
        #Fisica del jugador principal
        self.velocidad_x = 0
        self.velocidad_y = 0
        self.aceleracion_x = 0
        self.en_el_suelo = False
        self.salto = False
        self.salto_doble = False
        
        #Estados del personaje pricipal
        self.vidas = Config_Jugador['Vidas']
        self.balas = Config_Jugador['Balas']
        self.puntuacion = 0
        self.monedas = 0
        self.invencible = False
        self.tiempo_invencible = 0
        self.muerto = False
        self.mira_a_derecha = True
        
        #Animacion del personaje principal
        self.animacion_frame = 0
        self.animacion_tiempo = 0
        self.animacion_velocidad = 5
        self.estado = 'quieto'
        
        #Personaje principal disparo
        self.disparo = True
        self.no_disparo = 0
        
        #Colision
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        self.pies_rect = pygame.Rect(self.x + 5, self.y + self.alto - 10, self.ancho - 10, 10)
        
    #En caso de la muerte del personaje principal
    def actualizar(self, teclas, mouse_click = False):
        if self.muerto:
            return []
        
        balas_disparadas = []
        
        #Procesamiento de entrada
        self.procesar_entrada(teclas)
    
        #Disparo con raton
        if mouse_click and self.disparo and self.balas > 0:
            bala = self.disparar()
            if bala:
                balas_disparadas.append(bala)
        
        if self.no_disparo > 0:
            self.no_disparo -= 1
            if self.no_disparo <= 0:
                self.disparo = True
        
        #Se aplica la fisica del personaje pricipal
        self.aplicar_fisica()
        
        #Se actualizan las animaciones
        self.actualizar_animacion()
        self.actualizar_invencibilidad()
        
        #Se actualiza el personaje pricipal
        self.rect.x = self.x
        self.rect.y = self.y
        self.pies_rect.x = self.x + 5
        self.pies_rect.y = self.y + self.alto - 10
        
        #Limitamos la posicion a la que puede llegar el personaje pricipal
        if self.y < 0:
            self.y = 0
            self.velocidad_y = 0
            
        if self.y > Ventana_alto + 100:
            self.morir()
            
        return balas_disparadas

    def procesar_entrada(self, teclas):
        self.aceleracion_x = 0
        
        #Movimineto horizontal del personaje pricipal
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.aceleracion_x = -Aceleracion
            self.mira_a_derecha = False
            self.estado = 'corriendo'
        elif teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.aceleracion_x = Aceleracion
            self.mira_a_derecha = True
            self.estado = 'corriendo'
        else:
            if self.en_el_suelo:
                self.estado = 'quieto'
                
        #Salto del personaje pricipal
        if (teclas[pygame.K_SPACE] or teclas[pygame.K_w] or teclas[pygame.K_UP]) and self.en_el_suelo:
            self.saltar()
        elif (teclas[pygame.K_SPACE] or teclas[pygame.K_w] or teclas[pygame.K_UP]) and not self.salto_doble:
            self.salto_doble = True
            self.velocidad_y = Fuerza_Salto * 0.8
        
    def aplicar_fisica(self):
        self.velocidad_x += self.aceleracion_x
        self.velocidad_x *= Friccion
        
        #Limite de velocidad
        if abs(self.velocidad_x) > Velocidad_maxima:
            self.velocidad_x = Velocidad_maxima if self.velocidad_x > 0 else -Velocidad_maxima
            
        #Actualizacion de las posiciones y fisicas del juego
        self.x += self.velocidad_x
        self.velocidad_y += Gravedad
        self.y += self.velocidad_y
        self.en_el_suelo = False
        
        if self.velocidad_y >= 0 and self.y >= Ventana_alto - 150 - self.alto:
            self.y = Ventana_alto - 150 - self.alto
            self.velocidad_y = 0
            self.en_el_suelo = True
            self.salto_doble = False
    
    def saltar(self):
        if self.en_el_suelo:
            self.velocidad_y = Fuerza_Salto
            self.saltando = True
            self.en_el_suelo = False
            self.estado = 'saltando'
            
    def disparar(self):
        if self.balas > 0 and self.disparo:
            self.balas -= 1
            self.disparo = False
            self.no_disparo = 10
            
            bala = {
                'x' : self.x + self.ancho,
                'y' : self.y + self.alto//2 - Balas['Alto']//2,
                'ancho' : Balas['Ancho'],
                'alto' : Balas['Alto'],
                'velocidad' : Balas['Velocidad'],
                'color': Colores['Bala']
                }
            
            if not self.mira_a_derecha:
                bala['x'] = self.x - Balas['Ancho']
                bala['velocidad'] = -Balas['Velocidad']
            
            return bala
        return None
            
    def actualizar_animacion(self):
        #Actualizar animacion del personaje principal
        self.animacion_tiempo += 1
        if self.animacion_tiempo >= self.animacion_velocidad:
            self.animacion_frame = (self.animacion_frame + 1) % 4
            self.animacion_tiempo = 0
            
    def actualizar_invencibilidad(self):
        #Acutalizamos el estado invencible del personaje principal
        if self.invencible:
            self.tiempo_invencible -= 1
            if self.tiempo_invencible <= 0:
                self.invencible = False
    
    def dibujar(self,pantalla):
        #Dibujamos al personaje principal
        color_cuerpo = Colores['Jugador']
        if self.invencible and self.tiempo_invencible % 10 < 5:
            color_cuerpo = (255,255,255)
            
        #Cuerpo del personaje principal
        pygame.draw.rect(pantalla, color_cuerpo, self.rect)
        
        #Cabeza
        cabeza_rect = pygame.Rect(self.x + 10, self.y, self.ancho - 20, 25)
        pygame.draw.rect(pantalla, Colores['Jugador_piel'], cabeza_rect)
        
        #Ojos
        ojo_offset = 0
        if self.estado == 'corriendo':
            ojo_offset = math.sin(self.animacion_frame * 0.8) * 2
        ojo_izquierdo = (self.x + 15 + ojo_offset, self.y + 10)
        ojo_derecho = (self.x + self.ancho -15 + ojo_offset, self.y + 10)
        pygame.draw.circle(pantalla, (0,0,0), ojo_izquierdo, 4)
        pygame.draw.circle(pantalla, (0,0,0), ojo_derecho, 4)
        
        #Pupilas
        direccion_offset = 2 if self.mira_a_derecha else -2
        pygame.draw.circle(pantalla, (255,255,255), (ojo_izquierdo[0] + direccion_offset, ojo_izquierdo[1]), 2)
        pygame.draw.circle(pantalla, (255,255,255), (ojo_derecho[0] + direccion_offset,ojo_derecho[1]), 2)
        
        #Brazos
        brazo_offset = 0
        if self.estado == 'corriendo':
            brazo_offset = math.sin(self.animacion_frame * 0.8) * 15
        pygame.draw.line(pantalla, color_cuerpo, (self.x + 5,self.y + 30), (self.x - 10 - brazo_offset, self.y + 40),8)
        pygame.draw.line(pantalla, color_cuerpo, (self.x + self.ancho - 5,self.y + 30), (self.x + self.ancho + 10 + brazo_offset, self.y + 40),8)
    
        #Piernas
        pierna_offset = 0
        if self.estado == 'corriendo':
            pierna_offset = math.sin(self.animacion_frame * 0.8) * 10
        pygame.draw.line(pantalla, Colores['Jugador_tipo'], (self.x + 10, self.y + self.alto -10), (self.x + 5 - pierna_offset, self.y + self.alto +20), 10)
        pygame.draw.line(pantalla, Colores['Jugador_tipo'], (self.x + self.ancho - 10, self.y + self.alto -10),(self.x + self.ancho - 5 + pierna_offset, self.y + self.alto +20), 10)
        
        #Botones
        pygame.draw.circle(pantalla, Colores['Jugador_accesorios'], (self.x + self.ancho//2, self.y + 40), 4)
        
        #Indicador de balas
        if self.balas > 0:
            pygame.draw.circle(pantalla, Colores['Bala'], (self.x + self.ancho//2, self.y - 10), 5)
        
    def recibir_daño(self):
        #Daño que se hace al personaje principal
        if not self.invencible:
            self.vidas -= 1
            self.invencible = True
            self.tiempo_invencible = Config_Jugador['Tiempo invencible']
            
            #Cuando recibe daño se echa para atras
            self.velocidad_x = -5
            self.velocidad_y = -10
            
            if self.vidas <= 0:
                self.morir()
            return True
        return False
    
    def morir(self):
        #Muerte del personaje principal
        self.muerto = True
        self.velocidad_y = -15
        
    def recolectar_moneda(self):
        #Monedas que consigue personaje pricipal
        self.monedas += 1
        self.puntuacion += 50
        #100 monedas = 1 vida
        if self.monedas % 100 == 0:
            self.vidas = min(self.vidas + 1, 5)
    
    def recargar_balas(self, cantidad):
        #Recarga de balas del personaje principal
        self.balas = min(self.balas + cantidad, Balas['Maximo_Balas'])
        