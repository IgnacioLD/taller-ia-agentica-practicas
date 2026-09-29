from inventario import core
from inventario.core import Herramienta


def test_buscar_ignora_espacios_de_mas():
    herramientas = [Herramienta(1, "Soldador Hakko FX-888D", "electrónica")]
    assert [h.id for h in core.buscar(herramientas, " soldador ")] == [1]
