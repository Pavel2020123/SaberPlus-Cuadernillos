# SP-001: cierre de la entrega compacta, 13/11/2026

Esta revisión sustituye los estados parciales de los informes anteriores para la entrega PDF. No publica cambios en GitHub ni altera los JSON de partida, los paquetes C1 o los respaldos anteriores.

## Entrega

Los seis PDF actuales están en `output/SP001_entrega/`. Los dos JSON y sus equivalencias de numeración también están allí. Cada respaldo integral independiente se guarda en `E:/SaberPlus_SP001_cierre_2026-11-13/SP001_{primera,segunda}_cierre_verificado_2026-11-13.zip`, con imágenes, motor y manifiesto SHA-256.

| Sesión | Preguntas | Estudiante | Resuelto | Clave | Imágenes vinculadas |
|---|---:|---:|---:|---:|---:|
| Primera | 120 | 57 páginas | 85 páginas | 1 página | 69 |
| Segunda | 134 | 50 páginas | 71 páginas | 1 página | 93 |

## Qué se completó

- Se recuperó el trabajo donde Claude se interrumpió. La penalización de columnas vacías ya estaba en el script temporal; no estaba pendiente su implementación, sino ejecutar y comprobar sus resultados.
- Se ejecutó el reordenamiento de ambas sesiones. En la primera produjo 58 páginas y se descartó porque empeoraba la extensión frente a las 57 de la base de trabajo. En la segunda produjo 50 páginas y se conservó.
- Se corrigió manualmente la pregunta 85 de la primera: a ancho completo evita una columna derecha vacía sobre la pregunta 86. No cambia contenido, clave, orden, tamaños de figuras ni cantidad de páginas.
- Se regeneraron los PDF con el motor actual. No se usaron como entrega los PDF antiguos de `output/` que no correspondían al último estado temporal.
- Se cotejaron por ID con C1 los enunciados, opciones, explicaciones y claves: no cambian. Solo se permiten diferencias de maquetación, dimensiones de imágenes y orden autorizado dentro de cada área. Se conservan áreas, cantidades, orden de Inglés y grupos de contexto contiguos, con su orden interno.
- Se incluyó una lista de códigos y puestos por pregunta en cada respaldo, y equivalencias desde la numeración de C1. Los informes históricos que citan números antiguos deben interpretarse mediante esas equivalencias.

## Comprobaciones

- 136 pruebas `unittest` superadas; `node tool/test_editor_live.mjs` correcto y `git diff --check` limpio.
- 120 y 134 IDs únicos, sin faltantes respecto a C1; todas las 69 y 93 rutas de imágenes existen.
- La numeración docente coincide por ID y respuesta con cada JSON. La hoja del estudiante tiene 120 y 134 filas respectivamente. Los PDF llevan su sesión correspondiente y no presentan caracteres de sustitución ni cuadrados negros en el texto extraído.
- Revisión visual de todas las páginas de los seis PDF mediante láminas; ampliación adicional de la página corregida de Sociales, las tablas de gases y aceite, las cuatro alternativas de tortugas, la tormenta, los manómetros y la hoja de 134 respuestas. Las láminas no sustituyen una lectura editorial de cada palabra a tamaño de impresión.
- Los ZIP se comprueban con CRC y SHA-256 de cada archivo interno. El manifiesto permite verificar la restauración sin depender de la conversación.

## Límites y espacios que todavía se ven

La entrega sigue teniendo huecos visibles, sobre todo en Lectura y al final de áreas o bloques gráficos. No se certifica que todos sean inevitables ni que el algoritmo encuentre la paginación mínima. La búsqueda global probada no mejoró la primera sesión; se conservó la versión más corta comprobada. Cada respaldo incluye `ESPACIOS_RESTANTES.md` con una medición orientativa de los espacios inferiores mayores de 180 pt.

No se ha hecho impresión física. Las leyendas más pequeñas de gráficos, el cómic y las burbujas A–G requieren esa comprobación antes de una tirada. No se añadieron preguntas, no se rehízo ninguna imagen en este cierre y no se alteraron los originales de `references/`.

No se hizo commit ni push: los compañeros aún no reciben estos archivos mediante GitHub. La entrega y los respaldos son locales y en PAVEL.
