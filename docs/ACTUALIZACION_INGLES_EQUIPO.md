> Actualización posterior: paquete combinado de25 Matemáticas+55 Inglés en `handoff/SP001_segunda_matematicas_ingles/`. Ver [cierre de Matemáticas](../planning/SP001_S2_MAT_CIERRE_CARGA.md). El paquete solo de Inglés sigue disponible como antecedente independiente.

# Actualización de inglés — 12 de noviembre de 2026

## Qué se entrega

55 preguntas completas de inglés de SP-001, segunda sesión, con contextos, claves, explicaciones y tres imágenes. Registro global: 175 registros (120 de primera sesión y 55 de inglés). La ausencia de repetición exacta no certifica equivalencias entre escaneos: cotejar también la fuente. Fuente de códigos: [lista de 55 usados](../planning/SP001_S2_INGLES_CODIGOS_USADOS.md) y `planning/PREGUNTAS_USADAS_GLOBAL.json`.

El paquete transportable está en `handoff/SP001_ingles_segunda/`: `proyecto.json`, `imagenes.json` con SHA-256 y `assets/uploads/` con las imágenes. No incluye el proyecto personal ni el guardado automático de ningún compañero. Este JSON contiene claves: es material del equipo, no entregar a estudiantes.

## Cómo actualizar sin perder trabajo

1. Guardar el proyecto del editor y descargar su JSON. Respaldar también `assets/uploads/`: el JSON por sí solo no lleva las fotos.
2. Comprobar `git status`. Si hay cambios propios, guardarlos en su rama/commit antes de actualizar; no usar reset ni sobrescribirlos.
3. Ejecutar `git pull --ff-only` y `uv sync`. Si hay divergencia, resolverla en una rama con el coordinador; no forzar el push.
4. Cerrar el servidor y volver a iniciarlo para cargar el motor nuevo. Arranque normal: `uv run --offline python -B tool/editor_server.py --port 4185`. Abrir http://127.0.0.1:4185/ y Ctrl+F5. Cada localhost apunta al equipo de quien lo abre, no al de Pavel.
5. Para probar el inglés, abrir una copia separada del proyecto. Antes de importar, copiar los archivos de `handoff/SP001_ingles_segunda/assets/uploads/` a `assets/uploads/` del repositorio, conservando nombres. No reemplazar imágenes existentes sin comparar el SHA-256. Importar `handoff/SP001_ingles_segunda/proyecto.json` desde el editor. La importación reemplaza el proyecto abierto: hacerlo únicamente después del respaldo.
6. Generar los tres PDF y revisar la vista. Nunca importar este JSON sobre las preguntas de otro compañero sin una integración explícita.

No se necesita la USB para abrir este paquete. Los PDF originales de referencia no se incluyen. Los permisos de reproducción y una clave oficial externa no están certificados.

## Cambios visibles

- Parte 1: descripciones a la izquierda y banco A–G a la derecha; ejemplo H separado. Sin círculos bajo las preguntas. El resuelto indica la letra junto a cada descripción.
- Parte 2: letreros vectoriales limpios con diseños diferentes, opciones A–C a la derecha.
- Parte 3: ejemplo ilustrado limpio y conversaciones con opciones a la derecha.
- Parte 4: Salento enmarcado y ocho espacios, opciones A–C en filas.
- Parte 5: British Museum en marco redondeado, siete preguntas con mayor separación.
- Parte 6: lectura sobre periodos de ocio, cuatro opciones; última pregunta con tarjetas 2×2.
- Parte 7.A: Spider-Wedding, ilustración a la izquierda; Parte 7.B: Chinua Achebe, retrato restaurado a la derecha. Diez espacios por texto, opciones A–D en filas.
- Bordes redondeados. Ejemplos resueltos independientes; ninguna marca de respuesta en los ítems del estudiante.
- Muestra solo de inglés: portada sin áreas vacías ni tiempo de sesión completa; tiempo por definir. Al integrar otras áreas vuelve la portada general.
- Las 55 respuestas de la muestra caben en una sola hoja; círculos conservan tamaño. Clave docente separada.

## Numeración y cantidades

Reparto editorial adoptado: 5/5/5/8/7/5/20 = 55, conservando bloques completos. Sustituye para este lote la propuesta histórica 5/6/6/10/9/6/13. No modificar la matriz histórica como si fuera un reparto oficial. La muestra imprime 1–55; el orden guardado 80–134 permite que, al integrar las 79 preguntas previas, inglés ocupe 80–134. No crear preguntas vacías para forzar números.

## Datos y compatibilidad

Los contextos de inglés incluyen metadatos opcionales `notice_layout`, `dialogue_layout`, `cloze_layout`, `reading_layout`, `inference_layout`, `illustrated_cloze_layout`, `image_side`, `part_label` y datos del ejemplo. No borrarlos al reexportar o integrar JSON. Las preguntas pueden incluir `answer_cards`. Los espacios usan `{{h...}}` una sola vez por pregunta y el campo `slot` correspondiente. Cambiar solo el número en el texto rompe la vinculación.

La paginación medida continúa rechazando bloques que exceden la página. No reducir imágenes hasta hacerlas ilegibles para ocultar el error. Los cambios no migran automáticamente los proyectos de otros compañeros. El motor es compartido: revisar sus tres PDF tras actualizar, especialmente inglés Parte 1 y hojas de respuesta.

## Trabajo en equipo y Git

Antes de elegir códigos: actualizar la rama y revisar el registro global. Cada compañero trabaja en su rama y reserva un bloque completo. Sincronizar el registro con `uv run --offline python -B tool/sync_used_questions.py RUTA_AL_JSON --session segunda` (o primera según corresponda), revisar el diff, hacer commit del lote y push al terminar el área. No borrar registros de otro compañero ni resolver conflictos del registro eligiendo un lado completo. Comparar códigos y huellas. Coordinar integración de JSON; Git no fusiona automáticamente proyectos del editor ni sus imágenes ignoradas.

## Validación y límites

Los tres PDF aportados por el usuario se auditaron: 55 claves, 55 explicaciones y 55 resaltados del resuelto coinciden con el JSON; estudiante sin resaltados, sin placeholders visibles. Después se regeneraron: estudiante 11 páginas, resuelto 17, clave 1. Se inspeccionaron la portada, hoja única y correspondencias de Parte 1. Sigue pendiente la aprobación final de impresión del usuario.

La ilustración de Spider-Man conserva el recorte original y textura: la restauración automática fue rechazada; no afirmar que está restaurada. El retrato de Achebe y el ejemplo de conversaciones sí fueron limpiados. No se tocaron Flutter, backend, la USB ni los PDF originales.

## Comprobación antes de publicar

Pasaron 132 pruebas con `uv run --offline python -B -m unittest discover -s tool -p "test*.py"`. Tres expectativas históricas se actualizaron al comportamiento vigente: lectura larga completa en página propia, banco de palabras sin círculos bajo las descripciones y encabezado Palabras. Se comprueba que no se pierden las 30 líneas del contexto ni las 20 de la pregunta al separar páginas. `git diff --check` sin errores de espacios.
