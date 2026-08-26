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
            'Tiempo_limite' : 50,
            'Enemigos' : {'Bloque':15, 'Andante':10, 'Volador':0},
            'Monedas':30,
            'Velocidad': -4,
            'Color_fondo': (135,206,235),
            'Dificultad': 'Principiante'
        },
        
        {
            #Nivel 1: Facil
            'Nombre' : 'Nivel 1 - Pradera',
            'Tiempo_limite' : 180,
            'Enemigos' : {'Bloque':10, 'Andante':15, 'Volador':5},
            'Monedas':40,
            'Velocidad': -5,
            'Color_fondo': (135,206,235),
            'Dificultad': 'Principiante'
        },
        
        {
            #Nivel 2: Intermedio
            'Nombre' : 'Nivel 2 - Bosque',
            'Tiempo_limite' : 220,
            'Enemigos' : {'Bloque':18, 'Andante':20, 'Volador':12},
            'Monedas':50,
            'Velocidad': -6,
            'Color_fondo': (100,180,100),
            'Dificultad': 'Intermedio'
        },
        
        {
            #Nivel 3: Dificil
            'Nombre' : 'Nivel 3 - Montaña',
            'Tiempo_limite' : 220,
            'Enemigos' : {'Bloque':30, 'Andante':25, 'Volador':20},
            'Monedas':60,
            'Velocidad': -7,
            'Color_fondo': (180,180,200),
            'Dificultad': 'Avanzado'
        },
        
        
        {
            #Nivel 4: Muy Dificil
            'Nombre' : 'Nivel 4 - Volcan',
            'Tiempo_limite' : 250,
            'Enemigos' : {'Bloque':25, 'Andante':30, 'Volador':25},
            'Monedas':70,
            'Velocidad': -8,
            'Color_fondo': (80,40,20),
            'Dificultad': 'Muy Dificl'
        },
        
        {
            #Nivel 5: Experto
            'Nombre' : 'Nivel 5 - Hielo',
            'Tiempo_limite' : 280,
            'Enemigos' : {'Bloque':20, 'Andante':35, 'Volador':30},
            'Monedas':80,
            'Velocidad': -8,
            'Color_fondo': (200,220,255),
            'Dificultad': 'Experto'
        },
        
        {
            #Nivel 6: General
            'Nombre' : 'Nivel 6 - Castillo Oscuro',
            'Tiempo_limite' : 300,
            'Enemigos' : {'Bloque':40, 'Andante':40, 'Volador':35},
            'Monedas':100,
            'Velocidad': -9,
            'Color_fondo': (40,40,60),
            'Dificultad': 'General'
        },
        
        
        {
            #Nivel 7: Leyenda
            'Nombre' : 'Nivel 7 - Mundo Final',
            'Tiempo_limite' : 350,
            'Enemigos' : {'Bloque':50, 'Andante':45, 'Volador':40},
            'Monedas':150,
            'Velocidad': -10,
            'Color_fondo': (20,20,40),
            'Dificultad': 'Leyenda'
        }
    ]

Balas = {
    
    'Velocidad' : 15,
    'Ancho' : 20,
    'Alto' : 5,
    'Maximo_Balas' : 30,
    'Recarga' : 10,
         }

