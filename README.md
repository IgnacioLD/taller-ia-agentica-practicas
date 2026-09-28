# Inventario del hackerspace

Repo de prácticas del curso de IA agéntica para socios del Hackerspace
Valencia. Es un gestor mínimo del inventario de herramientas: qué hay y quién
lo tiene.

Solo necesita **Python 3.10 o superior**. No tiene dependencias.

```sh
python3 -m inventario listar
python3 -m inventario buscar soldador
python3 -m inventario prestar 1 tu-nombre
python3 -m inventario devolver 1
```

Tests:

```sh
python3 -m unittest                      # el inventario
python3 -m unittest discover -s agente   # tu agente (sesión 2)
```

## Tu agente (sesión 2)

`agente/agente.py` es un agente mínimo que escribes tú: la conexión con el
modelo y las herramientas ya están; el bucle, no. Las pruebas de
`agente/test_agente.py` usan un servidor falso que imita a OpenRouter: no
gastan saldo. Cuando pasen todas, tu agente funciona.

```sh
export OPENROUTER_API_KEY=sk-or-...   # tu clave del curso
export MODELO=...                     # el modelo del día
python3 agente/agente.py "explícame qué hace este proyecto"
```

## Otras carpetas

- `seguridad/`: material de la demo de seguridad de la sesión 5. El secreto es
  **falso**.
- `plantillas/`: plantillas para tu proyecto final (`AGENTS.md`, diario de
  agente y ficha del proyecto).

## Checkpoints

Cada ejercicio del curso tiene su solución en una rama `checkpoint/sN-M`
(sesión N, ejercicio M). Si te quedas atrás:

```sh
git switch checkpoint/s1-2
```
