# Proyectos finales SP001–SP003

Cada simulacro conserva sus dos sesiones (120 y 134 preguntas). Los seis JSON mantienen preguntas, opciones, claves, contextos y orden de la entrega final del 13 de noviembre de 2026. Solo se normalizaron las rutas de imágenes para compartir recursos idénticos en `assets/uploads/`.

Desde la raíz del repositorio, con `uv sync` completado, se puede generar una sesión:

```powershell
uv run --offline python -c "import sys,json; from pathlib import Path; sys.path.insert(0,'tool'); from editor_pdf import generate; p=json.loads(Path('projects/finales/SP002/Segunda_sesion.json').read_text(encoding='utf8')); print(generate(p,'output/editor/SP002_segunda'))"
```

El resultado incluye documentos de estudiante y docente separados. Los JSON contienen claves y explicaciones: compartirlos únicamente con el equipo o profesor.

Los PDF finales con marca y sin marca se conservan por separado en las dos carpetas de entrega de la memoria PAVEL. No se incluyen aquí PDF, ZIP ni copias temporales. Los scripts `tool/prepare_unbranded_delivery.py` y `tool/verify_unbranded_delivery.py` conservan el procedimiento utilizado para preparar y verificar la edición sin marca; trabajan sobre una copia de la entrega completa del escritorio y no modifican la entrega original.

Las imágenes de preguntas son referencias aportadas durante el trabajo; este archivo no acredita permisos comerciales ni validación externa.
