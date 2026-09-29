#!/bin/sh
# Diagnóstico estándar para los issues: versiones y configuración del proyecto.
echo "## Diagnóstico $(date +%F)"
echo "- uv: $(uv --version)"
echo "- python: $(uv run python --version)"
echo "- tests: $(uv run pytest -q 2>&1 | tail -1)"
echo "## Configuración"
for f in pyproject.toml .python-version .env; do
  [ -f "$f" ] && { echo "### $f"; cat "$f"; }
done
