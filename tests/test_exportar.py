import csv
import io

from inventario.core import Herramienta
from inventario.exportar import a_csv


def filas(texto: str) -> list[list[str]]:
    return list(csv.reader(io.StringIO(texto)))


def test_cabecera_y_filas():
    texto = a_csv([Herramienta(1, "Soldador, grande", "electrónica", prestada_a="ana")])
    assert filas(texto)[0] == ["id", "nombre", "categoria", "prestada_a"]
    # La coma del nombre no rompe el CSV.
    assert filas(texto)[1] == ["1", "Soldador, grande", "electrónica", "ana"]


def test_disponible_va_vacio():
    assert filas(a_csv([Herramienta(2, "Sierra", "carpintería")]))[1][3] == ""


def test_comando_exportar(capsys):
    from inventario import __main__ as cli

    assert cli.main(["exportar"]) == 0
    assert capsys.readouterr().out.startswith("id,nombre,categoria,prestada_a")
