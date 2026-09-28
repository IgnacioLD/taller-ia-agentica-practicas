"""Un agente mínimo: el bucle, dos herramientas y nada más.

Uso:
    export OPENROUTER_API_KEY=sk-or-...
    export MODELO=<el modelo del día>
    python3 agente/agente.py "explícame qué hace este proyecto"

Solo usa la biblioteca estándar de Python. Habla con la API de OpenRouter,
que es compatible con la de OpenAI.
"""

import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

API = os.environ.get("OPENROUTER_URL", "https://openrouter.ai/api/v1/chat/completions")
MAX_VUELTAS = 20
MAX_SALIDA = 20_000  # caracteres: lo que devuelve una herramienta también ocupa contexto

SISTEMA = """Eres un agente de programación que trabaja en el repositorio actual.
Antes de responder, mira los ficheros que haga falta con tus herramientas.
Cuando cambies código, ejecuta los tests para comprobarlo.
Cuando hayas terminado, responde con un resumen breve de lo que has hecho."""

HERRAMIENTAS = [
    {
        "type": "function",
        "function": {
            "name": "leer_fichero",
            "description": "Lee un fichero de texto del proyecto y devuelve su contenido.",
            "parameters": {
                "type": "object",
                "properties": {"ruta": {"type": "string", "description": "Ruta relativa al proyecto"}},
                "required": ["ruta"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "ejecutar",
            "description": (
                "Ejecuta un comando de shell en el proyecto y devuelve su salida. "
                "Sirve para listar ficheros, ejecutar tests o modificar ficheros."
            ),
            "parameters": {
                "type": "object",
                "properties": {"comando": {"type": "string", "description": "Comando de shell"}},
                "required": ["comando"],
            },
        },
    },
]


# --- Herramientas: esto lo ejecuta TU programa, no el modelo -----------------


def leer_fichero(ruta: str) -> str:
    return Path(ruta).read_text(encoding="utf-8")[:MAX_SALIDA]


def ejecutar(comando: str) -> str:
    # EJERCICIO 2: pide permiso antes de ejecutar (input) y, si la respuesta no
    # es "s", devuelve un texto que le explique al modelo que no se ha ejecutado.
    r = subprocess.run(comando, shell=True, capture_output=True, text=True, timeout=120)
    salida = (r.stdout + r.stderr)[-MAX_SALIDA:]
    return salida or f"(sin salida, código de salida {r.returncode})"


FUNCIONES = {"leer_fichero": leer_fichero, "ejecutar": ejecutar}


# --- El modelo ---------------------------------------------------------------


def llamar_modelo(mensajes: list, modelo: str) -> dict:
    cuerpo = {
        "model": modelo,
        "messages": mensajes,
        "tools": HERRAMIENTAS,
        "usage": {"include": True},  # OpenRouter devuelve el coste de la llamada
    }
    peticion = urllib.request.Request(
        API,
        data=json.dumps(cuerpo).encode(),
        headers={
            "Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(peticion, timeout=180) as respuesta:
        return json.load(respuesta)


# --- El bucle ----------------------------------------------------------------


def agente(tarea: str, modelo: str | None = None) -> str:
    modelo = modelo or os.environ["MODELO"]
    mensajes = [{"role": "system", "content": SISTEMA}, {"role": "user", "content": tarea}]

    # EJERCICIO 1: el bucle. Repite:
    #   1. respuesta = llamar_modelo(mensajes, modelo)
    #      El mensaje del modelo está en respuesta["choices"][0]["message"].
    #   2. Añade ese mensaje a `mensajes`: la conversación crece en cada vuelta.
    #   3. Si no pide herramientas (mensaje.get("tool_calls") está vacío),
    #      has terminado: devuelve mensaje["content"].
    #   4. Si pide, para cada llamada en mensaje["tool_calls"]:
    #        nombre = llamada["function"]["name"]
    #        argumentos = json.loads(llamada["function"]["arguments"])
    #        resultado = FUNCIONES[nombre](**argumentos)
    #      y añade a `mensajes`:
    #        {"role": "tool", "tool_call_id": llamada["id"], "content": resultado}
    #   5. Vuelta al paso 1.
    #
    # EJERCICIO 2: que no pueda dar vueltas infinitas (MAX_VUELTAS), que un
    # error de una herramienta no rompa el bucle, y que imprima los tokens y el
    # coste de cada vuelta (respuesta["usage"]).
    raise NotImplementedError("escribe el bucle")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit('Uso: python3 agente/agente.py "tu tarea"')
    print(agente(" ".join(sys.argv[1:])))
