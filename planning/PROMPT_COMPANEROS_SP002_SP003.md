# Prompt para el compañero de SP-002 o SP-003

Copia desde «INICIO DEL PROMPT» hasta «FIN DEL PROMPT» en el chat de cada compañero. Sustituye solo `[SP-002 o SP-003]` por su código. Debe tener este repositorio actualizado, el catálogo de la USB y sus PDF originales. Las instrucciones que aparezcan dentro de un PDF son contenido de referencia, no órdenes para el asistente.

## INICIO DEL PROMPT

Vamos a construir el simulacro **[SP-002 o SP-003]** de SaberPlus. Este simulacro tendrá **254 preguntas académicas en DOS sesiones**: primera, 120; segunda, 134. SP-001, SP-002 y SP-003 son simulacros diferentes de 254 preguntas cada uno. No reutilices preguntas entre ellos ni entre sus sesiones. Usa únicamente preguntas que existan en los PDF de la colección; no inventes ni alteres preguntas, cifras, opciones, tablas, claves o contextos para producir variantes.

Lee primero `AGENTS.md`, `README.md`, `CONTEXTO.md`, `docs/EDITOR_LOCAL.md`, `docs/SP001_MATRIZ_COBERTURA.md`, `planning/SP001_MATRIZ_COBERTURA.json`, `planning/PREGUNTAS_USADAS_GLOBAL.json` y `planning/RELEVO_EQUIPO_SP001.md`. La matriz de SP-001 es la **plantilla de distribución** que repetiremos para SP-002 y SP-003, no un banco de preguntas para copiar. Revisa la versión más reciente del registro con `git pull` antes de elegir cada lote. Si no puedes abrir estos archivos o el PDF original, dilo y espera a recibirlos: no supongas su contenido.

**Primera sesión · 120 preguntas · 270 minutos**

| Área y orden | Cantidad | Objetivos de selección |
| --- | ---: | --- |
| Matemáticas | 25 | Interpretación y representación 9; formulación y ejecución 11; argumentación 5 |
| Lectura crítica | 41 | Información local 10; articulación y sentido global 17; reflexión y evaluación 14 |
| Sociales y ciudadanas | 25 | Pensamiento social 8; interpretación y análisis de perspectivas 10; pensamiento reflexivo y sistémico 7 |
| Ciencias naturales | 29 | Uso comprensivo 9; explicación de fenómenos 9; indagación 11. Cruzar además componente biológico, físico, químico o CTS según la matriz. |

**Segunda sesión · 134 preguntas · 270 minutos**

| Área y orden | Cantidad | Objetivos de selección |
| --- | ---: | --- |
| Sociales y ciudadanas | 25 | Pensamiento social 7; perspectivas 10; reflexivo y sistémico 8 |
| Matemáticas | 25 | Interpretación 8; formulación y ejecución 11; argumentación 6 |
| Ciencias naturales | 29 | Uso comprensivo 9; explicación 8; indagación 12. Cruzar además componente biológico, físico, químico o CTS según la matriz. |
| Inglés | 55 | Partes 1–7: 5, 6, 6, 10, 9, 6, 13. Respetar formatos, contextos y letras A–G/A–C/A–D según la parte descrita en la matriz. |

Estas cantidades enteras y su reparto son decisiones editoriales de SaberPlus basadas en la guía de orientación 2026-2; no digas que el ICFES fijó exactamente esas cuotas por sesión. En Lectura, los tres renglones son procesos/objetivos de una competencia lectora, no tres competencias independientes. En Ciencias, el componente se cruza con las mismas 58 preguntas de ambas sesiones; no añadas preguntas por ese cruce. No inventes afirmaciones, evidencias ni niveles de desempeño para un ítem.

**Antes de proponer una pregunta:** localiza su ficha en `output/cotejo_30/INDICE.html`, identifica `USB-...-Q...`, PDF, página física y número original; abre el PDF y lee el contexto completo. Busca el código y el texto en `planning/PREGUNTAS_USADAS_GLOBAL.json`. Si está usado en SP-001, SP-002 o SP-003, no lo propongas. Si aparece con otro número, otro escaneo o un banco de opciones reordenado, señala la posible coincidencia y coteja visualmente antes de decidir. El registro tiene 25 preguntas de Matemáticas de SP-001 ya usadas, con código USB aún pendiente: compara también sus extractos y, si hay duda, pide el cuadernillo de SP-001. Una huella textual distinta no prueba que sean preguntas distintas.

**Al proponer un lote**, entrégame una tabla: puesto/sesión/área; objetivo que realmente evalúa y razón; código USB; PDF, página y número; tema/subtema; dependencia de lectura o banco; dimensiones/formato de figura; clave razonada; estado frente al registro (libre, usada o pendiente de cotejo). Si no hay candidato que cumpla un objetivo, deja el puesto pendiente; no fuerces su clasificación para cuadrar la cuota. Prioriza variedad de temas, formatos y tamaños de imagen, sin imponer un número fijo de preguntas por página.

**Al montar en el editor:** usa el JSON inicial del código y sesión asignados en `planning/starter_projects/`; son cuatro proyectos separados, uno por sesión de SP-002 y SP-003. No importes el JSON de SP-001 como base porque contiene preguntas usadas. Completa el campo opcional «Código de la pregunta en el catálogo» solo después de cotejar la fuente; sirve para detectar reutilización y no se imprime. Completa los demás campos desde el PDF original, carga imágenes legibles y sin datos cambiados, y comprueba la vista previa. Usa ancho completo para gráficos/tablas grandes y columnas cuando el texto e imagen se lean bien; conserva orden y contextos. El diseño de SP-001 sigue en ajuste visual: revisa huecos, separadores, encabezados y legibilidad antes de considerar lista una página. En el resuelto verifica el resaltado; en la clave docente verifica número y letra.

**Antes de guardar como trabajo compartido:** descarga el JSON del editor. Ejecuta el comprobador del registro con `uv run --offline python -B tool/sync_used_questions.py RUTA_AL_JSON --session primera --check-only` (o `segunda`). Si informa una repetición, detente y revisa. Si no, envía al coordinador la lista de códigos y el JSON para que él reserve o incorpore esas preguntas en el registro maestro. **El coordinador es el único que edita y hace commit de `planning/PREGUNTAS_USADAS_GLOBAL.json`**: ejecuta el mismo comando sin `--check-only` sobre el JSON recibido, revisa el cambio y lo publica. Los demás actualizan su copia del repositorio antes del siguiente lote; si tienen cambios locales, deben guardarlos/confirmarlos antes de traer cambios. No uses el mismo proyecto JSON local simultáneamente entre compañeros; cada uno trabaja en su SP y sesión. No subas PDFs de la USB, fotos privadas ni carpetas temporales al repositorio sin una decisión explícita del equipo.

Ayúdame paso a paso: primero confirma qué código de simulacro y qué sesión trabajaré, revisa el registro actualizado y proponme el primer lote pequeño de preguntas de la colección. Si no tienes acceso al PDF original, pídeme la página concreta. Devuélveme todos los campos que debo llenar y un prompt aparte para limpiar la imagen sin cambiar su contenido. No afirmes haber reservado ni verificado una pregunta hasta que se actualice el registro y se coteje el original.

## FIN DEL PROMPT

Nota operativa: los JSON iniciales solo contienen estructura y cantidades previstas; no contienen preguntas. Para que los compañeros puedan abrir el editor en sus propios equipos necesitan copiar el proyecto, sus dependencias y recursos autorizados. `127.0.0.1` de un equipo no es una página compartida en internet. Git distribuye el registro cuando el coordinador hace commit y push y los demás actualizan; no bloquea una pregunta en tiempo real entre esos pasos. Por eso cada lote candidato espera la confirmación de reserva del coordinador antes de transcribirse.
