"""Exportar el inventario a CSV, para abrirlo en una hoja de cálculo."""

import csv
import io

from .core import Herramienta

COLUMNAS = ["id", "nombre", "categoria", "prestada_a"]


def a_csv(herramientas: list[Herramienta]) -> str:
    salida = io.StringIO()
    escritor = csv.writer(salida)
    escritor.writerow(COLUMNAS)
    for h in herramientas:
        escritor.writerow([h.id, h.nombre, h.categoria, h.prestada_a or ""])
    return salida.getvalue()
