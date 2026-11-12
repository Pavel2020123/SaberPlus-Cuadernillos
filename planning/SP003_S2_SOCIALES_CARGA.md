# SP-003 · Segunda sesión · Sociales completa

12 de noviembre de 2026. **25 preguntas guardadas en 4188, revisión 8.** Carga autorizada por el usuario, pendiente de su revisión individual. Sociales ocupa los números 1–25 de esta sesión. Matemáticas, Ciencias e Inglés siguen sin carga: faltan 109 preguntas de la segunda sesión.

Proyecto independiente: `data/parallel/SP-003-segunda-4188/project.json`. La primera sesión conserva su archivo sin cambios: revisión 26, 120 preguntas, SHA-256 `b47ae3ab762e32fdc7fc403c9b9d7341c5486597276d38f5bc4528e7aa403388`.

## Archivos para revisar

Carpeta local `output/editor/SP003-segunda-sociales-rev8/`:

| Archivo | Contenido | Páginas |
| --- | --- | ---: |
| [cuadernillo.pdf](../output/editor/SP003-segunda-sociales-rev8/cuadernillo.pdf) | Estudiante, preguntas y hoja de respuestas sin resolver | 16 |
| [cuadernillo_resuelto.pdf](../output/editor/SP003-segunda-sociales-rev8/cuadernillo_resuelto.pdf) | Resaltados, hoja marcada y 25 explicaciones al final | 20 |
| [clave_docente.pdf](../output/editor/SP003-segunda-sociales-rev8/clave_docente.pdf) | Clave separada | 1 |
| [proyecto.json](../output/editor/SP003-segunda-sociales-rev8/proyecto.json) | Respaldo descargado de esta revisión | — |

Los PDF y el proyecto completo permanecen locales. Las 25 preguntas son texto editable sin imágenes individuales ni contextos compartidos entre ítems. El JSON no necesita recursos cargados de estas preguntas. Al continuar, agregar las otras áreas al proyecto existente; no reemplazarlo con una plantilla vacía ni importar este JSON en la primera sesión.

[25 códigos, uno por línea](SP003_S2_SOCIALES_CODIGOS_USADOS.txt). [Tabla de fuentes y justificaciones](SP003_S2_SOCIALES_CANDIDATAS_25.md). [Claves razonadas, separadas del estudiante](SP003_S2_SOCIALES_CLAVE.md). [Manifiesto sin claves para coordinación](SP003_S2_SOCIALES_ENTREGA_COORDINACION.json).

## Contenido y clasificación

Reparto comprobado sobre el JSON: **7 pensamiento social / 10 interpretación y análisis de perspectivas / 8 pensamiento reflexivo y sistémico**. Competencia y justificación editoriales presentes en los 25 registros; afirmación, evidencia y nivel sin asignar. No se atribuye validación externa.

La pregunta 16 definitiva es **`USB-1c44481d3d4a-Q007`**, ayuda alimentaria y condiciones de acceso territorial. Sustituye a `USB-7b48857ae6bc-Q067`, retirada al comprobar que la revisión 5 sumaba 7/11/7. La retirada no forma parte de las 25 usadas actuales. Sus dos apariciones equivalentes también se identifican en el manifiesto para excluirlas de otras selecciones.

Se conservan los dos fragmentos de la 8, el pasaje documental de la 9, ambos autores de la 11, el relato completo de la 16 y el **NO** de la 25. La revisión 8 solo cambia a ancho completo las preguntas 13 y 14 para mejorar los espacios de las páginas 9–11; conserva el contenido, orden y tamaño de letra de la revisión 7. Sigue habiendo espacio libre cuando el siguiente bloque completo no cabe. No se recortan pasajes para llenar páginas.

## Comprobaciones de cierre

Se inspeccionaron las 16 páginas del estudiante, las 20 del resuelto y la clave. Las páginas 9–11 de la revisión 8 se revisaron de nuevo; los demás renderizados coinciden píxel a píxel con la revisión 7 inspeccionada.

- 25 códigos únicos y 25 claves coincidentes entre selección documentada, JSON, resaltados, hoja del resuelto y clave separada; 25 explicaciones numeradas.
- Estudiante sin resaltados de respuesta ni marcadores de contenido pendiente; límites físicos del texto comprobados en los tres PDF.
- Identidad de los diez PDF fuente comprobada de nuevo por SHA-256; 22 páginas físicas seleccionadas. Las transcripciones y los cotejos visuales de originales proceden del trabajo por lotes documentado.
- Sin coincidencias de código, equivalencias conocidas ni huella textual exacta frente a lo publicado de SP-001, las 120 de primera SP-003 y las 120 de primera SP-002; consultadas también las nuevas propuestas de Sociales de segunda SP-002 y sus alias.

Tras incorporar `origin/main` **`8542df4`**, se conservaron sus 225 registros de SP-001 y los 66 publicados de SP-003: registro local **291 usadas / 11 reservas**. La incorporación conserva los cambios publicados de numeración de Inglés. **No se añadieron estas 25 al maestro**: el coordinador debe integrarlas desde el JSON y el manifiesto. SP-002 consultado en **`dfbe592`**. Se resolvieron los conflictos de documentación y del registro sin escribir en los proyectos guardados.

Comando ejecutado:

```powershell
uv run --offline python -B tool/sync_used_questions.py output/editor/SP003-segunda-sociales-rev8/proyecto.json --session segunda --check-only
```

Resultado: **sin repeticiones exactas; 316 registros en la integración hipotética**. El cotejo amplía este control con las apariciones equivalentes identificadas en la selección. La cola del catálogo todavía contiene 12 pares que tocan estos grupos: fueron cotejados localmente en el trabajo previo, con 11 equivalencias y un par descartado; no se altera la cola global ni se certifica unicidad de toda la colección.

Evidencia local: `revision-salidas.json` y `cotejo-cierre.json` junto a los PDF; scripts y renders en `tmp/sp003/segunda/carga/`. No se afirma prueba interactiva de navegador ni impresión física. La revisión individual del usuario permanece pendiente.

## Continuación

Cerrar primero la revisión del usuario de Sociales. Antes de cargar otra área, volver a consultar main y las reservas: SP-002 primera ya utiliza tres de nuestras propuestas iniciales de Ciencias (`USB-524d98b0a234-Q061`, `USB-709bc037689b-Q051`, `USB-e4489f150183-Q063`). Esas tres propuestas de SP-003 quedan retiradas de la carga pendiente y requieren reemplazos; no se altera el trabajo de SP-002. Matemáticas conserva además su cotejo visual pendiente frente a las 25 finales de primera SP-001. No se empieza otra área en este cierre.
