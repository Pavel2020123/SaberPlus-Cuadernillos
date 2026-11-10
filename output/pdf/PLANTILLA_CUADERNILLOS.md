# SaberPlus - Prototipo de cuadernillos

## Entregables

- `SaberPlus_muestra_cuadernillo.pdf`: 8 páginas, 22 preguntas originales propuestas, cinco áreas y hoja de respuestas manual.
- `SaberPlus_guia_plantilla_y_clave.pdf`: 2 páginas con decisiones de diseño, controles editoriales y clave explicada.
- `SaberPlus_muestra_cuadernillo_SP-M02.pdf`: revisión visual versionada de la muestra, sin cambios en el banco de preguntas.
- `SaberPlus_guia_plantilla_y_clave_SP-M02.pdf`: guía y clave correspondientes a la revisión SP-M02.

Es una muestra para aprobar presentación, no un banco comercial terminado, una prueba oficial ni un instrumento validado.

- `SaberPlus_muestra_cuadernillo_SP-M03.pdf`: revisión monocromática con separadores e imágenes opcionales.
- `SaberPlus_guia_plantilla_y_clave_SP-M03.pdf`: guía y clave correspondientes a SP-M03.

## Revisión de referencias

Se consultaron metadatos y páginas representativas de los 13 PDF compartidos: portada, páginas interiores y páginas cercanas al final. No se hizo una auditoría completa de todas sus preguntas ni se verificó la procedencia o autenticidad que sugieren sus nombres.

- Los archivos S11-M/O/P/R/S/T muestran portadas de evaluación, cuadros de distribución, interiores compactos con dos columnas y bloques especiales de inglés. Los tamaños físicos y la calidad del escaneo varían.
- La primera sesión 2024 también presenta páginas con tablas, gráficos y preguntas en una sola columna.
- Una de las compilaciones 2024 incluye preguntas reducidas o repetidas en la misma página: no se adopta como patrón de legibilidad.
- Varios originales incluyen respuestas resaltadas, marcas de escáner o marcas de terceros. No se incorporan a la muestra.

No se ha determinado cuáles archivos pertenecen al Grupo 500. No se reproduce su marca ni se afirma que esta muestra sea de ese grupo.

Como consulta adicional, se revisaron en modo solo lectura 47 PDF proporcionados en una carpeta externa: 46 archivos únicos y una copia exacta. Se compararon renders representativos de portada, interior y cierre, además de páginas detalladas de cuadernillos escaneados y digitales. La observación se limitó a composición, densidad, columnas, tablas, gráficos, partes de inglés y hojas de respuestas; no se copió contenido ni identidad visual de terceros.

## Revisión visual SP-M03

- Se eliminó el acento azul de la propuesta anterior y se adoptó una escala de grises de alto contraste.
- Cada pregunta tiene reglas horizontales de separación; la lectura en dos columnas incluye una regla vertical central.
- Las tablas, avisos y bloques usan bordes y fondos neutros para conservar legibilidad al imprimir en blanco y negro.
- Se agregó soporte para `image` en las preguntas: ruta relativa al proyecto, escala proporcional, pie opcional y error explícito si falta el archivo o no cabe.
- La aproximación toma convenciones editoriales observadas en las referencias, pero conserva identidad SaberPlus y no reproduce marcas, códigos ni contenido oficial.

## Revisión visual SP-M02

- Portada con tarjetas de edición, cantidad de ítems, áreas y uso.
- Encabezados de tabla con mayor contraste y bandas de sección con acento lateral.
- Instrucción explícita para rellenar manualmente un solo círculo por pregunta.
- Salidas versionadas para conservar la muestra anterior y comparar las dos propuestas.

## Estructura propuesta

1. Portada con identificación, versión, distribución de preguntas e instrucciones.
2. Bloques de área con contextos compartidos y numeración continua.
3. Alternancia de una y dos columnas según la longitud y los recursos gráficos.
4. Inglés: vocabulario, avisos, conversaciones, texto gramatical con espacios, comprensión literal, comprensión inferencial y vocabulario en contexto.
5. Hoja de respuestas con las opciones realmente disponibles por ítem.
6. Archivo docente separado con clave, justificación y cobertura.

El esquema editable completo, con el mapa de páginas, los grupos y el flujo para reemplazar preguntas, está en `tool/BOOKLET_BANK_SCHEMA.md`. Antes de generar se puede ejecutar `tool/validate_booklet_bank.py`; la validación comprueba la estructura fija, las opciones, las claves y los marcadores de los textos de inglés.

La proporción de preguntas de esta muestra, el orden de las áreas y la cantidad de ítems por parte de inglés son decisiones del prototipo, no una reproducción de la distribución oficial. La dificultad de los ejemplos no se ha calibrado.

## Regeneración local

Desde la raíz del proyecto:

```powershell
uv run --with reportlab --with pymupdf python tool/generate_booklet_template.py
uv run --with reportlab --with pymupdf python tool/review_booklet_template.py
```

Para generar una versión sin reemplazar salidas anteriores:

```powershell
uv run --with reportlab --with pymupdf python tool/generate_booklet_template.py --output-suffix SP-M02
```

El banco editable está en `tool/booklet_template_bank.json`. El generador admite `--bank` para un archivo alternativo con el mismo esquema. La plantilla actual es de muestra fija: exige preguntas 1-22 y grupos concretos; no selecciona automáticamente cientos de preguntas ni pagina un banco arbitrario. Al cambiar textos, valida el esquema y falla si se excede la zona imprimible en vez de recortarlos silenciosamente. Siempre revisar los PNG de `tmp/pdfs/` después de regenerar.

Los PDF se generan con texto seleccionable y vectores, no pegando capturas del material de referencia. No hay cambios de app, datos de estudiantes, Docker ni servicios.

## Siguiente etapa, tras aprobar el diseño

Definir con el profesor el tamaño de los cuadernillos, áreas, temas, competencias, dificultad deseada y número de versiones. Diseñar un banco independiente con identificadores estables, autoría/permisos, contextos, recursos gráficos, opciones, clave y explicación. Incorporar selección por cobertura, paginación automática, conservación de contextos, control de duplicados y regeneración sincronizada de claves. Revisión docente y prueba impresa antes de comercializar o aplicar.
