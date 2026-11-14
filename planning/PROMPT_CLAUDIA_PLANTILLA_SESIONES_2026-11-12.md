# Prompt de relevo para Claudia: maquetación y hoja de respuestas

Copia desde aquí:

---

Trabaja en `C:\Users\LENOVO 14ALC6\Desktop\SaberPlus-Cuadernillos`. Es un proyecto Python/ReportLab independiente. Quiero corregir la presentación profesional de mis cuadernillos conservando todo el contenido: **no reconstruyas la aplicación ni cambies innecesariamente su arquitectura**. No tocar Flutter, backend, Docker, cuentas, servicios externos ni datos de estudiantes.

## 1. Lee el estado vigente y verifica antes de actuar

Lee, en este orden:

1. `AGENTS.md`, `README.md`, `CONTEXTO.md` (las notas antiguas de cierres parciales son antecedentes).
2. `docs/EDITOR_LOCAL.md` y `docs/ECUACIONES_Y_MAQUETACION.md`.
3. `docs/ACTUALIZACION_INGLES_EQUIPO.md`: conserva los formatos especiales y el reparto editorial adoptado.
4. `planning/SP001_S2_AUDITORIA_Y_RESPALDO_2026-11-12.md`.
5. `docs/REFERENCIAS_MAQUETACION_COMPLETAS_2026-11-12.md` y su inventario JSON.
6. Si vas a trabajar también la primera sesión, `planning/PROMPT_CLAUDE_MAQUETACION_SP001.md`, separando sus estados históricos de lo comprobado hoy.

Comprueba `git status`, rama y diff. Último commit de códigos conocido: `519e1aa` en `main`, enviado a origin/main. Puede haber cambiado: verifica. Hay documentos y respaldos locales sin commit deliberadamente. No hagas reset, restore global, checkout destructivo, force-push ni fusiones automáticas. No publiques el paquete completo o cambios de plantilla junto con códigos usados. Este relevo no autoriza un nuevo commit/push; realizarlos cuando yo lo pida.

## 2. Dos sesiones, dos proyectos JSON: nunca mezclarlos

**Primera sesión:** 120 preguntas incluidas: 25 Matemáticas, 41 Lectura crítica, 25 Sociales, 29 Ciencias.

- JSON activo conocido: `tmp/pdfs/flujo-mixto/datos_editor_prueba/project.json`.
- Editor: `http://127.0.0.1:4187/`.
- Última comprobación: revisión 102, 120 incluidas. Verifica el estado actual; no lo sustituyas por una copia más antigua.
- Respaldo anterior documentado: `C:\Users\LENOVO 14ALC6\Desktop\SaberPlus-Respaldos\SP-001-primera-2026-11-11`. Verifica su existencia y revisión; no modifiques esa ubicación ni otros proyectos para trabajar la sesión 2.

**Segunda sesión:** 134 incluidas: 25 Sociales, 25 Matemáticas, 29 Ciencias, 55 Inglés; puestos 1–25/26–50/51–79/80–134.

- JSON activo: `tmp/editor-sp001-segunda/project.json`.
- Editor: `http://127.0.0.1:4188/`; runner `tmp/start_sp001_segunda.py`.
- Respaldo auditado: `handoff/SP001_segunda_completa_2026-11-12_rev89/` y ZIP del mismo nombre.
- `proyecto.json` y `data/project.json` dentro de ese respaldo son dos copias del MISMO proyecto de segunda sesión. No son una primera y una segunda sesión.
- Revisión 89 al hacer el respaldo, 134 códigos únicos, 93 imágenes vinculadas verificadas. El JSON contiene claves y explicaciones: es privado del equipo.
- `MANIFIESTO_SHA256.json`, `imagenes.json`, `verificar_respaldo.py` y `LEEME_RESTAURAR.md` permiten comprobarlo. El ZIP se extrajo y verificó, y el motor copiado generó los PDF sin usar imágenes del proyecto original.

No importes un JSON sobre el editor activo sin haber respaldado sus cambios. Lee el estado actual antes de guardar y usa la revisión correspondiente. El usuario puede tener cambios todavía sin guardar en el navegador: no reinicies servicios ni recargues automáticamente. Para experimentar, trabaja en una copia aislada y un puerto distinto (por ejemplo 4190), no sobre 4187/4188.

## 3. Archivos que voy a aportar

Voy a adjuntar los PDF actuales y una foto del modelo de hoja de respuestas que quiero. Primero identifica qué sesión y revisión representa cada PDF; compara con el JSON actual y no asumas que el PDF coincide con una exportación antigua.

Si todavía no adjunté esos archivos, puedes revisar el respaldo y preparar diagnóstico y propuestas. Marca como pendientes la comparación con mis PDF nuevos y la decisión final de la hoja. No inventes el modelo de la foto ni detengas el resto de la revisión por esperarla. La hoja de respuestas actual está mal distribuida y la corregiremos con mi referencia.

## 4. Referencias completas ya revisadas

Disponibles localmente, solo para lectura:

- `references/S11-O Segunda sesión Completo.pdf`: 28 páginas físicas.
- `references/S11-M 2DA SESIÓN.pdf`: 28 páginas físicas.
- `references/S11-P s2.pdf`: 28 páginas físicas.

Se renderizaron e inspeccionaron las 84 páginas para estudiar estructura. Sus originales conservan los hashes del inventario. Las láminas están en `tmp/pdfs/referencias-estructura-completas/{O,M,P}/`. Usa páginas físicas para citar; O tiene un salto en la numeración impresa. Si no están los renders, vuelve a renderizar sin modificar originales.

Revisa el recorrido completo y amplía especialmente: P 2/4/7/13/17/20; M 6–8/17–19; O 11/16 y los bloques de Inglés 21–28 en los tres. Estos casos muestran franja ancha + columnas + franja ancha, grandes contextos, alternativas gráficas y formatos de inglés.

Extrae principios de composición; no copies marcas, personajes, preguntas o adornos de esos ejemplares. Su carácter oficial y permisos comerciales no están acreditados. No cambies las cantidades o partes de SP-001 porque otra referencia tenga un reparto diferente.

## 5. Qué corregir y cómo decidir el ancho

Audita primero cada página y entrega una tabla: sesión, página, número/ID de pregunta, defecto, causa probable y corrección propuesta. Mide el ancho/alto de texto, fórmulas, tabla y alternativas.

- No impongas dos, tres o cuatro preguntas por página. Una pregunta puede necesitar una página entera si tiene un estímulo complejo.
- Una página con un solo contexto de Inglés puede contener siete, ocho o diez preguntas. Cuenta los ítems vinculados, no las cajas.
- Distingue huecos evitables de espacio necesario. Revisa saltos manuales, reservas de contexto, altos máximos de imagen, flujo secuencial/equilibrado y capacidad de alternar franjas a ancho completo con columnas.
- Usa `layout`, `options_layout`, `image_width`, `image_height`, `option_image_width`, `option_image_height`, saltos y `column_flow` existentes antes de crear otro sistema. El motor medido es `tool/editor_pdf.py`; NO el prototipo histórico fijo de 22 ítems `generate_booklet_template.py`.
- No reduzcas letra, fórmulas o imágenes para disimular un bloque que no cabe. No recortes datos ni inventes compatibilidad con tamaños arbitrarios. Si necesitas ampliar los límites, justifica y prueba el cambio localizado.
- Conserva lectura por columnas, secuencia de alternativas, separación, márgenes y jerarquía. Evalúa el tamaño impreso, no solo el zoom en pantalla. Mantén la identidad SaberPlus.

### Aprovechamiento del espacio: requisito central del usuario

No trates cada pregunta como una p?gina ni cada p?gina como una ?nica cuadr?cula fija. Comp?n bandas consecutivas: bloque ancho ? dos columnas ? bloque ancho, seg?n las dimensiones reales y el orden de lectura. Por ejemplo, despu?s de una pregunta ancha de media p?gina, intenta colocar las siguientes preguntas debajo si caben completas y legibles. Si una banda de columnas acaba a distinta altura, el siguiente bloque ancho comienza debajo de la columna m?s baja: nunca invade la otra. Una pregunta peque?a puede continuar en la columna disponible solo si conserva la secuencia de lectura.

Ante cada hueco grande, identifica por qu? la siguiente pregunta salt?: salto expl?cito, altura reservada frente a altura dibujada, ancho innecesario, relleno interior de imagen, contexto indivisible o frontera de ?rea/parte. Registra medidas en puntos y captura antes/despu?s. No adelantes una pregunta posterior para tapar un hueco ni separes enunciado y opciones. No elimines todos los espacios: conserva respiraci?n y separaci?n entre preguntas.

Inspecciona `column_group`, `flush_columns`, `context_flows` y la condici?n `use_band` en `tool/editor_pdf.py`. El modo equilibrado actual excluye contextos compartidos, Ingl?s y saltos expl?citos: no atribuyas a esos bloques capacidades que a?n no tienen. Corrige el motor solo si los controles existentes no resuelven el caso. Una extensi?n para contextos debe mantener sus rangos y garantizar que ning?n enunciado quede separado de su est?mulo sin referencia clara.

## 6. Pendientes concretos de la segunda sesión

Los números siguientes son los impresos en la sesión de 134; no confundir con el número original del catálogo:

- 51, p.30: encabezado de tabla de temperatura recortado; 53, p.31: encabezados de tabla superpuestos/recortados.
- 57, p.34: las alternativas se reconstruyeron como cajas y el texto se superpone; deben recuperarse los dibujos originales. Contexto 56–58, p.33, conserva textura/borde ajeno.
- 52 y 59–62: se usaron reconstrucciones por código antes de la corrección del usuario. Sustituirlas por mejoras de los originales con la herramienta de imágenes y cotejar datos. En 60 y 62 hay trazados aproximados: no presentarlos como mediciones exactas.
- 55, p.32: cotejo detallado de la gráfica presión-volumen pendiente.
- 9 y 21, pp.6/12: CO₂ aparece con cuadrados en ciertos textos. En la explicación de 72 también fallan los subíndices de F23/F13. Usa el motor existente para texto matemático mixto sin cambiar las fórmulas.
- 33/38/44, pp.19/21/26: fórmulas, radicales y fracciones demasiado pequeños.
- 39, p.22: B es la clave prevista, pero D también expresa un cálculo compatible; supuestos de tasa y suministro requieren revisión editorial. 49, p.28: B también muestra nube con correlación positiva aunque su recta sea horizontal. No resolver estas ambigüedades cambiando claves u opciones silenciosamente.
- 40, p.23: redacción «recaudado» frente a «dejado de recaudar», ya documentada en la explicación.
- 75, p.47: manómetros correctos ampliados, pero pequeños al imprimir. Conservar orden de escala 0/0,5/1,0/1,5/2,0/2,5/3,0, extremos largos de agujas, contrapesos cortos y niveles de termómetros. Clave correcta actual **B**, corregida desde A: compresión, misma temperatura, presión 1,5 → 2,5. No reintroducir A desde una propuesta antigua.
- 60 y 79: revisar alcance y unicidad de las conclusiones; 70 y 71 conservan imprecisiones originales («contrapeso» de densidad y «Cigoto n» sin fertilización), documentadas en sus explicaciones. No borrar sus notas.
- Hojas pp.58–60 y clave pp.1–3: están los 134 números, pero las columnas quedan desequilibradas. Usar la foto que aportaré para definir el diseño final.
- Inglés pp.54–57: evaluar aire y tamaño de lectura; Spider-Wedding conserva textura de referencia.

Las páginas citadas corresponden al PDF auditado de revisión 89. Si cambia la paginación, usa IDs/códigos para localizar las mismas preguntas. Informe y evidencias en `planning/SP001_S2_AUDITORIA_Y_RESPALDO_2026-11-12.md` y `tmp/pdfs/auditoria-s2-rev89/`.

## 7. Imágenes y contenido intocables durante la maquetación

El usuario exige **mejorar las imágenes originales con la herramienta de imágenes**, no reemplazarlas por dibujos hechos por código. Usa las habilidades y herramientas disponibles para edición de imágenes. Después coteja el resultado: la herramienta puede alterar símbolos y no se acepta una mejora solo porque se vea limpia.

Conserva datos, unidades, posiciones relevantes, escalas, leyendas, puntos, flechas, trayectorias, conexiones, cargas, número de partículas, agujas y alternativas equivocadas. Sus errores intencionales son parte de la pregunta. No añadas graduaciones o valores a gráficos cualitativos. Guarda el original y una versión nueva; cambia la referencia del JSON solo tras inspección. Si un dato no se puede leer, documenta el pendiente sin inventarlo.

No modificar ni borrar IDs, códigos, enunciados, opciones, claves, explicaciones, clasificación, orden o contextos para hacer caber páginas. Los cambios editoriales de contenido deben quedar separados y explícitos; consulta los casos ambiguos. No se exige revisión de un docente ni se atribuye validación psicométrica o aprobación externa.

## 8. Inglés y hoja de respuestas

Conserva 55 ítems y el reparto vigente 5/5/5/8/7/5/20. La Parte 1 de SP-001 es asociación, aunque una referencia empiece con avisos.

- Parte 1: descripciones izquierda y banco de palabras derecha, sin círculos debajo de cada pregunta; conserva ejemplo H. Hoja de respuestas 80–84 con A–G.
- Avisos con diseños diferentes; conversaciones y opciones alineadas a derecha; lecturas con sus marcos; cloze con opciones en filas; ejemplos resueltos aparte. No convertir todo en preguntas genéricas de cuatro opciones.
- Las demás partes usan A–C o A–D según sus datos, no una cantidad fija para todo Inglés.
- La nueva hoja debe contener exactamente una fila por pregunta: 120 para primera y 134 para segunda, con correspondencia verificable entre número, letras permitidas y clave. Los ejemplos 0 no se cuentan como preguntas. Círculos legibles; clave docente con una sola marca. No afirmar lectura óptica sin calibración real.
- Revisa el resultado del estudiante, el resuelto y la clave: los ejemplos pueden estar resueltos, pero no deben filtrarse claves de ítems calificados al estudiante.

## 9. Ejecución segura, pruebas y entrega

Usa PowerShell y el entorno existente `uv run --offline python -B ...`. No cambies dependencias por rutina. Antes de cada modificación del JSON, respaldo con imágenes y revisión actual. Conserva el paquete rev89 intacto como punto de retorno; crea una revisión nueva para el resultado corregido.

Haz primero una variante aislada y reviewable con unas páginas representativas: texto, ecuaciones, cuatro gráficas, manómetros, contexto compartido, Inglés y hoja de respuestas. Cuando yo autorice el ajuste final, aplícalo a la sesión indicada sin reemplazar la otra. Las correcciones rutinarias que ya haya autorizado en esta conversación no necesitan permisos repetidos.

Comprueba al terminar:

1. Cantidades, conjunto de IDs/códigos, orden, contextos, huecos, claves y textos antes/después. Ninguna pregunta perdida ni duplicada; diferencias de contenido no autorizadas = detener publicación.
2. Todas las imágenes existen y conservan hashes si no se editaron. Para las editadas, registrar original/nueva y cotejo visual.
3. Generación de estudiante, resuelto y clave; guía auxiliar si corresponde. Renderiza y revisa **todas** las páginas finales, con vistas ampliadas de casos complejos. No basta `validate_project` ni extracción de texto.
4. Coincidencia de cada marca de clave y explicación con el JSON; ausencia de respuestas filtradas al estudiante; correspondencia completa de la nueva hoja.
5. Ejecuta las pruebas apropiadas: `uv run --offline python -B -m unittest discover -s tool -p 'test*.py'`, `node tool/test_editor_live.mjs` si cambias interfaz/estado, y `git diff --check`. Antes del relevo pasaron 132 pruebas, pero verifica tras tus cambios. No confundas un aviso de stderr de PowerShell con un fallo si el reporte de unittest termina en OK.
6. Entrega informe antes/después, páginas/IDs corregidos, pruebas efectivamente ejecutadas, pendientes y paquete nuevo con JSON, imágenes, manifiesto SHA-256, instrucciones de recuperación y ZIP probado tras extraer. Si trabajas las dos sesiones, generar **dos proyectos JSON y dos respaldos claramente separados**.

Empieza confirmando qué JSON y PDF representan el estado actual. Luego presenta el diagnóstico concreto y una propuesta de distribución basada en las referencias, sin perder contenido ni rehacer el proyecto. La hoja final debe ajustarse a la foto que yo aporte esta noche.

---
