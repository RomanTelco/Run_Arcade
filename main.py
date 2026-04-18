# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 20:06:52 2026

@author: Neo-PC
"""

from juego import Juego

#Main
def main():
    print("=" * 50)
    print("Run Arcade")
    print("=" * 50)
    print("\n!Bienvenido a la aventura!")
    print("\nInstrucciones:")
    print("- Corre, salta y dispara a los enemigos")
    print("- Recolecta monedas para ganar puntos")
    print("\nControles:")
    print("- <-- --> / A D: Moverse")
    print("- ESPACIO / W: Saltar")
    print("- DOBLE ESPACIO: Doble salto")
    print("- CLIC IZQUIERDO: Disparar")
    print("- P: Pausar Juego")
    print("- R: Reiniciar")
    print("- ESC: Salir")
    print("\n" + "=" * 50)
    print("Presiona ENTER para comenzar")
    print("=" * 50)
    
    #Ejecucion del juego
    juego=Juego()
    juego.ejecutar()
    
if __name__ == "__main__":
    main()