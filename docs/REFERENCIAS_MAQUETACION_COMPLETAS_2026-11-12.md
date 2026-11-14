# Referencias completas para revisar la maquetación

Revisión del 12/11/2026. Se renderizaron e inspeccionaron visualmente las **84 páginas físicas** de tres archivos completos disponibles en `references/`: 28 por archivo. Se revisó su composición, no la corrección de todas sus preguntas ni claves. Los originales se conservaron sin cambios; el SHA-256 se comprobó antes y después del renderizado.

| Referencia | Páginas físicas | Distribución visible |
| --- | ---: | --- |
| `references/S11-O Segunda sesión Completo.pdf` | 1–28 | Portada 1; Sociales 2–7; Matemáticas 8–12; Ciencias 13–20; Inglés 21–28 |
| `references/S11-M 2DA SESIÓN.pdf` | 1–28 | Portada 1; Sociales 2–5; Matemáticas 6–12; Ciencias 13–20; Inglés 21–28 |
| `references/S11-P s2.pdf` | 1–28 | Portada 1; Sociales 2–7; Matemáticas 8–12; Ciencias 13–20; Inglés 21–28 |

Sus portadas muestran 25 Sociales, 25 Matemáticas, 29 Ciencias y 55 Inglés, 134 en total, con cuatro horas y treinta minutos. Esto describe estos ejemplares editoriales y no acredita autenticidad oficial ni establece una regla universal. No se copiarán marca, personajes o contenido para maquetar SaberPlus. La referencia O tiene un salto en la numeración impresa de su última página: las citas de este informe usan **páginas físicas**, no la cifra de su pie.

Renders individuales: `tmp/pdfs/referencias-estructura-completas/{O,M,P}/01.png` a `28.png`. Láminas completas: `contacto-01.png`, `07`, `13`, `19`, `25`. Inventario con hashes: `inventario.json` en la carpeta superior; copia permanente en `docs/REFERENCIAS_MAQUETACION_INVENTARIO_2026-11-12.json`.

## Organización observada

1. Dos columnas como recurso frecuente, no como obligación para toda la página. Se leen de arriba abajo en la columna izquierda y después en la derecha, con separación central visible en varios ejemplares.
2. Bloques a ancho completo antes, entre o después de columnas: una lectura, tabla o figura ancha puede compartir página con preguntas más pequeñas. No se obtiene necesariamente el mejor resultado fijando una sola distribución para toda la página.
3. Las alternativas gráficas se agrupan como conjunto reconocible. Pueden ir en cuadrícula o en una columna cuando necesitan altura. Su orden y escala no se alteran para conseguir simetría.
4. Los contextos compartidos tienen un encabezado de rango y se imprimen una vez. Las preguntas continúan conservando numeración; una lectura no debe repetirse por cada pregunta.
5. Líneas horizontales separan bloques; la altura se ajusta al contenido, sin un número fijo de preguntas por página.
6. Inglés mantiene instrucciones, ejemplo y composición propia de cada tarea. Hay diferencias entre referencias en el orden de asociación/avisos y en las subdivisiones de partes: no copiar un reparto ajeno sobre el adoptado para SP-001.

## Casos concretos para que Claudia compare

| Archivo / página física | Composición útil para estudiar |
| --- | --- |
| P / 2 | Pregunta 1 a ancho completo y, debajo, lectura/preguntas en dos columnas. |
| P / 4 | Pregunta ancha, lectura compartida ancha y preguntas relacionadas en dos columnas al final. |
| P / 7 | Un bloque ancho inicial seguido de dos columnas de preguntas. |
| P / 13 | Tabla de ancho completo y dos preguntas con gráficos/imágenes debajo en columnas. |
| P / 17 | Tabla/figura ancha arriba, dos preguntas en columnas y otra pregunta a ancho completo al final. |
| P / 20 | Tablas y gráfica de gran ancho con sus preguntas; no forzar dos columnas estrechas para estos estímulos. |
| M / 6–8 | Preguntas con cuatro diagramas, tablas y contextos; el espacio se adapta a la altura real. En p.8 hay bloque ancho inferior. |
| M / 17–19 | Procesos científicos, comparación de diagramas e ilustraciones extensas con sus preguntas. |
| O / 11 | Alternancia de dos columnas con una pregunta/figura ancha inferior. |
| O / 16 | Figuras de Ciencias y bloque ancho inferior. |
| O / 21–28; M / 21–28; P / 21–28 | Recorrido completo de Inglés: avisos, banco de palabras, conversaciones, lecturas y cloze. Varias páginas son una sola **tarea o contexto**, pero contienen múltiples ítems. |

## Aplicación al proyecto actual

El cuadernillo SP-001 segunda sesión auditado tiene 60 páginas, incluidas portada, instrucciones y tres hojas de respuestas. Los ejemplos anteriores tienen 28 páginas físicas, pero no incluyen la hoja de respuestas separada y usan otros tamaños de letra, imágenes y composiciones. **28 páginas no es un objetivo automático para SaberPlus.** El objetivo es aprovechar ancho y altura sin perder legibilidad.

Una página con una pregunta no es necesariamente un error. Distinguir:

- Espacio justificado: diagrama grande, cuatro alternativas complejas, lectura extensa, inicio de área o una unidad editorial que necesita mantenerse junta.
- Hueco evitable: salto manual residual, bloque que reserva demasiada altura, límites de imagen inadecuados, columnas sin aprovechar o un ancho completo que podría alternarse con columnas.
- Página de Inglés con una lectura o cloze: contar las preguntas/huecos vinculados, no solo los recuadros visibles.

En SP-001 segunda sesión conviene comparar las páginas 16, 23, 37, 38, 42 y 49 como candidatas a evaluar por espacio libre; no se ordena compactarlas todas. La p.47 exige el problema inverso: los manómetros del puesto 75 necesitan números legibles y quizá más espacio. Nunca justificar la compresión de esa página mediante el conteo de preguntas.

El motor existente ya tiene `layout`, `options_layout`, tamaños máximos, saltos y `column_flow: balanced`, con límites y excepciones documentados en `docs/ECUACIONES_Y_MAQUETACION.md`. Primero evaluar esos recursos; si el error está en el motor, corregirlo de forma localizada. No reconstruir la aplicación.

## Hoja de respuestas

Las tres referencias anuncian una hoja separada, pero **no incluyen su modelo completo** en estos archivos. No deducir su diseño a partir de las portadas ni afirmar que se revisó una hoja inexistente. El usuario aportará una foto. Hasta verla no se debe decidir el formato final.

Problema actual comprobado: los 134 números y sus alternativas están, pero las tres páginas quedan desequilibradas. Al ajustar, mantener correspondencia única pregunta–fila, Inglés 80–84 con A–G, A–C/A–D en el resto según cada pregunta, y clave docente con una sola marca correcta. No prometer lectura óptica calibrada.

## Límites de esta revisión

Se inspeccionaron todos los folios de estos tres archivos mediante láminas renderizadas; es una revisión estructural global. No equivale a cotejar cada palabra, fórmula, medición o clave de los 402 ítems contra originales externos. Las fotos y PDF actuales que aporte el usuario tienen prioridad para detectar defectos en sus versiones finales.
