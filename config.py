# -*- coding: utf-8 -*-
"""
Created on Mon Feb  2 19:18:53 2026

@author: Neo-PC
"""

#Parametros generales del videojuego Run Arcade
#Ventana Principal
Ventana_ancho = 1200
Ventana_alto = 700
FPS = 60

#Paleta de Colores para los objetos
Colores = {
    #Entorno
    'Cielo': (135,206,235), #Azul cielo
    'Nube' : (255,255,255), #Blanco
    'Montaña' : (180,180,180), #Gris
    'Arbusto' : (34,139,34), #Verde
    'Suelo' : (222,184,135), #Marron
    'Hierba' : (124,252,0), #Verde claro
    'Camino' : (139,69,19), #Marron oscuro
    
    #Personaje
    'Jugador' : (255,0,0), #Rojo
    'Jugador_tipo' : (0,100,0), #Verde
    'Jugador_piel' : (255, 205,148), #Color piel
    'Jugador_accesorios' : (255,255,0), #Amarillo
    
    #Enemigos
    'Bloque' : (100,100,100), #Gris
    'Andante' : (255,50,50), #Rojo
    'Volador' : (180,0,255), #Morado
    
    #Elementos del juego
    'Moneda' : (255,215,0),
    'Bala' : (255,255,0),
    
    #Interfaz
    'Texto' : (255,255,255),
    'Texto_sombra' : (0,0,0),
    'Barra_vida' : (0,255,0),
    }

#Fisica del juego
Gravedad = 0.8
Velocidad_juego = -5
Velocidad_maxima= 8
Aceleracion = 0.2
Friccion = 0.9
Fuerza_Salto = -15

#Parametros del jugador
Config_Jugador = {
    'Ancho' : 40,
    'Alto' : 80,
    'Vidas' : 3,
    'Balas' : 20,
    'Tiempo invencible' : 60,
    }

#Parametros de los enemigos
Enemigos = {
    'Bloque': {
        'Ancho' : 60,
        'Alto' : 60,
        'Velocidad' : 0,
        'Vida' : 999,
        'Puntos': 0,
        'Color' : Colores['Bloque'],
        'Tipo' : 'estatico',
        'Descripcion' : 'Bloque fijo - Hay que saltar por encima'        
        },
    
    'Andante': {
        'Ancho' : 50,
        'Alto' : 70,
        'Velocidad' : -3,
        'Vida' : 2,
        'Puntos': 100,
        'Color' : Colores['Andante'],
        'Tipo' : 'terrestre',
        'Descripcion' : 'Enemigo caminante - Saltar o disparar'  
        },
    
    'Volador': {
        'Ancho' : 45,
        'Alto' : 45,
        'Velocidad' : -4,
        'Vida' : 1,
        'Puntos':150,
        'Color' : Colores['Volador'],
        'Tipo' : 'aereo',
        'Descripcion' : 'Enemigo volador - Disrar al objetivo'  
        }
    }

Niveles = [
        {   
            #Tutorial
            'Nombre' : 'Tutorial',
            'Tiempo_limite' : 300,
            'Enemigos' : {'Bloque':15, 'Andante':5, 'Volador':0},
            'Monedas':30,
            'Velocidad': -4,
        },
        
        {
            #Nivel 1: Facil
            'Nombre' : 'Nivel 1',
            'Tiempo_limite' : 280,
            'Enemigos' : {'Bloque':10, 'Andante':10, 'Volador':5},
            'Monedas':40,
            'Velocidad': -5,
        },
        
        {
            #Nivel 2: Intermedio
            'Nombre' : 'Nivel 2',
            'Tiempo_limite' : 250,
            'Enemigos' : {'Bloque':8, 'Andante':8, 'Volador':12},
            'Monedas':50,
            'Velocidad': -6,
        },
        
        {
            #Nivel 3: Dificil
            'Nombre' : 'Nivel 3',
            'Tiempo_limite' : 220,
            'Enemigos' : {'Bloque':12, 'Andante':15, 'Volador':15},
            'Monedas':60,
            'Velocidad': -7,
        }
    ]

Balas = {
    
    'Velocidad' : 15,
    'Ancho' : 20,
    'Alto' : 5,
    'Maximo_Balas' : 30,
    'Recarga' : 10,
         }

