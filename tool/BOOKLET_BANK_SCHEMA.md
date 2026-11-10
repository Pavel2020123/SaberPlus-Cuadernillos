# Esquema del banco para la plantilla

## Extensión de evaluación SP-M04

El banco anterior sigue admitido. La alternativa `booklet_competency_sample.json` incorpora `assessment_framework: "icfes-guia-2026-2"` y un objeto `assessment` por pregunta. El catálogo inicial está en `assessment_catalog.json`; no es un catálogo de niveles ni contiene conversiones de puntajes. Ver `docs/ESTADO_PLANTILLA_Y_CARGA.md` para alcance y pendientes.

Campos del objeto: `framework`, `area`, `status` (`unclassified`, `proposed`, `reviewed`), `competency`, `process` (lectura), `claim`, `evidence`, `component` (ciencias), `part` (inglés), `rationale`, `reviewer`, `reviewed_at`. Los valores no aplicables son `null`. Sin clasificar no puede tener etiquetas activas. Propuesta requiere justificación; revisada exige responsable y fecha ISO y, fuera de inglés, evidencia registrada. Los códigos se interpretan dentro del área y versión, no de forma global.

La muestra incluye 14 propuestas y 8 pendientes, no 22 clasificaciones confirmadas. Estos datos se imprimen solo en la guía docente. No hay todavía formulario web, paginación general ni reporte de desempeño del estudiante.

El archivo `booklet_template_bank.json` es la entrada editable del generador. La plantilla conserva una estructura fija de 22 ítems y produce el cuadernillo del estudiante, la hoja de respuestas y la guía docente con clave separada.

## Mapa de páginas

| Página | Contenido | Ítems |
| --- | --- | --- |
| 1 | Portada, identificación e instrucciones | - |
| 2 | Lectura crítica y Sociales y ciudadanas | 1-4 |
| 3 | Matemáticas, tabla y espacio de procedimientos | 5-7 |
| 4 | Ciencias naturales y esquema de apoyo | 8-10 |
| 5 | Inglés: vocabulario, aviso y conversación | 11-15 |
| 6 | Inglés: texto gramatical y comprensión literal | 16-19 |
| 7 | Inglés: comprensión inferencial y vocabulario en contexto | 20-22 |
| 8 | Hoja de respuestas manual | 1-22 |

La guía docente mantiene dos páginas: decisiones de plantilla y clave con tema y justificación.

## Grupos que se pueden editar

- `reading.questions`: exactamente 2 preguntas, números 1-2, cuatro opciones.
- `social`: exactamente 2 preguntas, números 3-4, cuatro opciones.
- `mathematics`: exactamente 3 preguntas, números 5-7, cuatro opciones.
- `science`: exactamente 3 preguntas, números 8-10, cuatro opciones.
- `english.words`: exactamente 7 palabras para el banco A-G.
- `english.matching`: exactamente 3 preguntas, números 11-13, clave A-G y sin lista de opciones individual.
- `english.notice`: pregunta 14, tres opciones.
- `english.conversation`: pregunta 15, tres opciones.
- `english.grammarText` y `english.grammar`: texto con `{{16}}` y `{{17}}`, más dos preguntas de tres opciones.
- `english.literalText` y `english.literal`: texto más dos preguntas, 18-19, de tres opciones.
- `english.inferenceText` y `english.inference`: texto más la pregunta 20, de cuatro opciones.
- `english.lexicalText` y `english.lexical`: texto con `{{21}}` y `{{22}}`, más dos preguntas de cuatro opciones.

Cada pregunta debe conservar estos campos:

```json
{
  "n": 1,
  "topic": "Tema o competencia",
  "stem": "Enunciado de la pregunta",
  "options": ["Opción A", "Opción B", "Opción C", "Opción D"],
  "answer": "A",
  "why": "Justificación docente de la clave."
}
```

Las preguntas de asociación 11-13 omiten `options` porque usan el banco común `english.words`; su `answer` debe ser una letra entre A y G.

## Imágenes y gráficos

Una pregunta puede incluir un recurso visual propio mediante el campo opcional `image`:

```json
{
  "n": 5,
  "topic": "Representación de datos",
  "stem": "Observa la gráfica y responde.",
  "image": {
    "path": "assets/grafica_pregunta_05.png",
    "caption": "Gráfica elaborada para esta pregunta.",
    "max_height": 150
  },
  "options": ["...", "...", "...", "..."],
  "answer": "B",
  "why": "..."
}
```

La ruta es relativa a la raíz del proyecto, las proporciones se conservan y el generador falla si no encuentra el archivo o si no cabe en el área imprimible. Usa imágenes propias o con permisos verificables; las referencias visuales no se convierten en recursos de salida.

La revisión editorial SP-M03 usa escala de grises, reglas horizontales para separar preguntas, tablas sin color de marca y una separación vertical cuando se usan dos columnas. Es una aproximación editorial inspirada en convenciones de cuadernillos impresos; no reproduce logotipos, marcas, códigos ni contenido oficial.

## Flujo para armar una versión

1. Duplica el JSON de ejemplo y cambia `title`, `version`, `disclaimer`, contextos, preguntas, opciones, claves y justificaciones.
2. Mantén los números y la cantidad de preguntas de cada grupo. No mezcles un contexto con otro grupo.
3. Ejecuta la validación sin crear archivos:

```powershell
uv run --with reportlab --with pymupdf python tool/validate_booklet_bank.py --bank tool/booklet_template_bank.json
```

4. Genera una salida versionada para conservar las anteriores:

```powershell
uv run --with reportlab --with pymupdf python tool/generate_booklet_template.py --bank tool/booklet_template_bank.json --output-suffix SP-M03
```

5. Renderiza y revisa todas las páginas antes de entregar. La validación comprueba estructura, no dificultad, calidad psicométrica, permisos ni aprobación docente.

La clave y las justificaciones permanecen en el banco y en la guía docente; no se incluyen en el PDF del estudiante. No uses preguntas, imágenes, logotipos o respuestas de las referencias sin autoría y permisos verificables.
