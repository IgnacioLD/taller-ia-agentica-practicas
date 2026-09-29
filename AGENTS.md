# AGENTS.md

Inventario de herramientas del Hackerspace Valencia: qué hay y quién lo tiene.
Python 3.12+ con [uv](https://docs.astral.sh/uv/). Datos en
`datos/inventario.json`.

## Comandos

- Instalar: `uv sync`
- Tests: `uv run pytest`. Tienen que pasar antes de dar nada por hecho.
- Ejecutar: `uv run inventario listar` (ver `uv run inventario --help`).

## Cómo se trabaja

- La lógica va en `src/inventario/core.py`; la línea de comandos, en
  `src/inventario/__main__.py`, sin lógica de negocio.
- Cada cambio de comportamiento lleva su test en `tests/`.
- No cambies un test para que pase: si un test está mal, dilo y explica por qué.
- Dependencias nuevas solo con `uv add`, y pregunta antes.
- Cambios pequeños y enfocados: toca solo los ficheros que pide la tarea.

## Estilo

- Nombres y mensajes en español de España, como el resto del código.
- Docstring corta cuando no sea obvio qué hace una función.

## No hagas

- No edites `datos/inventario.json` a mano en una tarea de código.
- No hagas commits ni push: eso lo decide la persona.
