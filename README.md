main.py
def crear_personaje():

    nombre = input("\nIntroduce el nombre de tu personaje: ")

    if not nombre == "":
        nombre = "Aventurero/a"

    print(f"\nBienvenido, {nombre}!")
    pausar()

    return nombre



funciones.py
def pueblo(nombre):

    while True:

        print("\n" + "=" * 40)
        print("      PUEBLO DE FOX ")
        print("=" * 40)

        print(f"""
Te encuentras en el pueblo de Fox.

El lugar parece abandonado, las casas están en ruinas y el silencio es inquietante.

A lo lejos ves una pequeña taberna con una luz tenue en la ventana.
También hay un camino que lleva hacia el bosque"
""")
        
        print("Opciones:")
        print("1. Entrar en la taberna")
        print("2. Explorar el bosque")
        print("3. Revisar el mapa")
        print("4. Salir del juego")

        opcion = input("\n¿Qué deseas hacer?: ")


  
datos.py
import random


# ==========================
# FUNCIONES DE TEXTO
# RPG DE TEXTO
# ==========================



def mostrar_titulo():
    print("=" * 40)
    print("      FOX´S ADVENTURES")
    print("=" * 40)
    print("      RPG DE TEXTO")
    print("=" * 40)
    print("Bienvenido a la aventura. El objetivo es recuperar la gema robada en las ruinas")
    print("=" * 40)


def pausar():
    input("Presiona ENTER para continuar...")


def mostrar_historia(texto):
    print("\n" + "-" * 45)
    print(texto)
    print("-" * 45)


README.md
Nombre del proyecto: Fox"s adventures.
Nombre de los integrantes: Daiana Antonella Benitez, Nicolle Alvez, Raul Benitez.
Descripcion breve: El juego trata de un zorro, que va cumpliendo objetivos hasta recuperar un cristal que se les fue robado a su aldea. Durante el transcurso se enfrentará a diversos enemigos e ira haciendo aliados.
Probema que resuelve: No resuelve ningun problema, es un sistema con fines recreativos.
Objetivo general: Busca entretener al publico.
Funcionalidades principales:
- Movilidad libre a travez del mapa.
- interaccion con los personajes
- toma de desiciones.
