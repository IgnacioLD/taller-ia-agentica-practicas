"""Pruebas del servidor MCP, conectando un cliente MCP de verdad en memoria."""

import pytest
from mcp import Client

from inventario.servidor_mcp import servidor


@pytest.fixture
def anyio_backend():
    return "asyncio"


async def llamar(nombre: str, argumentos: dict | None = None) -> list[dict]:
    async with Client(servidor) as cliente:
        resultado = await cliente.call_tool(nombre, argumentos or {})
    assert not resultado.is_error
    return resultado.structured_content["result"]


@pytest.mark.anyio
async def test_herramientas_de_solo_lectura():
    async with Client(servidor) as cliente:
        herramientas = (await cliente.list_tools()).tools
    assert {h.name for h in herramientas} == {"listar", "buscar", "disponibles"}
    assert all(h.annotations.read_only_hint for h in herramientas)


@pytest.mark.anyio
async def test_buscar():
    assert [h["id"] for h in await llamar("buscar", {"texto": "soldador"})] == [1]


@pytest.mark.anyio
async def test_disponibles_no_incluye_las_prestadas():
    disponibles = await llamar("disponibles")
    assert disponibles
    assert all(h["prestada_a"] is None for h in disponibles)
