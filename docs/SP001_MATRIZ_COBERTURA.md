# SP-001: matriz editorial de las dos sesiones

Fecha: 10 de noviembre de 2026. Estado de este archivo de planificación: 254 puestos creados sin asignaciones en su JSON. La copia de trabajo posterior contiene 25 preguntas incluidas de Matemáticas y 41 de Lectura crítica de primera sesión; su uso está documentado en `planning/PREGUNTAS_USADAS_GLOBAL.json`. El plan y el proyecto del editor son archivos distintos. La meta del editor de 25/41 para estas áreas ya está cubierta.

Decisión vigente del usuario: usar exclusivamente preguntas presentes en su colección de PDF. No redactar preguntas nuevas ni cambiar datos para crear variantes. Las cinco propuestas originales preparadas antes quedan retiradas del plan activo; se conservan solo como antecedente. Selección inicial de fuentes en [SP001_LOTE01_FUENTES_PDF.md](../planning/SP001_LOTE01_FUENTES_PDF.md).

El archivo operativo es [planning/SP001_MATRIZ_COBERTURA.json](../planning/SP001_MATRIZ_COBERTURA.json): contiene 254 puestos, no 254 preguntas redactadas ni clasificadas. No se debe importar como proyecto del editor. No modifica el proyecto guardado, la demostración ni las fuentes PDF.

## 1. Referencia y límites

Referencia: `17-marzo-guia-de-orientacion-saber-11-2026-2.pdf`, aportada por el usuario. Estructura en p. 12; Matemáticas p. 38; Lectura pp. 39-45; Sociales p. 53; Ciencias pp. 61-62; Inglés pp. 63-65.

- Los porcentajes proceden de la guía. Las cantidades enteras, su reparto entre sesiones y el orden editorial son decisiones de planificación de SaberPlus, no cuotas oficiales por sesión o por ítem.
- Son 254 preguntas académicas. Se excluyen los cuestionarios socioeconómico y de clima escolar; por ello, no se reproducen los totales oficiales de 143/159 incluyendo auxiliares.
- Tiempo de práctica: 270 minutos por sesión. Código visible: SP-001, identificado como primera o segunda sesión; los IDs internos de puestos no cambian ese código.
- Una cuota no acredita dificultad calibrada, permisos de reproducción ni clasificación pedagógica correcta. Cada pregunta necesita revisión propia.

## 2. Orden y numeración provisional

| Sesión | Área | Cantidad | Rango provisional |
| --- | --- | ---: | --- |
| Primera | Matemáticas | 25 | 1-25 |
| Primera | Lectura crítica | 41 | 26-66 |
| Primera | Sociales y ciudadanas | 25 | 67-91 |
| Primera | Ciencias naturales | 29 | 92-120 |
| Segunda | Sociales y ciudadanas | 25 | 1-25 |
| Segunda | Matemáticas | 25 | 26-50 |
| Segunda | Ciencias naturales | 29 | 51-79 |
| Segunda | Inglés | 55 | 80-134 |

Total: primera 120, segunda 134, conjunto 254. La numeración comienza en 1 en cada sesión. Los contextos deben permanecer juntos; el orden provisional puede ajustarse dentro del área o parte al seleccionar preguntas, sin cambiar las cuotas. El generador asigna los números finales, no los IDs de este plan.

## 3. Competencias, procesos y redondeo

Para Matemáticas y Ciencias se aproxima la distribución global antes de repartir entre sesiones. En los empates de redondeo se fija una elección editorial explícita: en Matemáticas, 22 de formulación/ejecución y 11 de argumentación; en Ciencias, 18 de uso comprensivo y 17 de explicación. No se exige que cada sesión reproduzca exactamente el porcentaje global.

| Área | Objetivo | % guía | Primera | Segunda | Total |
| --- | --- | ---: | ---: | ---: | ---: |
| Matemáticas | Interpretación y representación | 34 | 9 | 8 | 17 |
| Matemáticas | Formulación y ejecución | 43 | 11 | 11 | 22 |
| Matemáticas | Argumentación | 23 | 5 | 6 | 11 |
| Lectura | Información local | 25 | 10 | 0 | 10 |
| Lectura | Articulación y sentido global | 42 | 17 | 0 | 17 |
| Lectura | Reflexión y evaluación | 33 | 14 | 0 | 14 |
| Sociales | Pensamiento social | 30 | 8 | 7 | 15 |
| Sociales | Interpretación y análisis de perspectivas | 40 | 10 | 10 | 20 |
| Sociales | Pensamiento reflexivo y sistémico | 30 | 7 | 8 | 15 |
| Ciencias | Uso comprensivo del conocimiento científico | 30 | 9 | 9 | 18 |
| Ciencias | Explicación de fenómenos | 30 | 9 | 8 | 17 |
| Ciencias | Indagación | 40 | 11 | 12 | 23 |

Lectura tiene una competencia lectora, tres procesos y afirmaciones asociadas. Los porcentajes de la p. 45 se presentan por afirmación; no crear tres competencias independientes.

### Cruce de Ciencias: las mismas 58 preguntas, no preguntas adicionales

La tabla 31 de la guía cruza competencia y componente. Nuestra aproximación entera conjunta es:

| Objetivo | Biológico | Físico | Químico | CTS | Total |
| --- | ---: | ---: | ---: | ---: | ---: |
| Uso comprensivo | 6 | 5 | 5 | 2 | 18 |
| Explicación | 5 | 5 | 5 | 2 | 17 |
| Indagación | 7 | 7 | 7 | 2 | 23 |
| Total | 18 | 17 | 17 | 6 | 58 |

El JSON conserva también el desglose de cada sesión: primera 9/9/8/3 y segunda 9/8/9/3 por componente. Las matrices enteras internas se distribuyen así, en orden biológico/físico/químico/CTS:

- Primera: uso `[3,2,3,1]`, explicación `[3,3,2,1]`, indagación `[3,4,3,1]`.
- Segunda: uso `[3,3,2,1]`, explicación `[2,2,3,1]`, indagación `[4,3,4,1]`.

## 4. Inglés: adaptación editorial explícita

La tabla 32 asigna 11/11/11/18/16/11/22 %. Su redondeo sobre 55 da 6/6/6/10/9/6/12. Sin embargo, la descripción de la p. 64 indica cinco descripciones y siete palabras en la parte 1. Para conservar ese bloque se planifican cinco preguntas allí y se desplaza una a la parte 7. Esto es una adaptación de SaberPlus; no afirmar que la guía fija estos enteros.

| Parte | Formato | Letras | Cantidad | Rango provisional de segunda sesión |
| --- | --- | --- | ---: | --- |
| 1 | Asociación de vocabulario | A-G | 5 | 80-84 |
| 2 | Avisos y señales | A-C | 6 | 85-90 |
| 3 | Conversaciones | A-C | 6 | 91-96 |
| 4 | Texto con espacios: gramática | A-C | 10 | 97-106 |
| 5 | Lectura literal | A-C | 9 | 107-115 |
| 6 | Lectura inferencial | A-D | 6 | 116-121 |
| 7 | Texto con espacios: gramática y léxico | A-D | 13 | 122-134 |
| Total | | | 55 | |

La cantidad por parte no obliga a una única lectura larga. Se pueden usar varios contextos adecuados para las partes 4-7. Conservar lecturas, bancos, ejemplos resueltos y sus preguntas vinculadas, sin duplicar recursos por ítem. El ejemplo no cuenta como pregunta calificada.

## 5. Contenidos que debemos buscar, sin inventar cuotas por subtema

- Matemáticas: estadística, geometría y álgebra/cálculo; contenidos genéricos y no genéricos; situaciones personales, laborales, sociales y matemáticas/científicas (pp. 34-37).
- Lectura: textos continuos y discontinuos, literarios e informativos. La tabla 22 (p. 44) da 24 % literario continuo, 30 % informativo filosófico, 30 % informativo no filosófico, 8 % literario discontinuo y 8 % informativo discontinuo. El número de textos y el cruce por proceso se cerrarán al revisar los contextos disponibles; estos porcentajes son de preguntas, no de textos.
- Sociales: modelos y conceptos; Estado y participación; dimensiones históricas/geográficas; análisis de fuentes y perspectivas; relaciones entre dimensiones y efectos de intervenciones (pp. 47-52).
- Ciencias: conceptos biológicos, físicos y químicos, y temáticas CTS (p. 61), cruzados con la tarea cognitiva exigida por cada ítem.
- Inglés: habilidades y formatos de cada parte, no niveles asignados por una tasa de aciertos.

No cerrar una cuota para cada tema de nuestro catálogo como si fuera oficial: la guía no fija cantidades para cada subtema editorial. Completar afirmación/evidencia solo tras revisar el contenido de la pregunta. El catálogo existente de evidencias de Ciencias sigue siendo parcial.

## 6. Cómo llenar un puesto

1. Elegir una pregunta de la colección de PDF del usuario, comprobar su permiso de uso y revisar el contexto completo. No crear una nueva ni alterar sus datos; una pregunta defectuosa se excluye o se deja pendiente, no se corrige silenciosamente.
2. Comprobar qué exige resolver; confirmar si encaja con el `target` del puesto. No reclasificarla artificialmente para llenar un cupo.
3. Registrar un `question_id` canónico, fuente/página, contexto, recursos y permiso. Reusar el mismo ID si ya existe; no crear otro para disfrazar un duplicado.
4. Anotar responsable y estado. En `assignment` conservar tema/subtema, clasificación propuesta, justificación, clave/explicación y referencias de recursos; la revisión docente debe tener responsable y fecha.
5. Contrastar duplicados y variantes antes de reservar. El cotejo histórico no garantiza unicidad global ni permisos.
6. Cargar la pregunta real en el editor solo después de preparar esos datos. No importar el JSON de puestos como banco de preguntas.

`target` significa necesidad editorial; `assignment` significa información de la pregunta elegida. Al crear este plan todos los `question_id`, responsables y `assignment` quedan vacíos. No hay reservas multiusuario ni bloqueos implementados: el responsable de la matriz coordina las asignaciones manuales. No sobrescribir el archivo completo con copias divergentes de compañeros.

## 7. Primer lote: cinco preguntas de Matemáticas de primera sesión

| Puesto | Número provisional | Objetivo | Idea de contenido a buscar, no clasificación confirmada |
| --- | ---: | --- | --- |
| SP001-S1-MAT-001 | 1 | Interpretación | Leer y relacionar información en una tabla o gráfica |
| SP001-S1-MAT-002 | 2 | Formulación/ejecución | Resolver una situación de porcentajes o descuentos |
| SP001-S1-MAT-003 | 3 | Argumentación | Validar o refutar una solución geométrica y su justificación |
| SP001-S1-MAT-004 | 4 | Interpretación | Relacionar dos representaciones de los mismos datos |
| SP001-S1-MAT-005 | 5 | Formulación/ejecución | Plantear o ejecutar una estrategia de proporcionalidad |

La primera propuesta de contenido original queda retirada por decisión del usuario. Usar ahora [las candidatas localizadas en sus PDF](../planning/SP001_LOTE01_FUENTES_PDF.md). Los temas orientativos de esta tabla no obligan a alterar la pregunta fuente: confirmar su tarea real y ajustar el temario editorial si corresponde, manteniendo las cuotas cognitivas. Si comparten contexto, ajustar el orden para mantener el grupo unido.

## 8. Verificación y estado

`uv run --offline --with reportlab --with pymupdf --with pillow python -B -m unittest discover -s tool -p test_sp001_plan.py -v`

Las pruebas verifican puestos únicos, cantidades, numeración, orden, cuotas por objetivo, cruce científico, partes de Inglés y separación del formato de proyecto del editor. No prueban la calidad de preguntas que todavía no se han seleccionado.

Al preparar la matriz: 254 puestos, 0 preguntas asignadas, 0 revisiones docentes registradas. No se generaron PDF nuevos ni se modificaron app, backend, servicios o datos del proyecto editorial guardado.
