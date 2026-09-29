import pytest

from inventario import core
from inventario.core import Herramienta


@pytest.fixture
def herramientas():
    return [
        Herramienta(1, "Soldador Hakko FX-888D", "electrónica"),
        Herramienta(2, "Multímetro Fluke 117", "electrónica"),
        Herramienta(3, "Sierra de calar", "carpintería", prestada_a="jorge"),
    ]


def ids(lista):
    return [h.id for h in lista]


def test_busca_por_parte_del_nombre(herramientas):
    assert ids(core.buscar(herramientas, "Hakko")) == [1]


def test_no_distingue_mayusculas(herramientas):
    # Nadie escribe "Soldador" con mayúscula cuando busca.
    assert ids(core.buscar(herramientas, "soldador")) == [1]


def test_no_distingue_tildes(herramientas):
    # Ni se acuerda de si "multímetro" lleva tilde.
    assert ids(core.buscar(herramientas, "multimetro")) == [2]


def test_prestar_y_devolver(herramientas):
    core.prestar(herramientas, 1, "ana")
    assert core.obtener(herramientas, 1).prestada_a == "ana"
    core.devolver(herramientas, 1)
    assert core.obtener(herramientas, 1).prestada_a is None


def test_no_se_presta_dos_veces(herramientas):
    with pytest.raises(ValueError):
        core.prestar(herramientas, 3, "ana")


def test_disponibles(herramientas):
    assert ids(core.disponibles(herramientas)) == [1, 2]


def test_anadir_usa_el_id_siguiente(herramientas):
    assert core.anadir(herramientas, "Lijadora", "carpintería").id == 4
