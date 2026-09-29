"""Juez del eval de la sesión 2: comprueba la tarea de evals/tarea.md.

    uv run pytest evals
"""

import json
import shutil
from pathlib import Path

from inventario import __main__ as cli

DATOS = Path(__file__).resolve().parents[1] / "datos" / "inventario.json"


def test_disponibles_lista_solo_lo_que_no_esta_prestado(tmp_path, monkeypatch, capsys):
    ruta = tmp_path / "inventario.json"
    shutil.copy(DATOS, ruta)
    monkeypatch.setattr(cli, "RUTA", ruta)

    assert cli.main(["disponibles"]) == 0
    salida = capsys.readouterr().out

    herramientas = json.loads(DATOS.read_text(encoding="utf-8"))
    for h in herramientas:
        if h["prestada_a"] is None:
            assert h["nombre"] in salida
        else:
            assert h["nombre"] not in salida
    assert len(salida.strip().splitlines()) == sum(h["prestada_a"] is None for h in herramientas)
