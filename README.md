# Inventario del hackerspace

Repo de prácticas del curso de IA agéntica para socios del Hackerspace
Valencia. Es un gestor mínimo del inventario de herramientas: qué hay y quién
lo tiene.

## Arrancar

Necesitas [uv](https://docs.astral.sh/uv/getting-started/installation/), que
instala el Python que haga falta.

```sh
uv sync                          # instala Python y las dependencias
uv run inventario listar
uv run inventario buscar soldador
uv run pytest                    # tests del inventario
cp .env.ejemplo .env             # configuración local
```

## Qué hay

| Carpeta | Qué es | Sesión |
| --- | --- | --- |
| `src/inventario/` | El inventario: lógica (`core.py`) y línea de comandos | 1 |
| `tests/` | Tests con pytest. En `main` fallan 2 a propósito | 1 |
| `agente/` | Tu propio agente: el bucle lo escribes tú | 2 |
| `src/inventario/servidor_mcp.py` | Servidor MCP del inventario | 2 |
| `issues/` | Issues abiertos del proyecto | 2 |
| `scripts/` | Utilidades del proyecto | 2 |
| `plantillas/` | `AGENTS.md`, diario de agente y ficha de tu proyecto final | 2 |
| `.devcontainer/` | Sandbox: el agente dentro de un contenedor que solo ve este repo | 2 |

## Tu agente (sesión 2)

`agente/agente.py` habla con OpenRouter con el SDK de OpenAI. Las
herramientas y la llamada al modelo ya están; el bucle, no. Sus pruebas usan un
cliente falso y no gastan saldo: cuando pasen, tu bucle funciona.

```sh
uv run pytest agente
export OPENROUTER_API_KEY=sk-or-...   # tu clave del curso
uv run agente/agente.py "explícame qué hace este proyecto"
```

## Soluciones

Cada ejercicio tiene su solución en una rama `solucion/sN-M` (sesión N,
ejercicio M). Son acumulativas: cada una incluye las anteriores. Si te quedas
atrás:

```sh
git switch solucion/s1-2
```
