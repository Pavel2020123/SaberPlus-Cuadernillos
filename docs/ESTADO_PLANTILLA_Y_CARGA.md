# Estado y siguiente paso: carga de preguntas

> Actualización: ya se construyó el primer editor local, con vista previa automática. El estado vigente y la guía de prueba están en [EDITOR_LOCAL.md](EDITOR_LOCAL.md). Los apartados de este documento que describen un panel pendiente corresponden al hito anterior SP-M04.

## Decisiones guardadas

- Primer simulacro: código **SP-001**, primera sesión. No confundir este código de producto con las revisiones SP-M03/SP-M04 de la muestra de 22 ítems.
- Portada propia con Sabi, encabezado solo «SaberPlus», esquinas suaves y Sabi enteramente dentro del fondo. Pie «SP-001 · Primera sesión», S+ pequeña gris y numeración. Archivo actual: `output/pdf/SaberPlus_portada_e_indicaciones_SP-001_ajustada.pdf`.
- Las cantidades y el tiempo siguen pendientes. La portada aún es independiente del generador de muestra; no se ha construido un simulacro completo SP-001.
- Hay ilustraciones distintas de Sabi y una colección de lectura, matemáticas, ciencias y logro en `assets/sabi/coleccion_01/`.
- Mantener orden de sesión y partes de inglés según el perfil de referencia elegido; no mezclar áreas como en una muestra multipropósito ni inferir reglas universales a partir de cualquier PDF.
- El análisis de las cuatro guías, el reporte escolar y el Excel está en `COMPETENCIAS_ICFES_2025_2026.md`. Incluye la distinción entre puntaje, percentil, nivel y habilidades del reporte individual. No guarda registros ni puntajes personales.

## Implementado ahora, solo en cuadernillos

- `tool/assessment_catalog.json`: catálogo inicial versionado según la guía 2026-2, con competencias de las cinco áreas, procesos de lectura, afirmaciones, componentes de ciencias y siete partes/habilidades de inglés. Las etiquetas de afirmaciones son resúmenes; la fuente y páginas se conservan. Las evidencias de ciencias se cargaron parcialmente y esa limitación es explícita.
- `tool/assessment_metadata.py`: valida relaciones y estados. Cada ítem puede conservar área/versión, competencia, proceso, afirmación, evidencia, componente, parte, justificación y revisión. No genera resultados, niveles o percentiles.
- La muestra alternativa `tool/booklet_competency_sample.json` mantiene las preguntas originales, sin cambiar enunciados, claves ni numeración. Contiene 14 propuestas de clasificación y 8 preguntas sin clasificar. CERO revisiones docentes confirmadas. Las propuestas incluyen un ejemplo de lectura, uno de matemáticas y las partes de inglés.
- El generador acepta los bancos anteriores sin asignarles competencias implícitas. Con el nuevo esquema añade páginas de clasificación a la guía docente; no imprime esos metadatos en el PDF del estudiante.
- La validación comprueba consistencia de datos, no corrección pedagógica ni validación psicométrica. El estado «revisada» exige responsable y fecha; las áreas distintas de inglés requieren evidencia registrada. No hay todavía flujo de publicación comercial.

## Ejecutar y comprobar

```powershell
uv run --with reportlab python tool/generate_booklet_template.py --bank tool/booklet_competency_sample.json --output-suffix SP-M04
uv run --with reportlab python -m unittest discover -s tool -p "test_assessment_metadata.py" -v
```

## Panel que debemos construir después

Actualmente NO existe un formulario web para que el usuario cargue preguntas. No dar a entender que el JSON ya es ese panel. El formulario debe ofrecer:

1. Contenido: área, tema/subtema, enunciado y opciones; imágenes propias o autorizadas; clave y explicación docente.
2. Contexto compartido: texto, imagen o tabla que se vincula a varias preguntas sin duplicarlo. Esto incluye banco de palabras y lecturas de inglés.
3. Clasificación: fuente/versionado y selectores dependientes de área, competencia/proceso, afirmación/evidencia; componente de ciencias; parte de inglés. Permitir borrador sin clasificar.
4. Revisión: justificación, estado, responsable y fecha; alertas de campos faltantes y revisión de clasificación.
5. Armado: elegir perfil de sesión, orden y cantidades; seleccionar preguntas y revisar cobertura por contenidos y clasificación. El motor actual sigue siendo fijo de 22 ítems, no resuelve este armado general.
6. Vista previa y generación: portada aprobada + interiores + hoja de respuestas; guía docente aparte. Paginación que conserve contexto/preguntas, imágenes legibles y numeración sincronizada.

## Pendientes reales

Editor visual; catálogo completo de evidencias con descripciones; revisión docente de clasificaciones; perfiles de sesiones y cantidades; selección y paginación general; integración de la portada aprobada con los interiores; imágenes de contexto/opciones en todos los formatos; matriz de cobertura y exportación general. La app requiere cambios separados de modelo, snapshots y analítica: solo se documentaron, no se implementaron.
