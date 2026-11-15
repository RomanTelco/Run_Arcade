# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 21:45:36 2026

@author: Neo-PC
"""


#Motor visual del juego

import pygame

#Color del contorno
CONTORNO = (24,24,38)

#Efecto de pantalla antigua
EFECTO_CRT = True

_cache_sprites = {}
_cache_brillos = {}
_cache_crt = {}

def sombrear(color, factor):
    return tuple(max(0, min(255, int(c * factor))) for c in color)

def mezclar(color_a, color_b, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(color_a, color_b))

def _convertir(superficie):
    if pygame.display.get_surface() is not None:
        return superficie.convert_alpha()
    return superficie

def _procesar(grande, factor, contorno, blanco, volteo):
    ancho, alto = grande.get_size()
    pequeño = pygame.transform.smoothscale(grande, (ancho // factor, alto // factor))
    mascara = pygame.mask.from_surface(pequeño, 110)
    
    if blanco:
        limpio = mascara.to_surface(setcolor = (255,255,255,255), unsetcolor = (0,0,0,0))
    else:
        limpio = mascara.to_surface(setsurface = pequeño, unsetcolor = (0,0,0,0))
        opaco = mascara.to_surface(setcolor = (0,0,0,255), unsetcolor = (0,0,0,0))
        limpio.blit(opaco, (0,0), special_flags = pygame.BLEND_RGBA_MAX)
        borde_luz = mascara.copy()
        borde_luz.erase(mascara, (1,1))
        limpio.blit(borde_luz.to_surface(setcolor = (255,255,255,70), unsetcolor = (0,0,0,0)), (0,0))
        borde_sombra = mascara.copy()
        borde_sombra.erase(mascara, (-1, -1))
        limpio.blit(borde_sombra.to_surface(setcolor = (0,0,0,70), unsetcolor = (0,0,0,0)), (0,0))
    
    silueta = mascara.to_surface(setcolor = tuple(contorno) + (255,), unsetcolor = (0,0,0,0))
    ancho_p, alto_p = pequeño.get_size()
    final = pygame.Surface((ancho_p + 2, alto_p + 2), pygame.SRCALPHA)
    for dx in (0,1,2):
        for dy in (0,1,2):
            if dx != 1 or dy!= 1:
                final.blit(silueta, (dx,dy))
    final.blit(limpio, (1,1))
    final = pygame.transform.scale(final, ((ancho_p + 2) * factor, (alto_p + 2) * factor))
    if volteo:
        final = pygame.transform.flip(final, True, False)
    return _convertir(final)

def crear_sprite(ancho, alto, dibujar, factor = 2, margen = 16, contorno = CONTORNO, blanco = False, volteo = False):
    m = ((margen + factor - 1) // factor) * factor
    w = ancho + 2 * m
    h = alto + 2 * m
    w += (-w) % factor
    h += (-h) % factor
    grande = pygame.Surface((w, h), pygame.SRCALPHA)
    dibujar(grande, m, m)
    sprite = _procesar(grande, factor, contorno, blanco, volteo)
    off_y = m + factor
    if volteo:
        off_x = sprite.get_width() - (m + factor) - ancho
    else:
        off_x = m + factor
    return sprite, off_x, off_y

def sprite_cacheado(clave, ancho, alto, dibujar, **opciones):
    resultado = _cache_sprites.get(clave)
    if resultado is None:
        if len(_cache_sprites) > 500:
            _cache_sprites.clear()
        resultado = crear_sprite(ancho, alto, dibujar, **opciones)
        _cache_sprites[clave] = resultado
    return resultado

def resplandor(pantalla, x, y, radio, color, intensidad = 1.0):
    radio = int(radio)
    if radio < 3:
        return
    clave = (radio, tuple(color), round(intensidad, 1))
    superficie = _cache_brillos.get(clave)
    if superficie is None:
        if len(_cache_brillos) > 300:
            _cache_brillos.clear()
        superficie = pygame.Surface((radio * 2, radio * 2))
        superficie.fill((0,0,0))
        pasos = 12
        for i in range(pasos, 0, -1):
            t = i / pasos
            k = (1 - t) ** 1.4 * intensidad
            col = (min(255, int(color[0] * k)), min(255, int(color[1] * k)), min(255, int(color[2] * k)))
            pygame.draw.circle(superficie, col, (radio, radio), max(1, int(radio * t)))
        _cache_brillos[clave] = superficie
    pantalla.blit(superficie, (int(x) - radio, int(y) - radio), special_flags = pygame.BLEND_RGB_ADD)

def sombra_suelo(pantalla, centro_x, suelo_y, ancho, alpha = 90):
    ancho = int(ancho) // 4 * 4
    alpha = int(alpha) // 10 * 10
    if ancho < 8 or alpha <= 0:
        return
    clave = ('sombra', ancho, alpha)
    superficie = _cache_brillos.get(clave)
    if superficie is None:
        alto = max(6, ancho // 5)
        superficie = pygame.Surface((ancho, alto), pygame.SRCALPHA)
        pygame.draw.ellipse(superficie, (0,0,0, alpha), superficie.get_rect())
        _cache_brillos[clave] = superficie
    pantalla.blit(superficie, (int(centro_x - ancho / 2), int(suelo_y - superficie.get_height() / 2)))
    
def texto_contorno(pantalla, fuente, texto, x, y, color, contorno = (0,0,0), grosor = 2, centrado = True):
    base = fuente.render(texto, True, color)
    borde = fuente.render(texto, True, contorno)
    bx = x - base.get_width() // 2 if centrado else x
    for dx in range(-grosor, grosor + 1):
        for dy in range(-grosor, grosor + 1):
            if dx or dy:
                pantalla.blit(borde, (bx + dx, y + dy))
    pantalla.blit(base, (bx, y))
    
def aplicar_crt(pantalla):
    if not EFECTO_CRT:
        return
    tam = pantalla.get_size()
    capa = _cache_crt.get(tam)
    if capa is None:
        ancho, alto = tam
        capa = pygame.Surface(tam, pygame.SRCALPHA)
        for y in range(0, alto, 3):
            pygame.draw.line(capa, (0,0,0,26), (0, y), (ancho, y))
        for i in  range(36):
            a = int(110 * (1- i / 36) ** 2)
            pygame.draw.rect(capa, (0,0,0,a), (i,i, ancho - 2 * i, alto - 2 * i), 1)
        capa = _convertir(capa)
        _cache_crt[tam] = capa
    pantalla.blit(capa, (0,0))

        
    