import unittest

from inventario import core
from inventario.core import Herramienta


def ejemplo():
    return [
        Herramienta(1, "Soldador Hakko FX-888D", "electrónica"),
        Herramienta(2, "Multímetro Fluke 117", "electrónica"),
        Herramienta(3, "Sierra de calar", "carpintería", prestada_a="jorge"),
    ]


class TestBuscar(unittest.TestCase):
    def test_busca_por_parte_del_nombre(self):
        encontradas = core.buscar(ejemplo(), "Hakko")
        self.assertEqual([h.id for h in encontradas], [1])

    def test_no_distingue_mayusculas(self):
        # Nadie escribe "Soldador" con mayúscula cuando busca.
        encontradas = core.buscar(ejemplo(), "soldador")
        self.assertEqual([h.id for h in encontradas], [1])

    def test_no_distingue_tildes(self):
        # Ni se acuerda de si "multímetro" lleva tilde.
        encontradas = core.buscar(ejemplo(), "multimetro")
        self.assertEqual([h.id for h in encontradas], [2])


class TestPrestamos(unittest.TestCase):
    def test_prestar_y_devolver(self):
        herramientas = ejemplo()
        core.prestar(herramientas, 1, "ana")
        self.assertEqual(core.obtener(herramientas, 1).prestada_a, "ana")
        core.devolver(herramientas, 1)
        self.assertIsNone(core.obtener(herramientas, 1).prestada_a)

    def test_no_se_presta_dos_veces(self):
        with self.assertRaises(ValueError):
            core.prestar(ejemplo(), 3, "ana")

    def test_disponibles(self):
        self.assertEqual([h.id for h in core.disponibles(ejemplo())], [1, 2])


class TestAnadir(unittest.TestCase):
    def test_id_siguiente(self):
        herramientas = ejemplo()
        nueva = core.anadir(herramientas, "Lijadora", "carpintería")
        self.assertEqual(nueva.id, 4)


if __name__ == "__main__":
    unittest.main()
