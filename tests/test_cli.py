"""Pruebas de la línea de comandos, contra una copia de los datos."""

import shutil
from pathlib import Path

import pytest

from inventario import __main__ as cli

DATOS = Path(__file__).resolve().parents[1] / "datos" / "inventario.json"


@pytest.fixture
def inventario(tmp_path, monkeypatch, capsys):
    ruta = tmp_path / "inventario.json"
    shutil.copy(DATOS, ruta)
    monkeypatch.setattr(cli, "RUTA", ruta)

    def ejecutar(*args):
        codigo = cli.main(list(args))
        salida = capsys.readouterr()
        return codigo, salida.out, salida.err

    return ejecutar


def test_listar(inventario):
    codigo, salida, _ = inventario("listar")
    assert codigo == 0
    assert "Soldador" in salida


def test_prestar_y_devolver_guardan(inventario):
    inventario("prestar", "4", "ana")
    assert "prestada a ana" in inventario("listar")[1]
    inventario("devolver", "4")
    assert "prestada a ana" not in inventario("listar")[1]


def test_prestar_dos_veces_da_error(inventario):
    codigo, _, errores = inventario("prestar", "3", "ana")  # la 3 ya la tiene marta
    assert codigo == 1
    assert "ya la tiene" in errores
