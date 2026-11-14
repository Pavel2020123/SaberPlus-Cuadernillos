# Auditoría y respaldo de SP-001, segunda sesión

Fecha: 12/11/2026. Estado auditado: revisión 89, guardada explícitamente mediante el editor local del puerto 4188. Esta auditoría corresponde a la sesión 2; no modifica la sesión 1, Flutter, backend, servicios externos ni PDF originales.

## Resultado de integridad y recuperación

| Comprobación | Resultado |
| --- | --- |
| Preguntas guardadas e incluidas | 134 de 134 |
| Sociales | 25, puestos 1–25 |
| Matemáticas | 25, puestos 26–50 |
| Ciencias | 29, puestos 51–79 |
| Inglés | 55, puestos 80–134 |
| Códigos de catálogo únicos | 134; sin códigos repetidos |
| Identificadores internos | Sin duplicados |
| Repetición exacta de contenido completo | No detectada; comparación incluye contexto, hueco, opciones e imágenes |
| Candidatos con similitud textual superior a 0,88 | Ninguno con el umbral y longitud mínima empleados; no certifica equivalencias entre todos los escaneos |
| Imágenes vinculadas | 93 de 93 presentes, decodificables y copiadas con SHA-256 coincidente |
| Imágenes idénticas por bytes con nombres distintos | Ninguna entre las 93 vinculadas |
| Registro global | Coinciden los 134 códigos de SP-001 segunda sesión |
| Validación del modelo | Sin errores ni avisos de estructura |
| Recuperación aislada | Los PDF se generaron desde el motor y las imágenes COPIADOS al respaldo |
| Clave docente | 134 marcas coinciden, en orden, con el JSON |
| Explicaciones del resuelto | 134 encabezados y claves cotejados con el JSON |
| Resaltados del estudiante | Sin resaltados amarillos de respuestas; los ejemplos resueltos pertenecen al formato |
| Pruebas del proyecto | 132 pruebas existentes aprobadas; además, 11 de integridad ejecutadas por separado |

El cotejo de claves prueba concordancia interna, no que toda clave sea editorialmente inequívoca. Los contextos repetidos de un grupo no son preguntas duplicadas. Ciencias conserva los grupos 56–58 y 76–78 con un contexto por grupo. Inglés conserva todos sus bloques y huecos, sin preguntas vacías para completar el conteo.

## Sentido y organización de la sesión

El orden Sociales → Matemáticas → Ciencias → Inglés coincide con el perfil del editor. La portada actual muestra 25/25/29/55 y cuatro horas y treinta minutos. Ciencias mantiene la distribución prevista: 9 uso comprensivo, 8 explicación y 12 indagación. Inglés usa el reparto editorial vigente **5/5/5/8/7/5/20**, documentado en `docs/ACTUALIZACION_INGLES_EQUIPO.md`; el reparto histórico por porcentajes no es un faltante.

Se revisaron la organización, la concordancia de claves con explicaciones y los principales razonamientos y alertas existentes. No se rehízo el cotejo de todas las transcripciones con cada PDF fuente ni se efectuó aplicación piloto o impresión física. Las categorías editoriales continúan como propuestas, sin validación externa atribuida.

## Hallazgos que impiden declarar listo el PDF para aplicación

Se inspeccionaron las 60 páginas del estudiante mediante diez láminas de seis páginas, las 21 páginas añadidas de explicaciones del resuelto mediante láminas y las tres páginas de clave. También se revisaron vistas individuales de casos relevantes. El análisis automático no encontró texto fuera de los límites físicos, pero NO detecta texto recortado dentro de una imagen.

| Prioridad | Pregunta / página del estudiante | Hallazgo y acción pendiente |
| --- | --- | --- |
| Alta | 51 / p.30 | Encabezado de temperatura de la tabla recortado. Restaurar desde el original con la herramienta de imágenes, conservando números y unidad K. |
| Alta | 53 / p.31 | Encabezados de la tabla de cultivos se superponen o recortan dentro de la imagen. Mejorar el original; preservar datos completos. |
| Alta | 57 / p.34 | Recuadros sustituyen los dibujos originales y sus textos se superponen. Recuperar las alternativas originales con la herramienta de imágenes y cotejar la secuencia. |
| Alta | 39 / p.22 | Matemáticas 14 del lote anterior: B es la clave prevista, pero D también expresa un cálculo compatible; además la proyección supone suministro y tasa constantes. Requiere decisión editorial. |
| Alta | 49 / p.28 | Matemáticas 24 del lote anterior: B contiene puntos con correlación positiva aunque su línea sea horizontal; D es la prevista por la recta. Persisten ruido y letras originales. Revisar ambigüedad e imagen. |
| Media | 9 y 21 / pp.6 y 12 | CO₂ se presenta con cuadrados en algunos textos. La extracción de texto no basta para aprobar subíndices. Usar el motor matemático existente al corregir formato. |
| Media | 72 / explicación del resuelto p.73 | Los subíndices de F23 y F13 se ven como cuadrados en la explicación; el gráfico sí conserva los rótulos. Corregir solo el formato. |
| Media | 33, 38 y 44 / pp.19, 21 y 26 | Fracciones, radicales y expresiones de opciones pequeños. Revisar tamaño de impresión. |
| Media | 52 y 59–62 / pp.30, 35–38 | Se usaron reconstrucciones por código antes de la instrucción del usuario. Deben sustituirse por mejoras de originales; las curvas/barras aproximadas de 60 y 62 no son datos crudos exactos. |
| Media | Contexto 56–58 / p.33; 55 / p.32 | Conserva textura y un borde ajeno en el modelo de metales; pendiente cotejo detallado de la gráfica presión-volumen. |
| Media | 75 / p.47 | Los números y agujas de las imágenes mejoradas se cotejaron ampliados, pero los cuatro modelos quedan pequeños al imprimir. Ampliar sin omitir el enunciado ni modificar silenciosamente la arquitectura. |
| Editorial | 40 / p.23 | La opción C conserva «recaudado» donde se discute «dejado de recaudar»; la explicación registra la imprecisión. No corregir el original silenciosamente. |
| Editorial | 60 y 79 / pp.36 y 49 | C de 60 afirma «ninguna relación», más fuerte que la ausencia de tendencia observada. En 79, B también ordena tamaños por sectores; C es la representación de tiempos prevista. Mantener observaciones y revisar unicidad. |
| Editorial | 70 y 71 / pp.44 y 45 | Se conservan las imprecisiones originales «contrapeso de aluminio de 0,1 g/mL» y «Cigoto n» sin fertilización; las explicaciones documentan su alcance. |
| Diseño | Hojas pp.58–60; clave pp.1–3 | Numeración completa, pero la última columna queda vacía o muy desequilibrada. Mejorar distribución antes de entregar. |
| Diseño | Inglés pp.54–57 | Lecturas compactas; ilustración Spider-Wedding conserva textura. Verificar impresión a tamaño real. |

La clave de la pregunta 75 es **B**, corregida desde la A de la propuesta inicial al cotejar temperatura y presión. La corrección está en el JSON, la selección y la explicación; no se cambió el catálogo global de fuentes.

## Copia recuperable

Carpeta: `handoff/SP001_segunda_completa_2026-11-12_rev89/`.

Incluye JSON de las 134 preguntas, 93 imágenes vinculadas, imágenes de portada, motor del editor, dependencias fijadas, documentos de contexto, PDF de estudiante/resuelto/clave/guía, auditoría y verificador de integridad. El ZIP acompaña la carpeta y se verifica leyendo todos sus archivos y sus hashes tras extraerlo en una ubicación aislada.

Los PDF incluidos son la fotografía auditada **con los pendientes anteriores**, no una edición corregida aprobada. `proyecto.json` contiene claves y explicaciones privadas. Las imágenes mantienen sus rutas relativas: el JSON solo no constituye un respaldo completo.

Para restaurar, leer `LEEME_RESTAURAR.md` y ejecutar `verificar_respaldo.py` dentro de la carpeta extraída antes de importar o abrir. El respaldo no depende de la USB para editar las preguntas guardadas. Los originales y el catálogo global no se incluyen como parte del motor recuperable.

No se ejecutó nuevo commit o push de este paquete: el último push autorizado de códigos fue `d26052b` en `main`. Los paquetes anteriores de Inglés o Matemáticas+Inglés se conservan como antecedentes, no como respaldo de las 134 preguntas.
