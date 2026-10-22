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
Nombre de los integrantes: Nicolle Alvez, Raul Benitez, Alex Cardozo.
Descripcion breve: El juego trata de un zorro, que va cumpliendo objetivos hasta recuperar un cristal que se les fue robado a su aldea. Durante el transcurso se enfrentará a diversos enemigos e ira haciendo aliados.
Probema que resuelve: No resuelve ningun problema, es un sistema con fines recreativos.
Objetivo general: Busca entretener al publico.
Funcionalidades principales:
- Movilidad libre a travez del mapa.
- interaccion con los personajes
- toma de desiciones.
  ##ENTREGA NUMERO 4:

Archivos:
- fox_adventures.py: codigo del juego.
- web_app.py: parte web hecha con Flask.
- templates: paginas HTML.
- static: archivo CSS.
- fox_save.json: datos guardados de la partida. Se crea cuando guardo los cambios desde la web.

Para ejecutar el jueguito en otro dispositivo
Primero se instala las librerias desde la terminal:

python -m pip install -r requirements.txt


Para abrir el juego tambien lo hacemos por la terminal:

py fox_adventures.py

Para abrir la version de pagina web, hay que ejecutar este comando en el archivo web_app.py:

py web_app.py

Despues entrar desde el navegador a http://127.0.0.1:5000.

Lo que fuimos haciendo hasta ahora:
- Pagina de inicio con los datos de la partida.
- Formulario para cambiar la vida, pociones, cristales, mision y posicion.
- Listado de enemigos.
- Flask conecta las paginas y guarda los datos en JSON.

## A tener en cuenta
Esta parte web es un avance de la entrega 4. El juego de Pygame sigue funcionando aparte. Si cambio los datos desde la web, se guardan en el JSON, pero el juego no se controla desde el navegador.

Todavia falta probarlo bien y seguir conectando las funciones del juego.
