"""Lógica del inventario: cargar, buscar, prestar y devolver herramientas."""

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class Herramienta:
    id: int
    nombre: str
    categoria: str
    prestada_a: str | None = None


def cargar(ruta: Path) -> list[Herramienta]:
    datos = json.loads(Path(ruta).read_text(encoding="utf-8"))
    return [Herramienta(**h) for h in datos]


def guardar(ruta: Path, herramientas: list[Herramienta]) -> None:
    texto = json.dumps([asdict(h) for h in herramientas], ensure_ascii=False, indent=2)
    Path(ruta).write_text(texto + "\n", encoding="utf-8")


def anadir(herramientas: list[Herramienta], nombre: str, categoria: str) -> Herramienta:
    nuevo_id = max((h.id for h in herramientas), default=0) + 1
    herramienta = Herramienta(id=nuevo_id, nombre=nombre, categoria=categoria)
    herramientas.append(herramienta)
    return herramienta


def buscar(herramientas: list[Herramienta], texto: str) -> list[Herramienta]:
    """Herramientas cuyo nombre contiene `texto`."""
    return [h for h in herramientas if texto in h.nombre]


def obtener(herramientas: list[Herramienta], id: int) -> Herramienta:
    for h in herramientas:
        if h.id == id:
            return h
    raise KeyError(f"no existe la herramienta {id}")


def prestar(herramientas: list[Herramienta], id: int, socio: str) -> Herramienta:
    herramienta = obtener(herramientas, id)
    if herramienta.prestada_a:
        raise ValueError(f"{herramienta.nombre} ya la tiene {herramienta.prestada_a}")
    herramienta.prestada_a = socio
    return herramienta


def devolver(herramientas: list[Herramienta], id: int) -> Herramienta:
    herramienta = obtener(herramientas, id)
    herramienta.prestada_a = None
    return herramienta


def disponibles(herramientas: list[Herramienta]) -> list[Herramienta]:
    return [h for h in herramientas if h.prestada_a is None]
