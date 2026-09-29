from inventario import core
from inventario.core import Herramienta


def test_cuenta_total_y_disponibles():
    herramientas = [
        Herramienta(1, "Soldador", "electrónica"),
        Herramienta(2, "Multímetro", "electrónica", prestada_a="ana"),
        Herramienta(3, "Sierra", "carpintería"),
    ]
    assert core.por_categoria(herramientas) == {
        "carpintería": {"total": 1, "disponibles": 1},
        "electrónica": {"total": 2, "disponibles": 1},
    }


def test_sin_herramientas():
    assert core.por_categoria([]) == {}
