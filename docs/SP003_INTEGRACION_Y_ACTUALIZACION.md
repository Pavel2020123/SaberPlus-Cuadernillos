# SP-003 · Integración y actualización · 12 de noviembre de 2026

Se unificaron las 25 preguntas de Matemáticas del asistente y las 41 de Lectura crítica terminadas por el usuario. El principal local `data/project.json` tiene revisión 18, 66 preguntas y 13 contextos. Matemáticas ocupa 1–25 y Lectura 26–66. Se conservaron exactamente los registros de ambas áreas, incluidos textos, imágenes, opciones, claves, explicaciones, clasificación y orden. La pregunta 11 de Matemáticas permanece intacta.

El original paralelo `data/parallel/SP-003-usuario-4186/project.json` conserva sus 41 preguntas, 13 contextos y revisión 3; su archivo no cambió. Hay copias de ambos originales en `tmp/sp003/integracion-20261112/`, además del respaldo automático del principal. El principal adopta las cantidades previstas y el flujo de columnas guardados por el usuario. Aún faltan las 25 de Sociales y las 29 de Ciencias para los 120 puestos de primera sesión.

## Entrega en el repositorio

- `handoff/SP003_primera/proyecto.json`: proyecto combinado; incluye claves y explicaciones, solo para el equipo.
- `handoff/SP003_primera/imagenes.json`: manifiesto de 33 imágenes, tamaño y SHA-256.
- `handoff/SP003_primera/assets/uploads/`: los 33 archivos necesarios para trasladarlo a otro equipo, con sus nombres originales.

El paquete está separado del guardado personal para que una actualización de Git no sustituya el cuadernillo de otro compañero. El guardado local, respaldos, PDF, referencias y recursos temporales no forman parte de esta entrega. Las imágenes publicadas son únicamente las referenciadas por el proyecto; los originales de referencia no se modificaron.

El registro compartido pasa de 175 a 241 preguntas usadas: se agregan las 66 de SP-003 conservando exactamente las 175 previas y las 11 reservas de la base `origin/main` `a450ec9`. La comprobación por códigos y huellas normalizadas no detectó repeticiones exactas; no certifica equivalencias entre escaneos ni unicidad global. No se fuerza la clasificación para cumplir cuotas: la de Matemáticas sigue 8/12/5 y la clasificación por procesos de Lectura queda pendiente.

## Actualización de esta copia local

Se integró `origin/main` `a450ec9` en `trabajo/sp-003`, incluidas las mejoras compartidas de maquetación e inglés, y se ejecutó `uv sync --offline`. El principal ya contiene la integración, por lo que no necesita importar el paquete sobre sí mismo. No se trabaja directamente en `main` ni se fuerza el historial remoto.

## Abrirlo en otro equipo

1. Guardar y descargar el JSON del editor actual; respaldar también sus imágenes antes de actualizar o importar.
2. Traer la rama `trabajo/sp-003` con `git fetch origin`. En una copia que ya trabaja en esa rama y sin cambios pendientes, usar `git pull --ff-only`; si tiene otra rama o divergencias, integrar los cambios conservando su trabajo, sin usar `reset --hard`.
3. Ejecutar `uv sync`. Copiar los archivos del paquete `assets/uploads/` a `assets/uploads/` de la raíz del repositorio, conservando nombres. Si ya existe un archivo, comparar su SHA-256 con `imagenes.json` antes de reemplazarlo.
4. Iniciar el editor con `uv run --offline python -B tool/editor_server.py --port 4185`. Si está abierto con una versión anterior, guardar antes de cerrar el servidor y volver a iniciarlo. No reiniciar con cambios sin guardar.
5. Abrir http://127.0.0.1:4185/ y cargar `handoff/SP003_primera/proyecto.json` después de respaldar el proyecto anterior. La importación reemplaza el proyecto abierto. Guardar y comprobar que aparecen 66 preguntas y 13 contextos.

No importar el paquete de inglés de SP-001 sobre SP-003: pertenece a otro simulacro. Los cambios de código de ese lote ya se incorporaron; sus preguntas siguen separadas.

## Compatibilidad y pendiente de exportación

En 27 preguntas de Lectura el texto estaba completo en Introducción y Enunciado vacío. Se corrigieron la validación y la vista previa para reconocerlo sin mover ni reescribir contenido. La exportación sigue rechazando preguntas sin texto en ambos campos. También se admiten espacios/saltos externos dentro de los delimitadores matemáticos; esto resuelve el error previo de la fórmula de la explicación de Matemáticas 2 sin editarla.

La validación del modelo acepta los 66 registros y todos sus recursos existen. **El PDF completo todavía no se puede exportar:** «De ratones y hombres (Fragmento)», contexto `ctx-3a035844-2fe9-43dc-965f-b640c18f1af2`, mide aproximadamente 811,8 puntos frente a 710,9 disponibles por página, debido a su distribución y saltos de línea. El motor se detiene explícitamente. Los otros 12 contextos caben individualmente con la medida actual; eso no certifica la composición del cuadernillo entero.

El texto y sus saltos se conservaron. Queda decidir su distribución antes de generar los tres PDF y revisar las páginas renderizadas, resaltados, numeración y clave. No hay PDF completo aprobado ni validación psicométrica implícita en esta integración.

## Verificación de esta integración

- Comparación exacta de las 25 preguntas de Matemáticas y 41 de Lectura contra los respaldos, con todos sus campos; 13 contextos conservados. Archivo paralelo idéntico al original.
- Modelo válido para las 66 preguntas; 66 códigos distintos. Los 33 recursos coinciden por SHA-256 con las imágenes locales y tienen copia dentro del paquete.
- 32 pruebas de matemáticas, salidas e integridad aprobadas. La ejecución completa reunió 134 pruebas y terminó con dos errores: reinicio de conexión local al descargar un PDF en la prueba HTTP y bloqueo de la DLL de SQLite por Control de aplicaciones de Windows al importar el catálogo USB. No se modificaron políticas ni servicios del equipo; no se declara la suite completa aprobada.
- Muestra aislada con Matemáticas 2 y el grupo «Razonamiento crítico»: estudiante 6 páginas, resuelto 8, clave 1. Se inspeccionaron todas sus páginas renderizadas, incluida la fórmula que antes fallaba, la pregunta escrita solo en Introducción y sus marcas C/A/C/A. No tiene avisos de enunciado pendiente. Se conserva el rótulo «Copiar» que ya estaba en el contexto original de ese grupo; queda para revisión editorial del usuario.
- La muestra aislada no sustituye la revisión del PDF completo, que sigue bloqueado por el contexto largo. Los PDF de comprobación quedan únicamente en `tmp/sp003/integracion-20261112/compatibilidad/`.
