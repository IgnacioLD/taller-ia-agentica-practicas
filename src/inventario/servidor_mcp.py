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


@servidor.tool(annotations=SOLO_LECTURA)
def buscar(texto: str) -> list[dict]:
    """Herramientas cuyo nombre contiene `texto`, sin distinguir mayúsculas ni
    tildes. Úsala antes que `listar` cuando busques algo concreto."""
    return [asdict(h) for h in core.buscar(core.cargar(RUTA), texto)]


@servidor.tool(annotations=SOLO_LECTURA)
def disponibles() -> list[dict]:
    """Herramientas que no están prestadas ahora mismo."""
    return [asdict(h) for h in core.disponibles(core.cargar(RUTA))]


@servidor.tool(annotations=SOLO_LECTURA)
def categorias() -> dict[str, dict[str, int]]:
    """Resumen por categoría: cuántas herramientas hay y cuántas están disponibles."""
    return core.por_categoria(core.cargar(RUTA))


def main() -> None:
    servidor.run()
