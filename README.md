# SaberPlus - Cuadernillos

Proyecto independiente para diseñar y generar cuadernillos de práctica en PDF.

## Punto de continuación actual

SP-003: Matemáticas tiene **25 preguntas guardadas**, revisión 17 del editor principal; ver [carga de 17–25 y límites de verificación](planning/SP003_LOTE_17_25_CARGA.md). Lectura dispone de [41 candidatas en 13 grupos completos](planning/SP003_S1_LECTURA_CANDIDATAS_41.md), con [códigos completos para copiar](planning/SP003_S1_LECTURA_CODIGOS.txt) y clave aparte; su clasificación por procesos y coordinación siguen pendientes.

SP-003 Ciencias: [29 candidatas con fuentes, páginas y recursos](planning/SP003_S1_CIENCIAS_CANDIDATAS_29.md), [códigos completos](planning/SP003_S1_CIENCIAS_CODIGOS.txt) y clave aparte. Propuesta publicada para coordinación; sin carga en los editores. Totales propuestos 9/9/11 por competencia y 9/9/8/3 por componente; cruce interno pendiente de revisión.

Edición simultánea de SP-003: el principal de Matemáticas permanece en http://127.0.0.1:4185/ y el usuario dispone de http://127.0.0.1:4186/ con proyecto vacío y guardado independiente para otra área. El segundo se abre con `uv run --offline python -B tool/editor_parallel.py --port 4186 --workspace SP-003-usuario`. Ver [trabajo simultáneo y posterior integración](docs/EDITOR_LOCAL.md#trabajar-al-mismo-tiempo--sp-003).

Trabajo en equipo SP-001/SP-002/SP-003: [prompt para compañeros](planning/PROMPT_COMPANEROS_SP002_SP003.md), [registro global de uso y reservas](planning/PREGUNTAS_USADAS_GLOBAL.json) y [cuatro proyectos iniciales vacíos](planning/starter_projects/). Cada simulacro tiene 254 puestos en dos sesiones (120/134). SP-001 tiene 25 preguntas de Matemáticas y 41 de Lectura crítica cargadas; se completó la meta de Lectura. El registro compartido marca esas 66 preguntas como usadas y no mantiene reservas de SP-001. Los 41 códigos de Lectura usados están fuera de la selección de SP-002 y SP-003. Los 25 códigos USB de Matemáticas aún requieren cotejo. Ver [grupos completos de Lectura](planning/SP001_S1_LECTURA_GRUPOS_COMPLETOS.md). El coordinador actualiza el registro desde un JSON guardado con `tool/sync_used_questions.py` y comparte el commit antes del siguiente lote. Los PDF generados y las imágenes cargadas permanecen locales.

Ecuaciones y composición: [uso y límites del motor matemático](docs/ECUACIONES_Y_MAQUETACION.md). Fórmulas vectoriales con raíces, fracciones, índices y sucesiones; opciones en cuadrícula y controles manuales sin migrar preguntas. Instala el entorno con `uv sync` y ejecuta `uv run --offline python -B tool/editor_server.py`.

10 de noviembre: [matriz editorial SP-001 de las dos sesiones](docs/SP001_MATRIZ_COBERTURA.md). Plan de 254 puestos académicos (120/134), cuotas por objetivo, cruce de Ciencias y adaptación explícita de Inglés. El archivo `planning/SP001_MATRIZ_COBERTURA.json` es planificación, no un banco importable: todavía no tiene preguntas seleccionadas. Comenzar con el lote de cinco candidatos de Matemáticas indicado en esa matriz. La muestra de tamaños y el editor de prueba separado se describen en [EDITOR_LOCAL.md](docs/EDITOR_LOCAL.md).

31 de octubre: consultar primero [cotejo de preguntas y pendientes reales](docs/COTEJO_PREGUNTAS_ESTADO_ACTUAL.md). Se consolidaron 70 fichas adicionales: quedan 2764 fichas académicas y 723 apariciones académicas exactas enlazadas. El índice editorial está en `output/cotejo_30/INDICE.html`, con copia en la USB. Aún no se certifican preguntas únicas ni existe un banco importable completo: quedan cotejos visuales, transcripción de contenido, revisión docente y permisos. Los conteos de cierre anteriores son históricos.

Auditoría activa de la USB PAVEL: consultar [catálogo y punto de continuación](docs/CATALOGO_USB.md). La documentación manual de preguntas y el OCR son procesos distintos; no afirmar que toda la colección esté analizada. Este trabajo no modifica la app ni el editor.

Leer [editor local y prueba de carga](docs/EDITOR_LOCAL.md) y [análisis de competencias y niveles](docs/COMPETENCIAS_ICFES_2025_2026.md). Ya existe un primer editor local con imágenes, contextos compartidos y vista previa automática mediante el motor PDF. La muestra fija SP-M04 y sus documentos anteriores son antecedentes, no el diseño final aprobado.

## Probar el editor

```powershell
uv run --with reportlab --with pymupdf --with pillow python tool/editor_server.py
```

Abre http://127.0.0.1:4185. El apartado **Así va tu cuadernillo** actualiza las páginas al hacer una pausa al escribir, permite navegar y ampliar. No guarda automáticamente: usa **Guardar proyecto**. Para probar con contenido original de demostración, abre **Distribución prevista y respaldo del proyecto** y carga la muestra; esta acción reemplaza el proyecto actual y pide confirmación. Las siete partes de inglés se encuentran al elegir segunda sesión.

El editor sigue siendo un prototipo editorial: faltan aprobación visual conjunta, revisión editorial del banco y completar el catálogo parcial de evidencias. El equipo SaberPlus clasifica el contenido sin exigir aprobación de un docente ni atribuir validación externa. Bloques compartidos demasiado largos todavía requieren división manual; no se recortan para hacerlos caber.

**Generar los 3 PDF** produce el cuadernillo sin resolver, el resuelto con explicaciones al final y la clave del profesor. Las hojas usan círculos con letras: vacíos para el estudiante y rellenos para la clave. No hay QR ni publicación en internet todavía.

## Continuar en un nuevo chat

Abre esta carpeta como proyecto en Codex y escribe:

> Lee AGENTS.md, README.md y CONTEXTO.md. Continuemos con la plantilla de cuadernillos.

No es necesario copiar la conversación anterior: sus decisiones y pendientes están en CONTEXTO.md. Un chat nuevo no hereda automáticamente todo el historial; estos archivos son el relevo.

## Archivos

- `output/pdf/SaberPlus_muestra_cuadernillo.pdf`: muestra de estudiante, 8 páginas y 22 preguntas.
- `output/pdf/SaberPlus_guia_plantilla_y_clave.pdf`: guía editorial y clave, 2 páginas.
- `output/pdf/SaberPlus_muestra_cuadernillo_SP-M02.pdf`: revisión visual versionada de la muestra.
- `output/pdf/SaberPlus_guia_plantilla_y_clave_SP-M02.pdf`: guía y clave correspondientes a SP-M02.
- `output/pdf/PLANTILLA_CUADERNILLOS.md`: especificación y límites del prototipo.
- `tool/booklet_template_bank.json`: preguntas editables.
- `tool/BOOKLET_BANK_SCHEMA.md`: mapa de páginas, grupos y campos editables.
- `tool/generate_booklet_template.py`: generador de muestra.
- `tool/validate_booklet_bank.py`: validación del banco sin crear PDF.
- `tool/review_booklet_template.py`: renderizado y comprobación de límites de texto.
- `references/`: copias de los 13 PDF aportados para estudiar su estructura.

La revisión SP-M03 cambia la propuesta visual a escala de grises, incorpora reglas horizontales para separar preguntas, un separador vertical en la composición de dos columnas y soporte para imágenes propias mediante el campo opcional `image` del banco. No reproduce logotipos, marcas, códigos ni contenido oficial.

- `output/pdf/SaberPlus_muestra_cuadernillo_SP-M03.pdf`: revisión monocromática de la muestra.
- `output/pdf/SaberPlus_guia_plantilla_y_clave_SP-M03.pdf`: guía y clave correspondientes a SP-M03.

## Ejecutar

Con `uv` instalado, desde esta carpeta:

```powershell
uv run --with reportlab --with pymupdf python tool/validate_booklet_bank.py --bank tool/booklet_template_bank.json
uv run --with reportlab --with pymupdf python tool/generate_booklet_template.py
uv run --with reportlab --with pymupdf python tool/review_booklet_template.py
```

Para generar una revisión sin reemplazar los PDF anteriores, usar por ejemplo `--output-suffix SP-M02`.

La primera ejecución puede descargar dependencias. Los PDF salen en `output/pdf/` y las imágenes de revisión en `tmp/pdfs/`. La regeneración reemplaza únicamente los dos PDF de muestra con esos nombres; guardar versiones aprobadas con otro nombre antes de regenerar.

No requiere Flutter, backend, Docker ni USB. No está integrado con el banco de la app. No se ha inicializado Git ni publicado nada.
