# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 19:41:23 2026

@author: Neo-PC
"""

#Dibujos arcade de los personajes del juego
import math
import pygame
from config import *
from arte import crear_sprite, sprite_cacheado, resplandor, sombra_suelo, sombrear

SUELO_Y = Ventana_alto - 150
CHAQUETA = (226,52,62)
PALETAS_ESTRELLA = [(0,200,255), (120,255,110), (255,225,60), (255,120,220), (255,150,50), (190,120,255)]
PALETAS = [CHAQUETA] + PALETAS_ESTRELLA

#Jugador
def _cuerpo_jugador(s, ox, oy, estado, f, chaqueta):
    ch = chaqueta
    ch_osc = sombrear(ch, 0.68)
    ch_cla = sombrear(ch, 1.3)
    piel = (255,214,168)
    pant = (58,80,180)
    pant_osc = (38,54,130)
    bota = (74,46,52)
    bota_cla = (122,78,80)
    amar = (255,214,64)
    amar_osc = (255,150,30)
    blanco = (244,244,252)
    
    #Pose del jugador
    if estado == 'correr':
        bob = -2 if f % 2 == 1 else 0
        fase = f * math.pi / 2
        a_dx = math.sin(fase) * 9
        a_lev = max(0.0, math.cos(fase)) * 7
        b_dx = -a_dx
        b_lev = max(0.0, -math.cos(fase)) * 7
        mano = (11 - math.sin(fase) * 6, 52)
        cola = [(10,31), (10,38), (-6, 40 + (3 if f % 2 else 0)), (-12,35), (-4,33)]
    elif estado == 'salto':
        bob = 0
        a_dx, a_lev, b_dx, b_lev = 7, 8, -6, 2
        mano = (2,26)
        cola = [(10,31), (10,37), (4,52), (-1,46)]
    elif estado == 'caida':
        bob = 0
        a_dx, a_lev, b_dx, b_lev = 5, 3, -5, 0
        mano = (3,30)
        cola = [(10,31), (10,37), (-4,26), (-10,20)]
    else:
        bob = -1 if f == 1 else 0
        a_dx, a_lev, b_dx, b_lev = 0, 0, 0, 0
        mano = (11,52)
        cola = [(10,31), (10,38), (2,48), (-3,43)]
    
    #Pierna del jugador
    def pierna(hx, dx, lev, color):
        pie = 80 - lev
        pygame.draw.line(s, color, (ox + hx, oy + 58), (ox + hx + dx, oy + pie - 8), 11)
        pygame.draw.rect(s, bota, (ox + hx + dx - 7, oy + pie - 10, 18, 10), border_radius=3)
        pygame.draw.rect(s, bota_cla, (ox + hx + dx -6, oy + pie - 10, 16, 3), border_radius=1)
        pygame.draw.rect(s, (40,28,34), (ox + hx + dx - 7, oy + pie - 3, 18, 3))
        
    #Pierna de atras y brazo de atras
    pierna(14, b_dx, b_lev, pant_osc)
    pygame.draw.line(s, ch_osc, (ox + 11, oy + 35 + bob), (ox + mano[0], oy + mano[1] + bob), 8)
    pygame.draw.circle(s, blanco, (int(ox + mano[0]), int(oy + mano[1] + bob)), 5)
    
    #Pierna de delante
    pierna(26, a_dx, a_lev, pant)
    
    #Torso
    pygame.draw.rect(s, ch, (ox + 6, oy + 28 + bob, 28, 33), border_radius=7)
    pygame.draw.rect(s, ch_cla, (ox + 9, oy + 32 + bob, 4, 18), border_radius=2)
    pygame.draw.rect(s, ch_osc, (ox + 28, oy + 33 + bob, 5, 24), border_radius=2)
    rayo = [(22,34), (15,43), (20,43), (17,52), (26,40), (21, 40)]
    pygame.draw.polygon(s, amar, [(ox + px, oy + py + bob) for px, py in rayo])
    pygame.draw.rect(s, (58, 48, 70), (ox + 6, oy + 54 + bob, 28, 6))
    pygame.draw.rect(s, amar, (ox + 17, oy + 54 + bob, 7, 6))
    
    #Cola de la bufanda
    pygame.draw.polygon(s, amar_osc, [(ox + px, oy + py + bob) for px, py in cola])
    
    #Cabeza
    pygame.draw.circle(s, piel, (ox + 20, oy + 17 + bob), 14)
    for ex in (14,24):
        pygame.draw.ellipse(s, (255,255,255), (ox + ex, oy + 18 + bob, 8, 9))
        pygame.draw.circle(s, (20,20,40), (ox + ex + 5, oy + 23 + bob), 3)
    pygame.draw.line(s, (170, 70, 70), (ox + 25, oy + 29 + bob), (ox + 30, oy + 28 + bob),2)
    
    #Gorra con visera
    pygame.draw.circle(s, ch, (ox + 20, oy + 15 + bob), 15, draw_top_left=True, draw_top_right=True)
    pygame.draw.rect(s, ch_osc, (ox + 5, oy + 12 + bob, 30, 4))
    pygame.draw.polygon(s, ch_osc, [(ox + 24, oy + 12 + bob), (ox + 41, oy + 13 + bob), (ox + 40, oy + 17 + bob), (ox + 24, oy + 16 + bob)])
    pygame.draw.circle(s, amar, (ox + 20, oy + 7 + bob), 3)
    
    #Bufanda
    pygame.draw.rect(s, amar, (ox + 7, oy + 30 + bob, 26, 6), border_radius=3)
        
def _brazo_arma(s, ox, oy, chaqueta, con_balas):
    #Centro de la superficie es el hombro
    cx = ox + 55
    cy = oy + 20
    ch = chaqueta
    ch_osc = sombrear(ch, 0.68)
    acero = (98,106,132)
    acero_cla = (160,170,196)
    acero_osc = (60,64,86)
    energia = (90,240,255) if con_balas else(96,96,110)
    
    pygame.draw.rect(s, ch, (cx - 4, cy -6, 24, 12), border_radius=5)
    pygame.draw.rect(s, ch_osc, (cx - 4, cy + 1, 24, 5), border_radius=3)
    pygame.draw.rect(s, acero_osc, (cx + 16, cy + 3, 9, 12), border_radius=2)
    pygame.draw.rect(s, acero, (cx + 14, cy - 9, 28, 15), border_radius=4)
    pygame.draw.rect(s, acero_cla, (cx + 15, cy - 9, 26, 4), border_radius=2)
    pygame.draw.rect(s, acero, (cx + 38, cy - 6, 12, 9), border_radius=2)
    pygame.draw.rect(s, (255,200,60) if con_balas else (110,110,120), (cx + 48, cy - 7, 5, 11), border_radius=2)
    pygame.draw.circle(s, energia, (cx + 27, cy - 1), 3)
    pygame.draw.circle(s, (244,244,252), (cx + 20, cy + 5), 6)
    
def dibujar_jugador(pantalla, j):
    ahora = pygame.time.get_ticks()
    centro_x = j.x + j.ancho / 2
    #Sombra en el suelo
    altura = max(0, SUELO_Y - (j.y + j.alto))
    sombra_suelo(pantalla, centro_x, SUELO_Y, max(16, 46 - altura * 0.12), max(30, 100 - altura * 0.2))
    
    moneda = j.invencible and j.invencible_por_moneda
    daño = j.invencible and not j.invencible_por_moneda
    
    #Parpadeo al recibir daño
    if daño and not j.muerto and (j.tiempo_invencible // 4) % 2 == 0:
        return
    
    #Color de la chaqueta
    tinte = 0
    if moneda:
        if j.tiempo_invencible < 120 and (j.tiempo_invencible // 5) % 2 == 0:
            tinte = 0
        else:
            tinte = 1 + (ahora // 90) % len(PALETAS_ESTRELLA)
    
    #Estado de la animacion
    if not j.en_el_suelo:
        estado = 'salto' if j.velocidad_y < 0 else 'caida'
        frame = 0
    elif abs(j.velocidad_x) > 0.8:
        estado = 'correr'
        frame = (ahora // 85) % 4
    else:
        estado = 'quieto'
        frame = (ahora // 450) % 2
        
    volteo = not j.mira_a_derecha
    
    #Aura al coger la moneda de invencibilidad
    if moneda:
        color = PALETAS[tinte] if tinte else (255,255,255)
        resplandor(pantalla, centro_x, j.y + j.alto / 2, 75, color, 0.8)
        for k in range(4):
            a = ahora * 0.006 + k * math.pi / 2
            resplandor(pantalla, centro_x + math.cos(a) * 34, j.y + 40 + math.sin(a) * 46, 10, color, 0.9)
    
    #Cuerpo
    chaqueta = PALETAS[tinte]
    sprite, ox, oy = sprite_cacheado(('jugador', estado, frame, tinte, volteo),j.ancho, j.alto, lambda s, x, y: _cuerpo_jugador(s, x, y, estado, frame, chaqueta), factor = 2, margen = 24, volteo = volteo)
    pantalla.blit(sprite, (int(j.x) - ox, int(j.y) - oy))
    
    #Brazo con el arma
    con_balas = j.balas > 0
    brazo, _, _ = sprite_cacheado(('brazo', tinte, con_balas), 110, 40, lambda s, x, y: _brazo_arma(s, x, y, chaqueta, con_balas), factor = 2, margen = 4)
    angulo = j.angulo_apuntado
    if math.cos(angulo) < 0:
        brazo = pygame.transform.flip(brazo, False, True)
    brazo = pygame.transform.rotate(brazo, -math.degrees(angulo))
    dx=math.cos(angulo)
    dy=math.sin(angulo)
    retroceso = 3 if j.tiempo_entre_disparo >= j.velocidad_disparo - 2 else 0
    hombro = (int(j.x + 20 - dx * retroceso), int(j.y + 36 - dy * retroceso))
    pantalla.blit(brazo, brazo.get_rect(center = hombro))
    
    #Fogonazo al disparar
    if retroceso:
        resplandor(pantalla, hombro[0] + dx * 52, hombro[1] + dy * 52, 28, (255,220,90), 1.0)

#Enemigos
def _bloque(s, ox, oy, w, h, pulso):
    acero = (112, 118, 138)
    claro = (172, 180, 200)
    oscuro = (66, 70, 90)
    panel = (88,94,114)
    
    pygame.draw.rect(s, acero, (ox, oy, w, h), border_radius=6)
    pygame.draw.rect(s, oscuro, (ox, oy, w, h), 3, border_radius=6)
    pygame.draw.rect(s, panel, (ox + 9, oy + 9, w - 18, h - 18), border_radius=4)
    pygame.draw.rect(s, claro, (ox + 9, oy + 9, w - 18, h - 18), 2, border_radius=4)
    
    #Tornillos
    for rx, ry in ((6,6), (w - 6, 6), (6, h - 6), (w - 6, h - 6)):
        pygame.draw.circle(s, claro, (ox + rx, oy + ry), 3)
        pygame.draw.circle(s, oscuro, (ox + rx, oy + ry), 3, 1)
    
    #Ojo de peligro 
    ojo = pygame.Rect(ox + 14, oy + 16, w - 28, 10)
    pygame.draw.rect(s, (25,15,30), ojo, border_radius=4)
    color_ojo = (255, 60, 50) if pulso else (255,150,60)
    pygame.draw.rect(s, color_ojo, (ojo.x + 3, ojo.y + 2, ojo.w - 6, 6), border_radius=2)
    pygame.draw.rect(s, (255,240,200), (ojo.centerx - 3, ojo.y + 3, 6, 3))
    
    #Franja de peligro
    franja = pygame.Rect(ox + 9, oy + h - 22, w - 18, 10)
    pygame.draw.rect(s, (30,30,40), franja)
    s.set_clip(franja)
    for i in range(-1, 7):
        x0= franja.x + i * 10
        pygame.draw.polygon(s, (255, 206, 50), [(x0, franja.bottom), (x0 + 5, franja.bottom), (x0 + 10, franja.top), (x0 + 5, franja.top)])
    s.set_clip(None)
    
    #Grietas
    pygame.draw.line(s, oscuro, (ox + 40, oy + 11), (ox + 46, oy + 19), 2)
    pygame.draw.line(s, oscuro, (ox + 46, oy + 19), (ox + 43, oy + 27), 2)

def _andante(s, ox, oy, w, h, f):
    cuerpo = (226, 62, 66)
    osc = (150, 30, 48)
    barriga = (255,176,150)
    cuerno = (240,230,200)
    bob = (0,-2,0,-2)[f]
    fase = f * math.pi / 2
    paso = math.sin(fase) * 5
    
    #Pies
    for signo, px in ((1,15), (-1,35)):
        lev = max(0.0, math.cos(fase) * signo) * 4
        pygame.draw.ellipse(s, (74,34,56), (ox + px + paso * signo - 8, oy + h -11 - lev, 18, 11))
        
    #Manos
    pygame.draw.circle(s, osc, (int(ox + 1 + paso * 0.6), oy + 44 + bob), 6)
    pygame.draw.circle(s, osc, (int(ox + w - 1 - paso * 0.6), oy + 44 + bob), 6)
    
    #Cuernos
    pygame.draw.polygon(s, cuerno, [(ox + 8, oy + 24 + bob), (ox + 10, oy + 4 + bob), (ox + 19, oy + 19 + bob)])
    pygame.draw.polygon(s, cuerno, [(ox + w - 8, oy + 24 + bob), (ox + w - 10, oy + 4 + bob), (ox + w - 19, oy + 19 + bob)])
    
    #Cuerpo
    pygame.draw.ellipse(s, osc, (ox + 2, oy + 16 + bob, w - 4, h - 24))
    pygame.draw.ellipse(s, cuerpo, (ox + 4, oy + 16 + bob, w - 10, h - 30))
    pygame.draw.ellipse(s, barriga, (ox + 13, oy + 36 + bob, w - 26, 22))
    
    #Cara enfadada
    for ex in (17, 33):
        pygame.draw.circle(s, (255,255,255), (ox + ex, oy + 31 + bob), 7)
        pygame.draw.circle(s, (20,10,20), (ox + ex + 2, oy + 32 + bob), 3)
    pygame.draw.line(s, (60,10,30), (ox + 9, oy + 21 + bob), (ox + 22, oy + 27 + bob), 4)
    pygame.draw.line(s, (60,10,30), (ox + w - 9, oy + 21 + bob), (ox + w - 22, oy + 27 + bob), 4)
    pygame.draw.ellipse(s, (60,10,30), (ox + 15, oy + 42 + bob, 20, 10))
    for i in range(3):
        x0 = ox + 18 + i * 6
        pygame.draw.polygon(s, (255,255,255), [(x0, oy + 43 + bob), (x0 + 5, oy + 43 + bob), (x0 + 2, oy + 49 + bob)])
        
def _volador(s, ox, oy, w, h, f):
    bob = (0, -2, 0, 2)[f]
    morado = (160,70,225)
    osc = (100, 40, 170)
    claro = (205,140,255)
    llama = 8 + (f%2) * 4
    
    #Propulsor
    pygame.draw.polygon(s, (255,120,20), [(ox + 15, oy + 34 + bob), (ox + 22, oy + 40 + bob + llama), (ox + 30, oy + 34 + bob)])
    pygame.draw.polygon(s, (255,255,90), [(ox + 18, oy + 34 + bob), (ox + 22, oy + 36 + bob + llama // 2), (ox + 27, oy + 34 + bob)])
    
    #Aletas
    pygame.draw.polygon(s, osc, [(ox + 3, oy + 22 + bob), (ox - 6, oy + 34 + bob), (ox + 12, oy + 30 + bob)])
    pygame.draw.polygon(s, osc, [(ox + w - 3, oy + 22 + bob), (ox + w + 6, oy + 34 + bob), (ox + w - 12, oy + 30 + bob)])
    
    #Cupula con alien
    pygame.draw.ellipse(s, (170,235,255), (ox + 11, oy + 3 + bob, 23, 22))
    pygame.draw.ellipse(s, (95,170,215), (ox + 11, oy + 3 + bob, 23, 22), 2)
    pygame.draw.ellipse(s, (120,230,110), (ox + 17, oy + 11 + bob, 12, 12))
    pygame.draw.circle(s, (255,255,255), (ox + 22, oy + 16 + bob), 4)
    pygame.draw.circle(s, (20,20,30), (ox + 21, oy + 16 + bob), 2)
    
    #Platillo
    pygame.draw.ellipse(s, morado, (ox, oy + 18 + bob, w, 18))
    pygame.draw.ellipse(s, claro, (ox + 5, oy + 20 + bob, w - 10, 6))
    for i in range(5):
        color = (255, 230, 80) if (i+f) % 2 == 0 else (255,90,120)
        pygame.draw.circle(s, color, (ox + 8 + i * 7, oy + 30 + bob), 2)
        
def _sombra_enemigo(pantalla, o, factor_ancho, alpha):
    distancia = max(0, SUELO_Y - (o.y + o.alto))
    ancho = o.ancho * factor_ancho * max(0.35, 1 - distancia / 600)
    sombra_suelo(pantalla, o.x + o.ancho / 2, SUELO_Y, ancho, alpha * max(0.3, 1 - distancia / 500))
    
def dibujar_enemigo(pantalla, o):
    destello = o.daño_tiempo > 0 and o.daño_tiempo % 4 < 2
    f = o.animacion_frame % 4
    
    if o.tipo == 'Bloque':
        _sombra_enemigo(pantalla, o, 1.05, 90)
        pulso = f // 2
        sprite, ox, oy = sprite_cacheado(('bloque', pulso), o.ancho, o.alto, lambda s, x, y: _bloque(s, x, y, o.ancho, o.alto, pulso), factor=2, margen=8)
        pantalla.blit(sprite, (int(o.x) - ox, int(o.y) - oy))
    elif o.tipo == 'Andante':
        _sombra_enemigo(pantalla, o, 0.95, 90)
        volteo = o.velocidad_x < 0
        sprite, ox, oy = sprite_cacheado(('andante', f, volteo, destello), o.ancho, o.alto, lambda s, x, y: _andante(s, x, y, o.ancho, o.alto, f), factor=2, margen=10, volteo = volteo, blanco=destello)
        pantalla.blit(sprite, (int(o.x) - ox, int(o.y) - oy))
    else:
        _sombra_enemigo(pantalla, o, 0.8, 50)
        sprite, ox, oy = sprite_cacheado(('volador', f, destello), o.ancho, o.alto, lambda s, x, y: _volador(s, x, y, o.ancho, o.alto, f), factor=2, margen=16, blanco= destello)
        pantalla.blit(sprite, (int(o.x) - ox, int(o.y) - oy))
        resplandor(pantalla, o.x + o.ancho / 2, o.y + o.alto + 6, 24, (255, 140,30), 0.6)
    
    
    
        

