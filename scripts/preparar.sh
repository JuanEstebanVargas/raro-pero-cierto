#!/usr/bin/env bash
# Instala todo lo necesario (idempotente). Usar al inicio de cada ejecucion en la nube.
set -euo pipefail
cd "$(dirname "$0")/.."
if [ ! -d .venv ]; then python3 -m venv .venv; fi
. .venv/bin/activate
pip install -q -r requirements.txt
(cd video && npm ci --silent --no-audit --no-fund)
python - <<'PY'
from scripts.producir import asegurar_modelos
asegurar_modelos()
PY
echo "Entorno listo"
