"""Pruebas del agente contra un servidor falso que imita a OpenRouter.

No gastan saldo ni necesitan clave. Ejecuta:
    python3 -m unittest discover -s agente
"""

import json
import os
import sys
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent))
import agente  # noqa: E402


class ServidorFalso:
    """Devuelve, en orden, las respuestas que le digas y guarda lo que recibe."""

    def __init__(self, respuestas):
        self.respuestas = list(respuestas)
        self.recibido = []
        servidor = self

        class Manejador(BaseHTTPRequestHandler):
            def do_POST(self):
                largo = int(self.headers["Content-Length"])
                servidor.recibido.append(json.loads(self.rfile.read(largo)))
                cuerpo = json.dumps(servidor.respuestas.pop(0)).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(cuerpo)

            def log_message(self, *args):
                pass

        self.http = HTTPServer(("127.0.0.1", 0), Manejador)
        threading.Thread(target=self.http.serve_forever, daemon=True).start()
        self.url = f"http://127.0.0.1:{self.http.server_port}/"

    def cerrar(self):
        self.http.shutdown()


def texto(contenido):
    return {"choices": [{"message": {"role": "assistant", "content": contenido}}], "usage": {"cost": 0.001}}


def pide(nombre, argumentos, id="llamada-1"):
    return {
        "choices": [{"message": {"role": "assistant", "content": None, "tool_calls": [
            {"id": id, "type": "function", "function": {"name": nombre, "arguments": json.dumps(argumentos)}}
        ]}}],
        "usage": {"cost": 0.001},
    }


class TestAgente(unittest.TestCase):
    def arrancar(self, respuestas):
        self.servidor = ServidorFalso(respuestas)
        self.addCleanup(self.servidor.cerrar)
        entorno = {"OPENROUTER_API_KEY": "clave-falsa", "MODELO": "modelo/falso"}
        parches = [mock.patch.dict(os.environ, entorno), mock.patch.object(agente, "API", self.servidor.url)]
        for p in parches:
            p.start()
            self.addCleanup(p.stop)

    def test_sin_herramientas_devuelve_la_respuesta(self):
        self.arrancar([texto("hola")])
        self.assertEqual(agente.agente("saluda"), "hola")

    def test_usa_una_herramienta_y_ve_el_resultado(self):
        self.arrancar([pide("leer_fichero", {"ruta": "README.md"}), texto("es un inventario")])
        self.assertEqual(agente.agente("¿qué es esto?"), "es un inventario")
        # En la segunda llamada va el resultado de la herramienta: así "ve".
        segunda = self.servidor.recibido[1]["messages"]
        self.assertEqual(segunda[-1]["role"], "tool")
        self.assertIn("Inventario del hackerspace", segunda[-1]["content"])

    def test_la_conversacion_crece_en_cada_vuelta(self):
        self.arrancar([pide("leer_fichero", {"ruta": "README.md"}), texto("listo")])
        agente.agente("tarea")
        primera, segunda = (len(r["messages"]) for r in self.servidor.recibido)
        self.assertGreater(segunda, primera)

    def test_pide_permiso_antes_de_ejecutar(self):
        self.arrancar([pide("ejecutar", {"comando": "echo peligro"}), texto("vale")])
        with mock.patch("builtins.input", return_value="n"):
            agente.agente("ejecuta algo")
        resultado = self.servidor.recibido[1]["messages"][-1]["content"]
        self.assertIn("no ha permitido", resultado)

    def test_un_error_de_herramienta_no_rompe_el_bucle(self):
        self.arrancar([pide("leer_fichero", {"ruta": "no-existe.txt"}), texto("no estaba")])
        self.assertEqual(agente.agente("lee"), "no estaba")
        self.assertIn("Error", self.servidor.recibido[1]["messages"][-1]["content"])

    def test_para_al_llegar_al_limite_de_vueltas(self):
        self.arrancar([pide("leer_fichero", {"ruta": "README.md"}, id=str(i)) for i in range(agente.MAX_VUELTAS)])
        self.assertIn("límite", agente.agente("no acabes nunca"))


if __name__ == "__main__":
    unittest.main()
