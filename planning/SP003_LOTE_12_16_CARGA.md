# SP-003 · Carga autorizada de Matemáticas 12–16

11 de noviembre de 2026. Se incorporaron al editor local 4185 las cinco preguntas suministradas por el usuario en su archivo de textos exactos. Proyecto guardado: SP-003, primera sesión, revisión **16**, **16 preguntas**. Se preservaron los once registros anteriores completos, incluida la pregunta 11, que el usuario pidió dejar intacta. El guardado por API comprobó que la revisión de partida 15 no hubiera cambiado y creó su respaldo habitual.

| Puesto | Código de fuente cotejado | Página física / número original | Clave | Clasificación de carga | Composición |
| --- | --- | --- | --- | --- | --- |
| 12 | USB-1c6462bf5377-Q016 | 9 / 16 | A | Formulación y ejecución | Dos columnas, opciones verticales, sin imagen. |
| 13 | USB-1c6462bf5377-Q019 | 10 / 19 | B | Argumentación | Dos columnas, opciones verticales, sin imagen. El enunciado se imprime una vez. |
| 14 | USB-524d98b0a234-Q045 | 16 / 45 | D | Interpretación y representación | Ancho completo, tabla y cuatro opciones gráficas en cuadrícula A/B, C/D. |
| 15 | USB-1bc205e23b46-Q046 | 12 / 46 | D | Interpretación y representación | Ancho completo, tablas con texto intermedio en recurso compuesto y opciones verticales. |
| 16 | USB-d4e43db6988a-Q014 | 6 / 14 | C | Interpretación y representación | Ancho completo, tabla y diagrama lado a lado para legibilidad; opciones verticales. |

Los códigos de 14–16 pegados por el usuario con prefijo AAR1 no identificaban estas tareas. Se sustituyeron por los códigos cotejados de ABJ2, Desierto de la Tatacoa y Cóndor Andino, respectivamente. Se conservaron los textos, temas, subtemas, explicaciones y justificaciones, retirando los artefactos «Copiar». En 13 se trasladó la pregunta final al campo de enunciado para evitar repetirla; en 14 y 16 se tomó una sola vez el texto duplicado bajo dos rótulos del archivo. Las descripciones de las opciones de 14 se conservaron como texto alternativo del recurso; las opciones impresas son las gráficas originales mejoradas, sin añadir esas descripciones al estudiante.

## Recursos y cotejo

Se abrieron las páginas completas y se extrajeron regiones de los PDF originales sin alterarlos. Se cotejaron las huellas SHA-256 de los tres PDF que aportan imágenes. Se usó imagegen para mejorar siete recursos: tabla y cuatro gráficas de 14, conjunto de tablas de 15 y tabla/diagrama de 16. La primera versión vertical de 16 se conservó como variante descartada y se preparó otra horizontal para que sus rótulos se lean a tamaño de impresión.

Se comprobaron cifras, porcentajes, escalas, leyendas y relación entre valores y categorías. En 14 se preservaron los errores intencionales: B sigue con barras 7/8/4/7 sobre eje porcentual y C sigue con 80 % en la cuarta categoría; no se normalizaron los diagramas circulares. En 16 no se añadieron cifras ni porcentajes al diagrama, porque su ausencia es parte de la tarea evaluada. Los originales, las mejoras, los prompts y los respaldos permanecen locales en `tmp/sp003/lote12_16/` y `assets/uploads/`; no se suben a Git.

## Comprobación de salida y alcance

- Estudiante completo de los 16 puestos: 15 páginas. Se inspeccionaron las páginas afectadas 10–14, con los puestos 12–16; la 11 conserva su contenido y recurso anterior, y la nueva 12 aprovecha espacio debajo de ella.
- Revisión aislada del lote, conservando numeración 12–16: estudiante de 4 páginas, resuelto de 6 y clave de 1. Se revisaron las cuatro páginas de preguntas resueltas, las dos de explicaciones y la clave. Claves A/B/D/D/C, marcas y explicaciones coincidentes. No se observaron recortes ni solapamientos en esas vistas; la comprobación automática de texto no encontró bloques fuera de página. Las explicaciones y claves no aparecen en el estudiante.
- Se revisaron cálculos y medidas: 240 libros; contraejemplo a −30 °C para el reloj 1; representación de 70/80/40/70 %; modas 30 y 24, medianas 26 y 24, medias 26 y 24,8 y rangos 10; alcance de información absoluta frente a gráfica sin cantidades.
- El resuelto completo de las 16 sigue impedido por una fórmula preexistente con saltos de línea en la explicación de la pregunta 2. No se alteró esa pregunta. La revisión aislada certifica únicamente las salidas del lote, sin declarar terminada la exportación completa.

Se integraron los cambios publicados de `origin/main`, commit `52bcf74`, sin sobrescribir los datos locales. El registro común consultado contiene 91 preguntas usadas de SP-001 y cero reservas; se consultaron además las propuestas SP-002 en `ecb9881`. No apareció conflicto de código en los cinco puestos. Tras guardar, `tool/sync_used_questions.py data/project.json --session primera --check-only` no detectó repeticiones exactas; no se actualizó el registro maestro ni se atribuyó confirmación de reserva. El cotejo global de variantes y la coordinación siguen pendientes.

La clasificación IR de la 15 se conservó por indicación del usuario y compensa el cambio FE de la 11. La comprobación directa del JSON mostró además que el usuario ya tenía la 9 como FE, frente a la IR propuesta; se conservó sin editarla. Los 16 guardados suman **6 IR / 7 FE / 3 ARG**. Los puestos 17–25 siguen pendientes de carga y sus candidatas actuales aportarían 2 IR / 5 FE / 2 ARG, dando 8/12/5 en total. El objetivo editorial sigue siendo 9/11/5: queda revisar una sustitución en los puestos pendientes, sin forzar clasificaciones ni tocar otras preguntas. No se exige revisión docente ni se atribuye validación externa o psicométrica.
