# SP-003 · Sociales cargadas en espacio independiente

12 de noviembre de 2026. El usuario autorizó extraer los textos directamente de los PDF mientras continúa Ciencias en el principal. Se cargaron **las 25 preguntas de la selección**, sin sustituciones, en **http://127.0.0.1:4187/**, espacio `SP-003-sociales`, primera sesión, **revisión 5**.

**Pendiente: revisión del usuario y posterior unificación con su avance de Ciencias. No importar este JSON sobre el principal.**

## Guardados y entrega local

- Proyecto del editor: `data/parallel/SP-003-sociales-4187/project.json`.
- Copias automáticas de cada lote: `data/parallel/SP-003-sociales-4187/backups/`.
- Copia para revisar e integrar: `output/editor/SP003-sociales-rev5-204a5ba4/proyecto.json`.
- Estudiante: `output/editor/SP003-sociales-rev5-204a5ba4/cuadernillo.pdf`, **15 páginas**.
- Resuelto: `output/editor/SP003-sociales-rev5-204a5ba4/cuadernillo_resuelto.pdf`, **18 páginas**.
- Clave separada: `output/editor/SP003-sociales-rev5-204a5ba4/clave_docente.pdf`, **1 página**.
- El directorio de entrega incluye una copia local del único recurso gráfico dentro de `assets/uploads/`, con su nombre original. Para trasladarlo, el JSON necesita esa imagen en el almacén de la raíz.

Los guardados se hicieron por la API local de **4187**, con token propio, control de revisión y respaldo, en cinco lotes de cinco preguntas. No se escribieron ni reiniciaron el editor 4185 del usuario, su proyecto principal o el antiguo paralelo de 4186. El servidor separado se abrió mediante `editor_parallel.py`, no cambiando solamente el puerto del servidor principal.

Para reabrir únicamente el espacio de Sociales si se detiene:

```powershell
uv run --offline python -B tool/editor_parallel.py --port 4187 --workspace SP-003-sociales
```

Conserva el guardado existente; no cargar una muestra ni crear otro espacio con un nombre distinto.

## Contenido y recursos

La [lista de 25 códigos utilizados](SP003_S1_SOCIALES_CODIGOS_USADOS.txt) coincide exactamente, en el mismo orden, con la [selección documentada](SP003_S1_SOCIALES_CANDIDATAS_25.md). La numeración de este proyecto aislado es 1–25; al reunirlo con Matemáticas y Lectura ocupará los puestos 67–91. No se introdujeron preguntas vacías para forzar esos números.

Se transcribieron casos, fragmentos, citas, enunciados y cuatro opciones por pregunta desde las páginas renderizadas de los originales. Se normalizaron los saltos de renglón del escaneo para componer los párrafos, sin cambiar datos, opciones o negaciones. La pregunta 6 conserva ambos textos de Nariño y sus referencias; la 12 conserva el «NO». Las explicaciones y justificaciones editoriales fueron redactadas por SaberPlus, separadas del material sin resolver; no se atribuyen al autor de los PDF.

La clasificación guardada es **8 pensamiento social, 10 perspectivas y 7 pensamiento reflexivo y sistémico**, con justificaciones y sin inventar afirmaciones o evidencias. Conserva estado editorial `proposed`, pendiente de revisión del usuario; no atribuye aprobación docente ni calibración psicométrica.

La figura de Sociales 20 se extrajo de la física 2 de `USB-524d98b0a234` y se mejoró con la herramienta integrada **imagegen**, siguiendo la instrucción del usuario sobre imágenes nuevas. Recurso: `assets/uploads/5d96ceaedad54b9e83dcf05a6919ba69.png`; original de extracción, prompt y cotejo en `tmp/sp003/sociales/carga/`, especialmente `PROMPT_CARTEL.md`. Se conservan texto, fotografía, X y proporción general; la restauración reconstruye detalles tipográficos y fotográficos. El usuario revisará también esa imagen. No se editaron los PDF originales ni las referencias.

## Comprobaciones

- Modelo válido: 25 preguntas incluidas, 25 códigos distintos, cuatro opciones, clave y explicación en cada registro; sin contextos compartidos entre preguntas.
- Las 25 claves coinciden letra por letra con la hoja docente; el resuelto incluye 25 marcas sobre las alternativas previstas y 25 explicaciones numeradas. El estudiante no tiene resaltados de respuestas ni marcadores de pendiente.
- Se inspeccionaron las **15 páginas del estudiante, las 18 del resuelto y la única de la clave** mediante sus renderizados. No se observaron recortes ni solapamientos en esas vistas. La comprobación automática de bloques de texto no encontró salidas de los límites físicos de página.
- El cotejo de contenido se basa en las fuentes originales inspeccionadas y en la transcripción manual. Quedan la revisión final del usuario y una impresión física; no se declara un banco validado por ello.
- `sync_used_questions.py --check-only` no detectó repeticiones exactas. Informó que el registro resultante tendría **266 preguntas**; fue solo una comprobación: el registro maestro permanece con 241 usadas y 11 reservas. La ausencia de coincidencias exactas no cierra los 40 pares de cotejo históricos que tocan la selección.
- No se modificó código del editor en esta fase. El material preparado, la imagen y los PDF permanecen locales, pendientes de revisión e integración; al repositorio se suben únicamente el informe y los códigos/estado editorial.

## Para la próxima unificación

Guardar primero el avance de Ciencias del usuario y descargar su JSON. Comparar el principal vigente con el lote de Sociales por IDs y códigos, agregar únicamente sus 25 registros y conservar las áreas ya guardadas. No sustituir el JSON principal completo ni reutilizar una fotografía antigua del principal como si fuera el estado actual. Verificar los tres PDF del proyecto reunido, incluidas las áreas anteriores; la revisión de este lote aislado no certifica el cuadernillo completo ni resuelve por sí sola el contexto largo de Lectura.
