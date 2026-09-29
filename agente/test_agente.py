"""Pruebas del agente con un cliente falso: no llaman a ningún modelo ni gastan
saldo. Cuando pasen todas, tu bucle funciona: `uv run pytest agente`."""

import copy
import json
from types import SimpleNamespace

from openai.types.chat import ChatCompletion

from agente import agente as ag


def respuesta(mensaje: dict) -> ChatCompletion:
    return ChatCompletion.model_validate({
        "id": "falsa",
        "object": "chat.completion",
        "created": 0,
        "model": "falso",
        "choices": [{"index": 0, "finish_reason": "stop", "message": {"role": "assistant", **mensaje}}],
    })


def texto(contenido: str) -> ChatCompletion:
    return respuesta({"content": contenido})


def pide(nombre: str, argumentos: dict, id: str = "llamada_1") -> ChatCompletion:
    return respuesta({
        "content": None,
        "tool_calls": [{"id": id, "type": "function", "function": {"name": nombre, "arguments": json.dumps(argumentos)}}],
    })


class ClienteFalso:
    """Imita a cliente.chat.completions.create y guarda lo que se le manda."""

    def __init__(self, *respuestas):
        self.respuestas = list(respuestas)
        self.peticiones = []
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self.create))

    def create(self, **peticion):
        self.peticiones.append(copy.deepcopy(peticion["messages"]))
        return self.respuestas.pop(0) if len(self.respuestas) > 1 else self.respuestas[0]


def test_responde_sin_herramientas():
    cliente = ClienteFalso(texto("Es un inventario."))
    assert ag.agente("¿qué es esto?", cliente) == "Es un inventario."
    assert len(cliente.peticiones) == 1


def test_ejecuta_la_herramienta_y_le_devuelve_el_resultado():
    cliente = ClienteFalso(pide("leer_fichero", {"ruta": "pyproject.toml"}), texto("Hecho."))
    assert ag.agente("lee el pyproject", cliente) == "Hecho."
    resultado = cliente.peticiones[1][-1]
    assert resultado["role"] == "tool"
    assert resultado["tool_call_id"] == "llamada_1"
    assert 'name = "inventario"' in resultado["content"]


def test_la_conversacion_crece_en_cada_vuelta():
    cliente = ClienteFalso(pide("leer_fichero", {"ruta": "pyproject.toml"}), texto("Hecho."))
    ag.agente("lee el pyproject", cliente)
    primera, segunda = cliente.peticiones
    # La segunda llamada lleva todo lo anterior más la petición del modelo y el resultado.
    assert segunda[: len(primera)] == primera
    assert len(segunda) == len(primera) + 2


def test_para_en_el_limite_de_vueltas():
    cliente = ClienteFalso(pide("leer_fichero", {"ruta": "pyproject.toml"}))  # nunca termina
    final = ag.agente("no pares nunca", cliente)
    assert len(cliente.peticiones) == ag.MAX_VUELTAS
    assert "límite" in final


def test_un_error_de_herramienta_vuelve_al_modelo():
    cliente = ClienteFalso(pide("leer_fichero", {"ruta": "no-existe.txt"}), texto("No está."))
    assert ag.agente("lee un fichero que no existe", cliente) == "No está."
    assert cliente.peticiones[1][-1]["content"].startswith("Error:")


def test_no_lee_fuera_del_proyecto():
    assert ag.leer_fichero("../../../../etc/hosts").startswith("Error:")


def test_pide_permiso_antes_de_ejecutar(monkeypatch, tmp_path):
    monkeypatch.setattr("builtins.input", lambda _: "n")
    marca = tmp_path / "ejecutado"
    assert "no ha permitido" in ag.ejecutar(f"touch {marca}")
    assert not marca.exists()
