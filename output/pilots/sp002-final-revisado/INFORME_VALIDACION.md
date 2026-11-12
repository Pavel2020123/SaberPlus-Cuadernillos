# SP-002, primera sesión: informe de validación local

## Entrega

- Proyecto editable: `project.json` (120 preguntas: 25 Matemáticas, 41 Lectura Crítica, 25 Sociales y 29 Ciencias Naturales).
- Cuadernillos: `cuadernillo.pdf` (61 páginas), `cuadernillo_resuelto.pdf` (79 páginas) y `clave_docente.pdf` (3 páginas).
- Manifiesto canónico: `substitutions.json`. Contiene los 16 cambios de posición, código anterior y nuevo, fuente, página, clave y transcripción completa. `replacements.json` se integró en este manifiesto y se retiró para evitar divergencias.
- SHA-256 del proyecto: `dd14765df81e56b53ffc756fca68d92fca0124add5d48239fb0d90216e86f9d9`. El `proyecto.json` exportado al generar los PDF es semánticamente idéntico.

## Validaciones

- `validate_project(exporting=True)`: sin advertencias.
- 120 preguntas seleccionadas y 120 códigos distintos; orden por áreas 25/41/25/29.
- 120 claves A-D, cuatro opciones completas, tema, subtema, explicación y clasificación editorial propuesta. Se completaron las clasificaciones heredadas de las posiciones 4 y 33.
- 14 contextos conservados, 13 referenciados correctamente; el contexto restante quedó sin uso al sustituir su bloque, pero se preservó por seguridad. Los grupos activos son contiguos.
- 56 imágenes referenciadas existen tanto en el piloto independiente como en `assets/uploads/` para el editor. Diez recursos nuevos se recortaron del PDF original sin marcas de respuesta.
- 16 sustituciones coherentes entre manifiesto y proyecto. La antigua posición 119, cuyo enunciado dependía de un contexto ausente, quedó sustituida.
- Cotejo contra `origin/main` `a450ec9` y `origin/trabajo/sp-003` `2406940`, con registros usados/reservados, reservas tabulares y equivalencias documentadas: cero coincidencias exactas y cero equivalencias confirmadas para las 120 preguntas. Ninguno de los 16 reemplazos enlaza en la cola de cotejo con un código ocupado. Hay 22 enlaces pendientes hacia códigos no ocupados en 15 de esos 16 reemplazos; necesitan cotejo visual antes de afirmar exclusividad definitiva.
- 42 pruebas automatizadas de PDF, integridad del editor, salidas, clasificaciones, imágenes e importación: correctas. La prueba de subíndices químicos confirma que se renderizan con posición inferior y sin cuadrados negros.
- Inspección visual local: figura grande de la pregunta 112, imagen de la 99, fórmulas y pregunta 120 en la página 58, hoja de respuestas desde la 59 hasta la 61, cierre del resuelto con explicación de la 120 y clave docente hasta la 120. No se observaron cortes ni figuras deformadas en esas páginas.

## Editor local

- Instancia aislada: `http://127.0.0.1:4192/`, iniciada con `python -B tool/editor_server.py --port 4192 --data-dir output/pilots/sp002-final-revisado`.
- La ruta principal y una imagen nueva respondieron HTTP 200. El endpoint de carga respondió 200 en el registro del servidor. La lectura de su cuerpo desde la herramienta local se cortó a 255 KiB; el proyecto supera ese tamaño.
- El mismo `load()`/`save()` del servidor se probó con una copia temporal exacta del proyecto: abrió 120 preguntas, guardó revisión 1→2 y creó un respaldo. El proyecto entregado permaneció sin cambios.
- La inspección visual del navegador no se completó: Computer Use detuvo el control al no poder confirmar con certeza la URL activa. El usuario debe abrir manualmente el enlace y comprobar el panel y la vista previa. Para reabrir después de reiniciar, ejecutar el comando anterior desde la raíz del repositorio; no se sustituye el editor habitual.

## Coordinación y publicación propuesta

La tabla de 29 códigos de Ciencias quedó añadida a `planning/reservas/SP-002.md` como **propuesta**, sin declararla reserva definitiva. Recomiendo compartir ese archivo, `tool/editor_pdf.py` y `tool/test_pdf_superscripts.py` tras revisión del coordinador. El proyecto, los PDF, los recortes originales y el manifiesto con transcripciones permanecen locales por ahora. No se modificó `planning/PREGUNTAS_USADAS_GLOBAL.json` y no se ejecutó commit, push ni merge.
