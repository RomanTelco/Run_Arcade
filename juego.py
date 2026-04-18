# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 15:12:53 2026

@author: Neo-PC
"""

import pygame
import sys
from config import *
from jugador import Jugador
from mundo import Mundo
from nivel import Nivel

#Fichero con las funciones principales del juego
class Juego:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        
        #Ventana principal del juego
        self.pantalla = pygame.display.set_mode((Ventana_ancho, Ventana_alto))
        pygame.display.set_caption("Run Arcade")
        
        #FPS del juego
        self.reloj = pygame.time.Clock()
        
        #Estados principales del juego
        self.estado = 'MENU'
        self.nivel_actual = 0
        self.puntuacion_total = 0
        
        #Elementos del juego
        self.jugador = None
        self.mundo = None
        self.nivel = None
        self.balas = []
        
        #Fuentes del juego
        self.fuente_grande = pygame.font.Font(None,72)
        self.fuente_media = pygame.font.Font(None, 48)
        self.fuente_pequeña = pygame.font.Font(None, 36)
        self.fuente_muy_pequeña = pygame.font.Font(None, 24)
        
        #Inicializacion del juego
        self.inicializar_juego()
        
    def inicializar_juego(self):
        #Creacion del mundo del juego
        self.mundo = Mundo(self.nivel_actual)
        
        #Creacion del jugador
        suelo_y = Ventana_alto - 150
        self.jugador = Jugador(100, suelo_y - Config_Jugador['Alto'])
        
        #Creacion del nivel
        self.nivel = Nivel(self.nivel_actual, self.mundo)
        
        #Renovar en pantalla el numero de balas
        self.balas = []
        
    def manejar_eventos(self):
        #Eventos del juego
        mouse_click = False
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if evento.type == pygame.KEYDOWN:
                #Menu del juego
                if self.estado == 'MENU':
                    if evento.key == pygame.K_RETURN:
                        self.estado = 'JUGANDO'
                    elif evento.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                
                #Durante el juego
                elif self.estado == 'JUGANDO':
                    if evento.key == pygame.K_p:
                        self.estado = 'PAUSA'
                    elif evento.key == pygame.K_ESCAPE:
                        self.estado = 'MENU'
                
                #Juego completado o GAME OVER
                elif self.estado in ['GAME OVER', 'COMPLETADO']:
                    if evento.key == pygame.K_r:
                        self.nivel_actual = 0
                        self.puntuacion_total = 0
                        self.inicializar_juego()
                        self.estado = 'MENU'
            
            #Click para el raton del disparo
            if evento.type == pygame.MOUSEBUTTONDOWN and self.estado == 'JUGANDO':
                if evento.button == 1:
                    mouse_click = True
        return mouse_click
    
    def actualizar(self, mouse_click):
        #Actualizacion del estado del jugador
        if self.estado != 'JUGANDO':
            return
        
        #Obtancion de las teclas presionadas
        teclas = pygame.key.get_pressed()
        
        #Actualizacion del jugador y obtancion de nuevas balas
        nuevas_balas = self.jugador.actualizar(teclas, mouse_click)
        self.balas.extend(nuevas_balas)
        
        #Actualizacion dle mundo
        self.mundo.actualizar()
        
        #Actualizacion del nivel
        self.nivel.actualizar(self.jugador, self.balas)
        
        #Actualizacion de las balas
        for bala in self.balas[:]:
            bala['x'] += bala['velocidad']
            if bala['x'] < -100 or bala['x'] > Ventana_ancho + 100:
                self.balas.remove(bala)
                
        #Verificacion del estado del jugador : vivo o muerto
        if self.jugador.muerto:
            self.estado = 'GAME OVER'
            self.puntuacion_total += self.jugador.puntuacion
        
        #Verificacion del estado del nivel: completado o no
        elif self.nivel.completado:
            self.puntuacion_total += self.jugador.puntuacion
            
            #Siguiente nivel
            if self.nivel_actual < len(Niveles) - 1:
                self.nivel_actual += 1
                self.inicializar_juego()
                self.estado = 'JUGANDO'
            else:
                self.estado = 'COMPLETADO'
       
    def dibujar(self):
        #Lo que aparece en pantalla
        if self.estado == 'MENU':
            self.dibujar_menu()
        elif self.estado == 'JUGANDO':
            self.dibujar_juego()
        elif self.estado == 'PAUSA':
            self.dibujar_juego()
            self.dibujar_pausa()
        elif self.estado == 'GAME OVER':
            self.dibujar_juego()
            self.dibujar_game_over()
        elif self.estado == 'COMPLETADO':
            self.dibujar_juego()
            self.dibujar_completado()
        
        pygame.display.flip()
        
    def dibujar_menu(self):
        #Pantalla del menu principal
        
        #Fondo
        self.pantalla.fill(Colores['Cielo'])
        
        #Titulo
        titulo = self.fuente_grande.render("RUN ARCADE", True, Colores['Jugador'])
        sombra = self.fuente_grande.render("RUN ARCADE", True, Colores['Texto_sombra'])
        self.pantalla.blit(sombra, (Ventana_ancho//2 - titulo.get_width()//2 + 3, 103))
        self.pantalla.blit(titulo, (Ventana_ancho//2 - titulo.get_width()//2, 100))
        
        #Subtitulo
        subtitulo = self.fuente_media.render("Corre, Salta y Dispara", True, Colores['Texto'])
        self.pantalla.blit(subtitulo, (Ventana_ancho//2 - subtitulo.get_width()//2,180))
        
        #Controles
        controles = [
            "CONTROLES:",
            "<-- --> / A D: Moverse",
            "ESPACIO / W : Saltar",
            "DOBLE ESPACIO: Dobrle salto",
            "Click Izquierdo: Disparar",
            "P: Pausar juego",
            "ESC : Volver al Menu"
            ]
        
        for i, texto in enumerate(controles):
            render = self.fuente_pequeña.render(texto, True, Colores['Texto'])
            self.pantalla.blit(render, (Ventana_ancho//2 - render.get_width()//2, 250 + i * 35))
            
        #Instrucciones para comenzar
        comenzar = self.fuente_media.render("Presiona ENTER para comenzar", True, Colores['Jugador'])
        self.pantalla.blit(comenzar, (Ventana_ancho//2 - comenzar.get_width()//2,500))
        
        #Version
        version = self.fuente_muy_pequeña.render("4 Niveles de Aventura", True, (200,200,200))
        self.pantalla.blit(version, (Ventana_ancho//2 - version.get_width()//2, 580))
    
    def dibujar_juego(self):
        #Juego en progreso
        
        #Mundo
        self.mundo.dibujar(self.pantalla)
        
        #Nivel
        self.nivel.dibujar(self.pantalla)
        
        #Balas
        for bala in self.balas:
            pygame.draw.rect(self.pantalla, bala['color'], (bala['x'], bala['y'], bala['ancho'], bala['alto']))
            
        #Jugador
        self.jugador.dibujar(self.pantalla)
        
        #Interfaz
        self.dibujar_interfaz()
        
    def dibujar_interfaz(self):
        #Interfaz del usuario
        
        #Panel superior
        panel = pygame.Surface((Ventana_ancho, 80), pygame.SRCALPHA)
        panel.fill((0,0,0,128))
        self.pantalla.blit(panel,(0,0))
        
        #Vidas
        vidas_texto = self.fuente_pequeña.render(f"VIDAS: {self.jugador.vidas}", True, Colores['Barra_vida'])
        self.pantalla.blit(vidas_texto, (20,10))
        
        #Balas
        balas_texto = self.fuente_pequeña.render(f"BALAS: {self.jugador.balas}", True, Colores['Bala'])
        self.pantalla.blit(balas_texto, (20,45))
        
        #Puntos
        puntos_texto = self.fuente_pequeña.render(f"PUNTOS: {self.jugador.puntuacion}", True, Colores['Texto'])
        self.pantalla.blit(puntos_texto, (200, 10))
        
        #Monedas 
        monedas_texto = self.fuente_pequeña.render(f"MONEDAS: {self.jugador.monedas}", True, Colores['Moneda'])
        self.pantalla.blit(monedas_texto, (200, 45))
        
        #Nivel
        nivel_nombre = Niveles[self.nivel_actual]['Nombre']
        nivel_texto = self.fuente_pequeña.render(f"NIVEL: {nivel_nombre}", True, Colores['Texto'])
        self.pantalla.blit(nivel_texto, (Ventana_ancho - 300, 10))
        
        #Tiempo
        minutos = self.nivel.tiempo_restante // 60
        segundos = self.nivel.tiempo_restante % 60
        tiempo_texto = self.fuente_pequeña.render(f"TIEMPO: {minutos:02d}:{segundos:02d}", True, Colores['Texto'])
        self.pantalla.blit(tiempo_texto, (Ventana_ancho - 300, 45))
        
        #Barra de progreso
        barra_x = Ventana_ancho//2 - 100
        barra_y = 65
        barra_ancho = 200
        barra_alto = 10
        
        pygame.draw.rect(self.pantalla, (100,100,100), (barra_x, barra_y, barra_ancho, barra_alto), 2)
        
        relleno_ancho = int(barra_ancho * (self.mundo.progreso / 100))
        pygame.draw.rect(self.pantalla, Colores['Texto'], (barra_x, barra_y, relleno_ancho, barra_alto))
        
        pygame.draw.rect(self.pantalla, Colores['Texto'], (barra_x, barra_y, barra_ancho, barra_alto), 2)
        
        
        
    def dibujar_pausa(self):
        #Pausa del juego
        overlay = pygame.Surface((Ventana_ancho, Ventana_alto), pygame.SRCALPHA)
        overlay.fill((0,0,0,150))
        self.pantalla.blit(overlay, (0,0))
        
        pausa = self.fuente_grande.render("PAUSA", True, Colores['Texto'])
        self.pantalla.blit(pausa, (Ventana_ancho//2 - pausa.get_width()//2, Ventana_alto//2 - 50))
        
        continuar = self.fuente_media.render("Presiona P para continuar", True, Colores['Jugador'])
        self.pantalla.blit(continuar, (Ventana_ancho//2 - continuar.get_width()//2, Ventana_alto//2 + 30))
        
    def dibujar_game_over(self):
        #Game over
        overlay = pygame.Surface((Ventana_ancho, Ventana_alto), pygame.SRCALPHA)
        overlay.fill((0,0,0,200))
        self.pantalla.blit(overlay, (0,0))
        
        game_over = self.fuente_grande.render("GAME OVER", True, (255, 50, 50))
        self.pantalla.blit(game_over, (Ventana_ancho//2 - game_over.get_width()//2, Ventana_alto//2 - 80))
        
        puntos = self.fuente_media.render(f"PUNTUACION: {self.jugador.puntuacion}", True, Colores['Texto'])
        self.pantalla.blit(puntos, (Ventana_ancho//2 - puntos.get_width()//2, Ventana_alto//2 - 20))
        
        nivel = self.fuente_pequeña.render(f"NIVEL ALCANZADO: {self.nivel_actual + 1}", True, Colores['Texto'])
        self.pantalla.blit(nivel, (Ventana_ancho//2 - nivel.get_width()//2, Ventana_alto//2 + 20))
        
        reiniciar = self.fuente_pequeña.render("Presiona R para reiniciar", True, Colores['Texto'])
        self.pantalla.blit(reiniciar, (Ventana_ancho//2 - reiniciar.get_width()//2, Ventana_alto//2 + 80))
        
    def dibujar_completado(self):
        #Cuando el nivel se complete en el juego
        overlay = pygame.Surface((Ventana_ancho, Ventana_alto), pygame.SRCALPHA)
        overlay.fill((0,0,0,200))
        self.pantalla.blit(overlay, (0,0))
        
        completado = self.fuente_grande.render("JUEGO COMPLETADO", True, Colores['Moneda'])
        self.pantalla.blit(completado, (Ventana_ancho//2 - completado.get_width()//2, Ventana_alto//2 - 80))
        
        puntos = self.fuente_media.render(f"PUNTUACION TOTAL: {self.puntuacion_total}", True, Colores['Texto'])
        self.pantalla.blit(puntos, (Ventana_ancho//2 - puntos.get_width()//2, Ventana_alto//2 - 20))
        
        reiniciar = self.fuente_pequeña.render("Presiona R para jugar de nuevo", True, Colores['Texto'])
        self.pantalla.blit(reiniciar, (Ventana_ancho//2 - reiniciar.get_width()//2, Ventana_alto//2 + 40))
        
    def ejecutar(self):
        #Bucle principal
        while True:
            mouse_click = self.manejar_eventos()
            self.actualizar(mouse_click)
            self.dibujar()
            self.reloj.tick(FPS)
            
        
                    
                
                