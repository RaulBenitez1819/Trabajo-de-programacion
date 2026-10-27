import json
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for


app = Flask(__name__)
app.secret_key = "fox-adventures-clave-local"

CARPETA_PROYECTO = Path(__file__).resolve().parent
ARCHIVO_PARTIDA = CARPETA_PROYECTO / "fox_save.json"


def partida_inicial():
    """Devuelve los valores que se usan si todavía no hay una partida guardada."""
    return {
        "version": 1,
        "player_x": 100,
        "hp": 100,
        "potions": 3,
        "crystals": 0,
        "quest": 0,
        "allies": [],
        "defeated": [],
        "seen_intro": False,
    }


def cargar_partida():
    """Lee los datos de la partida desde el archivo JSON."""
    try:
        with ARCHIVO_PARTIDA.open("r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        if isinstance(datos, dict):
            return datos

    except (OSError, json.JSONDecodeError):
        pass

    return partida_inicial()


def guardar_partida(datos):
    """Guarda los datos de la partida en JSON."""
    with ARCHIVO_PARTIDA.open("w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)


@app.route("/")
def inicio():
    datos = cargar_partida()

    misiones = [
        "Hablar con la anciana del pueblo",
        "Derrotar a las sombras del bosque",
        "Rescatar a Luma, la exploradora",
        "Encontrar la entrada de las ruinas",
        "Derrotar al Guardián y recuperar el cristal",
        "Aventura completada",
    ]

    numero_mision = datos.get("quest", 0)

    if not isinstance(numero_mision, int):
        numero_mision = 0

    numero_mision = max(0, min(numero_mision, len(misiones) - 1))

    return render_template(
        "index.html",
        datos=datos,
        nombre_mision=misiones[numero_mision],
    )


@app.route("/partida", methods=["GET", "POST"])
def partida():
    datos = cargar_partida()

    if request.method == "POST":
        try:
            vida = int(request.form.get("hp", datos.get("hp", 100)))
            pociones = int(request.form.get("potions", datos.get("potions", 3)))
            cristales = int(request.form.get("crystals", datos.get("crystals", 0)))
            mision = int(request.form.get("quest", datos.get("quest", 0)))
            posicion = int(request.form.get("player_x", datos.get("player_x", 100)))

            if not 0 <= vida <= 100:
                raise ValueError("La vida tiene que estar entre 0 y 100.")

            if not 0 <= pociones <= 99:
                raise ValueError("Las pociones tienen que estar entre 0 y 99.")

            if not 0 <= cristales <= 99:
                raise ValueError("Los cristales tienen que estar entre 0 y 99.")

            if not 0 <= mision <= 5:
                raise ValueError("Elegí una misión válida.")

            if not 0 <= posicion <= 3300:
                raise ValueError("La posición tiene que estar entre 0 y 3300.")

            datos.update({
                "version": 1,
                "hp": vida,
                "potions": pociones,
                "crystals": cristales,
                "quest": mision,
                "player_x": posicion,
            })

            datos.setdefault("allies", [])
            datos.setdefault("defeated", [])
            datos.setdefault("seen_intro", False)

            guardar_partida(datos)

            flash("Se guardaron los cambios de la partida.", "success")
            return redirect(url_for("inicio"))

        except ValueError as error:
            mensaje = str(error) or "Revisá los valores ingresados."
            flash(mensaje, "error")
            return redirect(url_for("partida"))

    return render_template("partida.html", datos=datos)


@app.route("/enemigos")
def enemigos():
    lista_enemigos = [
        {
            "nombre": "Sombra",
            "tipo": "Enemigo común",
            "zona": "Bosque",
        },
        {
            "nombre": "Lobo salvaje",
            "tipo": "Enemigo común",
            "zona": "Bosque",
        },
        {
            "nombre": "Sombra antigua",
            "tipo": "Enemigo fuerte",
            "zona": "Ruinas",
        },
        {
            "nombre": "Guardián del Cristal",
            "tipo": "Jefe final",
            "zona": "Ruinas",
        },
    ]

    return render_template("enemigos.html", enemigos=lista_enemigos)


if __name__ == "__main__":
    app.run(debug=True)
