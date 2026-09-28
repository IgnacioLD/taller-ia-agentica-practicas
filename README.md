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
python3 -m unittest
```

## Checkpoints

Cada ejercicio del curso tiene su solución en una rama `checkpoint/sN-M`
(sesión N, ejercicio M). Si te quedas atrás:

```sh
git switch checkpoint/s1-2
```
