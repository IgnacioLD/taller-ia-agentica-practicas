"""Uso: uv run inventario <comando> ...

Comandos:
  listar                     todas las herramientas
  buscar <texto>             buscar por nombre
  prestar <id> <socio>       prestar una herramienta
  devolver <id>              devolver una herramienta
  anadir <nombre> <categoria>
  exportar                   el inventario en CSV (uv run inventario exportar > inventario.csv)
"""

import argparse
import sys
from pathlib import Path

from . import core, exportar

# src/inventario/__main__.py -> raíz del repo
RUTA = Path(__file__).resolve().parents[2] / "datos" / "inventario.json"


def mostrar(herramientas):
    for h in herramientas:
        estado = f"prestada a {h.prestada_a}" if h.prestada_a else "disponible"
        print(f"{h.id:>3}  {h.nombre:<28} {h.categoria:<14} {estado}")


def main(argv=None):
    parser = argparse.ArgumentParser(prog="inventario", description="Inventario del Hackerspace Valencia")
    sub = parser.add_subparsers(dest="comando", required=True)
    sub.add_parser("listar")
    p = sub.add_parser("buscar")
    p.add_argument("texto")
    p = sub.add_parser("prestar")
    p.add_argument("id", type=int)
    p.add_argument("socio")
    p = sub.add_parser("devolver")
    p.add_argument("id", type=int)
    p = sub.add_parser("anadir")
    p.add_argument("nombre")
    p.add_argument("categoria")
    sub.add_parser("exportar")
    args = parser.parse_args(argv)

    herramientas = core.cargar(RUTA)
    try:
        if args.comando == "listar":
            mostrar(herramientas)
        elif args.comando == "buscar":
            mostrar(core.buscar(herramientas, args.texto))
        elif args.comando == "prestar":
            h = core.prestar(herramientas, args.id, args.socio)
            core.guardar(RUTA, herramientas)
            print(f"{h.nombre} prestada a {h.prestada_a}")
        elif args.comando == "devolver":
            h = core.devolver(herramientas, args.id)
            core.guardar(RUTA, herramientas)
            print(f"{h.nombre} devuelta")
        elif args.comando == "anadir":
            h = core.anadir(herramientas, args.nombre, args.categoria)
            core.guardar(RUTA, herramientas)
            print(f"añadida con id {h.id}")
        elif args.comando == "exportar":
            sys.stdout.write(exportar.a_csv(herramientas))
    except (KeyError, ValueError) as err:
        print(f"error: {err.args[0]}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
