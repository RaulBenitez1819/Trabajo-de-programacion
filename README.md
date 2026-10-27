# Fox's Adventures

## De que se trata
Este es mi juego de aventura del zorro. La idea es recuperar el cristal que le robaron al pueblo.

## Archivos
- `fox_adventures.py`: codigo del juego.
- `web_app.py`: parte web hecha con Flask.
- `templates`: paginas HTML.
- `static`: archivo CSS.
- `fox_save.json`: datos guardados de la partida. Se crea cuando guardo los cambios desde la web.

## Como ejecutarlo
Primero instalar las librerias:

```powershell
python -m pip install -r requirements.txt
```

Para abrir el juego:

```powershell
python fox_adventures.py
```

Para abrir la pagina web:

```powershell
python web_app.py
```

Despues entrar desde el navegador a `http://127.0.0.1:5000`.

## Lo que tiene por ahora
- Pagina de inicio con los datos de la partida.
- Formulario para cambiar la vida, pociones, cristales, mision y posicion.
- Listado de enemigos.
- Flask conecta las paginas y guarda los datos en JSON.

## A tener en cuenta
Esta parte web es un avance de la entrega 4. El juego de Pygame sigue funcionando aparte. Si cambio los datos desde la web, se guardan en el JSON, pero el juego no se controla desde el navegador.

Todavia falta probarlo bien y seguir conectando las funciones del juego.
