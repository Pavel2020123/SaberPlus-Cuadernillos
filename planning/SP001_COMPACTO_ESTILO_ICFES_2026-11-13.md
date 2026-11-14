# SP-001 · Versión compacta con estilo de cuadernillo real · 13/11/2026

Base: los JSON de `handoff/SP001_primera_codex_C1_2026-11-13/` y `handoff/SP001_segunda_codex_C1_2026-11-13/` (correcciones C1 conservadas: textos, opciones, claves, explicaciones e imágenes idénticos a C1). Sin commit ni push.

| Paquete (`handoff/`) | Preguntas | Estudiante / resuelto / clave | C1 de partida |
|---|---|---|---|
| `SP001_primera_compacta_2026-11-13` | 120 | 57 / 85 / 1 | ver su INFORME |
| `SP001_segunda_compacta_2026-11-13` | 134 | 50 / 71 / 1 | ver su INFORME |

## Qué cambia

1. **Flujo adaptativo** (`column_flow: "adaptive"`, motor): cada pregunta va en columna si cabe; si no, a lo ancho debajo de las columnas; solo entonces pasa de página. La última pregunta de un tramo abre la columna derecha en vez de dejarla vacía. `layout: "full"` sigue forzando ancho completo.
2. **Estilo de cuadernillo real, con marca SaberPlus** (sin logos ni marcas ajenas): número de pregunta y letras de opción en negrita con sangría, texto justificado, separadores punteados, contexto sin recuadro con encabezado centrado en mayúsculas, número de página en círculo al pie.
3. **Figuras y tablas más pequeñas**: tamaño por defecto ≈ 1 pt por cada 8 px del original, entre 130 pt y el ancho de columna, alto máximo 190 pt; las de letra muy menuda reciben más ancho (hasta 300 pt) y pasan a lo ancho. Ajustes a mano pedidos por el usuario: tabla Madre/Edad 130 pt, tabla de contagiados 170 pt, tapa circular 110 pt. Los tamaños fijados por C1 no se tocaron (por eso varias de Ciencias de segunda siguen grandes y a lo ancho). A lo ancho quedan: primera 2, 4, 22, 95, 97, 104, 107, 108, 118, 120; segunda 11, 29, 36, 37, 39, 41, 42, 49, 50, 51, 52, 53, 55, 57, 59, 60, 61, 62, 63, 71, 72, 75 (numeración anterior al reordenamiento).
4. **Reordenamiento dentro de cada área** (autorizado por el usuario): cuando la siguiente pregunta no cabía, se trajo la más cercana que sí. No cambia el orden de las áreas, ni la cantidad por área, ni Inglés; los grupos con contexto siguen juntos y en su orden interno. El orden se eligió para llenar cada página y dejar el espacio sobrante en la última página de cada área (búsqueda sobre la simulación de páginas). Cambia de puesto la mayoría de las preguntas no inglesas. **La numeración impresa cambia**: equivalencias antes → ahora en `numeracion_antes_ahora.json` de cada paquete. Los números citados en informes anteriores (p. ej. pendientes de imágenes) son los de «antes».
5. Hoja de respuestas: la marca de agua es ahora «S+».

## Verificado

- 136 pruebas `unittest` OK (6 se actualizaron al estilo nuevo: número como etiqueta, contexto sin recuadro, encabezado en mayúsculas); `test_editor_live.mjs` OK; `git diff --check` limpio.
- Contra los JSON de C1: mismo contenido pregunta por pregunta (solo difieren `layout`, tamaños de imagen y `order`), mismas preguntas en cada área (25/41/25/29 y 25/25/29/55), Inglés en el mismo orden, contextos contiguos, claves iguales por ID, hoja con una fila por pregunta, sin respuestas en el PDF del estudiante.
- Revisión visual: láminas de muestra de ambas sesiones (unas 16 páginas a tamaño legible por sesión en esta última versión). **No se revisaron todas las páginas de la versión final una por una ni se imprimió.**

## Cierre (última revisión)

- **Referencias numéricas**: se buscó en enunciados, introducciones, opciones, explicaciones, contextos e instrucciones cualquier cita de un número de pregunta; no hay ninguna fija (solo «punto 1, 2, 3» de la gráfica de gases). Los rangos «RESPONDA LAS PREGUNTAS X A Y» se calculan al generar y se comprobó en el PDF que cada uno coincide con los números reales de su grupo. La hoja tiene una fila por pregunta y las marcas de la clave coinciden con el JSON por ID.
- **Tamaños de C1 ajustados caso por caso** (segunda, numeración C1): 51→200 pt, 52→229, 53→350, 59→380, 60→380, 61→213, 42→330, 71→250, 72→330; primera: rampa →260. Cifras, unidades y leyendas siguen legibles en la revisión en pantalla.
- **Tablas ampliadas** (primera, Ciencias): pH, alcoholes/éteres, queso, material de laboratorio, ciclistas, geometría molecular, conductividad y choques, a lo ancho entre 268 y 430 pt; segunda: boletas 305 pt.
- **Lectura**: se evaluó poner el contexto en una columna y las preguntas en la otra. No conviene: en columna cada lectura mide 425–1084 pt (la página útil son 710) y, donde cabe, ocupa más alto que el texto a lo ancho con sus preguntas debajo en dos columnas; con las infografías además se pierde legibilidad. En su lugar se reordenaron los grupos de lectura para que encajen mejor. Cómic «Filosofía en viñetas» a 460 pt de alto.
- Revisión visual: todas las páginas de ambas sesiones en láminas antes del último reordenamiento, y tras él las páginas 3–20 de primera y 21–38 de segunda más las figuras cambiadas. Sin impresión.

## Pendiente / a revisar

- Figuras que quedaron pequeñas y conviene mirar impresas: primera, tablas de 98, 99, 101 y 105 (numeración nueva) y la tabla de casillas; segunda, tablas de 36 y 41.
- Lectura crítica (primera) conserva huecos: cada lectura larga no cabe con su primera pregunta en lo que queda de página (págs. 18, 22, 24, 27 aprox.).
- Segunda: 49, 50 y 75 quedan casi solas en su página por el tamaño fijado en C1; las alternativas de 75 en cuadrícula se ven pequeñas.
- Explicaciones o textos que citen un número de pregunta fijo no se actualizan solos con el reordenamiento (los encabezados de contexto sí).
- Siguen vigentes los pendientes editoriales y de imágenes de los informes anteriores.

## Ajuste final pedido por el usuario

- Cuando un texto compartido cabe en lo que queda de la página pero no con su primera pregunta, ahora se imprime ahí, debajo de las preguntas anteriores, y sus preguntas abren la página siguiente (como en los cuadernillos impresos). Antes saltaba de página y dejaba media hoja en blanco. El encabezado «RESPONDA LAS PREGUNTAS X A Y» indica a qué preguntas pertenece.
- El orden dentro de cada área deja el espacio sobrante al final del área.
- Lectura crítica: sus preguntas van a lo ancho debajo de cada texto (pedido por el usuario tras comparar con un cuadernillo real); las demás áreas siguen en dos columnas.
- Cambio de área: si quedan al menos 260 pt libres, el área siguiente empieza en la misma página con su título centrado (no aplica a Inglés, que siempre abre página). En esta versión ocurre con Sociales tras Lectura (primera, pág. 29).
