"""Un agente mínimo: un bucle, dos herramientas y límites.

Uso:
    export OPENROUTER_API_KEY=sk-or-...   # tu clave del curso
    uv run agente/agente.py "explícame qué hace este proyecto"

Habla con OpenRouter a través del SDK de OpenAI: la API de chat de OpenAI es
el estándar de hecho y casi todos los proveedores la aceptan. Cambia de
modelo con la variable MODELO.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

from openai import OpenAI

MODELO = os.environ.get("MODELO", "~deepseek/deepseek-flash-latest")
MAX_VUELTAS = 15
MAX_SALIDA = 20_000  # caracteres: lo que devuelve una herramienta también ocupa contexto
RAIZ = Path.cwd().resolve()

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


# --- Herramientas: las ejecuta TU programa, no el modelo -----------------------


def leer_fichero(ruta: str) -> str:
    fichero = (RAIZ / ruta).resolve()
    if not fichero.is_relative_to(RAIZ):
        return "Error: solo puedes leer ficheros dentro del proyecto."
    return fichero.read_text(encoding="utf-8")[:MAX_SALIDA]


def ejecutar(comando: str) -> str:
    # El modelo propone; tú decides. Sin esto, cualquier texto que lea el agente
    # (un issue, una web) podría acabar ejecutándose en tu máquina.
    if input(f"\n¿Ejecutar `{comando}`? [s/N] ").strip().lower() != "s":
        return "El usuario no ha permitido ejecutar ese comando."
    r = subprocess.run(comando, shell=True, cwd=RAIZ, capture_output=True, text=True, timeout=120)
    salida = (r.stdout + r.stderr)[-MAX_SALIDA:]
    return salida or f"(sin salida, código de salida {r.returncode})"


FUNCIONES = {"leer_fichero": leer_fichero, "ejecutar": ejecutar}


def ejecutar_herramienta(llamada) -> str:
    """Ejecuta una llamada a herramienta del modelo. Los errores también se le
    devuelven como texto: son información para que corrija."""
    try:
        argumentos = json.loads(llamada.function.arguments or "{}")
        print(f"  -> {llamada.function.name}({argumentos})", file=sys.stderr)
        return FUNCIONES[llamada.function.name](**argumentos)
    except Exception as error:
        return f"Error: {error}"


# --- El modelo -----------------------------------------------------------------


def llamar_modelo(cliente: OpenAI, mensajes: list, modelo: str, vuelta: int):
    """Una llamada al modelo con toda la conversación. Enseña tokens y coste."""
    respuesta = cliente.chat.completions.create(
        model=modelo,
        messages=mensajes,
        tools=HERRAMIENTAS,
        extra_body={"usage": {"include": True}},  # OpenRouter devuelve el coste
    )
    uso = respuesta.usage
    if uso:
        coste = getattr(uso, "cost", None)
        print(
            f"[vuelta {vuelta}] entrada {uso.prompt_tokens} tokens, salida {uso.completion_tokens}"
            + (f", {coste:.5f} $" if coste is not None else ""),
            file=sys.stderr,
        )
    return respuesta


# --- El bucle --------------------------------------------------------------------


def agente(tarea: str, cliente: OpenAI, modelo: str = MODELO) -> str:
    mensajes = [{"role": "system", "content": SISTEMA}, {"role": "user", "content": tarea}]

    # EJERCICIO: escribe el bucle del agente (unas 10 líneas).
    # En cada vuelta, como mucho MAX_VUELTAS:
    #   1. Llama al modelo: llamar_modelo(cliente, mensajes, modelo, vuelta).
    #      Su mensaje está en respuesta.choices[0].message.
    #   2. Añádelo a `mensajes` con mensaje.model_dump(exclude_none=True):
    #      la conversación crece en cada vuelta.
    #   3. Si no pide herramientas (mensaje.tool_calls está vacío), ha
    #      terminado: devuelve mensaje.content.
    #   4. Si pide, ejecuta cada llamada con ejecutar_herramienta(llamada) y
    #      añade el resultado a `mensajes`:
    #      {"role": "tool", "tool_call_id": llamada.id, "content": resultado}
    # Si se acaban las vueltas, devuelve un aviso de que no ha terminado.
    raise NotImplementedError("escribe el bucle del agente")


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit('Uso: uv run agente/agente.py "tu tarea"')
    if not os.environ.get("OPENROUTER_API_KEY"):
        sys.exit("Falta OPENROUTER_API_KEY: export OPENROUTER_API_KEY=sk-or-...")
    cliente = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.environ["OPENROUTER_API_KEY"])
    print(agente(" ".join(sys.argv[1:]), cliente))


if __name__ == "__main__":
    main()
