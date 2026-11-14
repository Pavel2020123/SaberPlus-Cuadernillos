# SP-003: revisión y plantilla actual

## Entrega

| Sesión | Preguntas | Estudiante | Resuelto | Clave |
|---|---:|---:|---:|---:|
| Primera | 120 | 60 páginas | 83 páginas | 1 página |
| Segunda | 134 | 56 páginas | 74 páginas | 1 página |

Origen conservado: `E:/SP-003_dos_sesiones_2026-11-13_r26-r29/`, revisiones 26 y 29. Los originales, sus imágenes y el manifiesto recibido no se modificaron. Entrega local: `output/SP003_entrega/`. Respaldo: `E:/SP-003-ENTREGA-CORREGIDA/`. ZIP: `E:/SP003_DOS_SESIONES_PLANTILLA_ACTUAL_2026-11-13.zip`.

## Correcciones y maquetación

- La primera estaba marcada como segunda sesión y exportaba solo 79 preguntas: se corrigió el selector en la copia para incluir las 41 de Lectura y obtener sus 120 preguntas.
- Se aplicó el flujo adaptativo: columnas para texto, ancho completo para lecturas y figuras. Se reorganizaron preguntas y grupos completos dentro de las áreas, conservando el orden de áreas, el orden interno de los grupos y todo Inglés. Cambiaron de puesto 101 preguntas en la primera y 67 en la segunda; consultar `numeracion_antes_ahora.json`.
- Los enunciados completos que estaban exclusivamente en `introduction` se trasladaron a `stem`, evitando duplicarlos y resolviendo la validación.
- Las imágenes cuya altura superaba el límite de pregunta se trasladaron a contextos cuando era posible para conservar su tamaño. Los campos de altura sin imagen se normalizaron. La imagen de la última pregunta de la primera, que ya tenía contexto, se mantiene dentro del límite admitido. Se ajustaron dimensiones y alternativas en cuadrícula sin estirar las figuras. Los archivos gráficos recibidos conservan sus hashes; no se reconstruyeron ni editaron con IA.
- Las fuentes se distinguen de las lecturas mediante cursiva, gris y alineación derecha. Se eliminaron dos rótulos residuales «Copiar» de encabezados de Lectura.
- Segunda, pregunta original 55 (`q-sp003-s2-cn-05`, actual 57): los datos posteriores al experimento respaldan una conclusión, no convierten la conclusión en hipótesis previa. Se adaptaron enunciado, distractores, explicación y justificación editorial para preguntar si la evidencia respalda la afirmación sobre algunos catalizadores. Se conserva la clave A y todos los datos experimentales.
- Segunda, pregunta original 18 (actual 17): se corrigió el medio de la referencia de Greta Thunberg de El País a elDiario.es, cotejándolo con la [publicación enlazada](https://www.eldiario.es/internacional/greta-thunberg-parlamento-britanico-volveremos_1_1581512.html). No se modificó el discurso.
- El motor acepta los siete códigos de Inglés con sufijos de examen `.1` y `.2`, conservándolos íntegros. No se inventaron códigos nuevos ni se eliminaron sufijos.
- Se corrigió el motor matemático para admitir saltos de línea dentro de una fórmula de presentación; antes bloqueaba la generación del resuelto de la primera.

Los cambios detallados están en `AJUSTES_*.json` y `DIFERENCIAS_PREGUNTAS_Y_CONTEXTOS.json` de cada sesión. El archivo `original_recibido.json` permite recuperar el contenido recibido. Las instrucciones neutras añadidas a bloques con enunciado íntegro dentro de imagen se documentan en los ajustes de compatibilidad.

## Comprobaciones

- 254 IDs y códigos distintos, con las 254 claves originales conservadas. Distribución 120/134 y cantidades por área intactas. Inglés mantiene sus IDs y orden.
- 54 rutas de imagen de primera y 60 de segunda presentes; archivos gráficos idénticos a los recibidos. Recursos de portada incluidos aparte.
- Sin coincidencias exactas de códigos con las entregas vigentes de SP-001 ni SP-002. Esto no demuestra ausencia de equivalencias visuales entre códigos distintos.
- 138 pruebas automatizadas pasan; comprobación JavaScript del editor superada. Las pruebas nuevas cubren sufijos de examen y fórmulas multilínea.
- Numeración impresa, claves, orden, grupos, rótulos de sesión y filas de las hojas comprobados. Extracción sin caracteres de sustitución ni texto fuera de los límites físicos de página.
- Revisión visual mediante láminas de todas las páginas de los cuadernillos y resueltos y ampliaciones de fórmulas, tablas, imágenes y hojas. La revisión en láminas no equivale a leer cada palabra impresa.

## Límites

Persisten espacios por bloques completos y contextos; se documentan en `ESPACIOS_RESTANTES.md`. No se garantiza un mínimo matemático de páginas. Algunas imágenes originales conservan ruido o texto pequeño: ampliar el tamaño de impresión no recupera detalle ausente del original. Falta impresión física, especialmente de leyendas pequeñas y burbujas A–G. No se atribuye validación psicométrica ni revisión docente externa. No se modificaron SP-001, SP-002, registros globales, servicios ni otros proyectos. Sin commit ni push.
