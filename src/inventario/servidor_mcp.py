"""Servidor MCP del inventario: cualquier agente compatible (opencode, Claude
Code, Codex, Cursor...) puede consultar el inventario con estas herramientas.

Arranca por stdio: el agente lo lanza y le habla por la entrada y salida
estándar. Para probarlo a mano, con el inspector oficial:
    npx @modelcontextprotocol/inspector uv run inventario-mcp
"""

from dataclasses import asdict

from mcp.server import MCPServer
from mcp.types import ToolAnnotations

from . import core
from .__main__ import RUTA

servidor = MCPServer(
    "inventario",
    instructions="Inventario de herramientas del Hackerspace Valencia: qué hay y quién lo tiene.",
)

SOLO_LECTURA = ToolAnnotations(readOnlyHint=True)


@servidor.tool(annotations=SOLO_LECTURA)
def listar() -> list[dict]:
    """Todas las herramientas del inventario, con quién tiene cada una."""
    return [asdict(h) for h in core.cargar(RUTA)]


# EJERCICIO: añade dos herramientas más, de solo lectura como `listar`:
#   - buscar(texto): las herramientas cuyo nombre contiene `texto`.
#   - disponibles(): las que no están prestadas.
# La docstring es lo que lee el modelo para decidir cuándo usar cada una:
# escríbela pensando en él.


def main() -> None:
    servidor.run()
