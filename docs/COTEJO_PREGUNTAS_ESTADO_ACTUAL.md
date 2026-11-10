# Cotejo de preguntas: estado actual

Fecha: 31 de octubre de 2026.

## Resultado comprobado

- 30 PDF cubiertos por el lote; no se inició el PDF 31.
- 2764 fichas académicas actuales, frente a 2834 anteriores.
- 70 fichas adicionales consolidadas con evidencia: 64 cotejos visuales históricos explícitos y seis coincidencias nuevas verificadas en imágenes lado a lado.
- 723 apariciones académicas exactas adicionales; se conservan 3487 apariciones académicas en total.
- 240 fichas y 48 repeticiones de autoinformes, excluidas del banco académico.
- No se borró ni alteró el contenido de ningún PDF. Se preservaron marcas y fichas previas en un archivo recuperable.
- Los enlaces repetidos apuntan directamente a una ficha existente, sin cadenas. La cobertura por fuente se conserva.

## Lo que todavía NO está terminado

El filtro automático examinó 2834 fichas y produjo 5831 pares candidatos. Tras la consolidación y el registro de variantes explícitas quedan 5680 pares distintos pendientes, que involucran 1975 fichas. No son duplicados confirmados: son casos por contrastar; varios pueden compartir tema sin ser la misma pregunta.
Hay 36 fichas sin clave propuesta cerrada y 1060 con alertas documentadas. Una alerta no equivale siempre a un error: debe leerse y resolverla.
El índice conserva temas, competencias propuestas, claves razonadas y páginas de origen. No contiene todavía todos los enunciados, opciones y recursos separados en el formato del editor/app. Ninguna ficha se declara validada por docente, autorizada comercialmente ni lista para publicación automática.

## Entrega y continuación

- `output/cotejo_30/INDICE.html`: índice local con búsqueda y filtros.
- `indice_editorial.json` y CSV: inventario editorial, NO banco importable.
- `cotejos_pendientes.json`: cola verificable y reanudable de pares.
- `variantes_preservadas.json`: siete relaciones explícitas conservadas en este pase; no representa todas las variantes existentes.
- `archivo_fichas_consolidadas.json`: fichas originales completas y estado previo para recuperación.
- `estado_actual.json`: conteos actuales; sustituye para estos conteos la fotografía histórica de cierre del lote.

Siguiente trabajo: verificar candidatos en sus fuentes y contextos completos, registrar decisión por par, luego transcribir contenido y recursos con permiso de uso, revisar claves y competencias, y finalmente seleccionar la matriz de las dos sesiones. No sustituir estos pasos por similitud automática.

## Validación técnica

23 pruebas USB aprobadas después de añadir pruebas de cadenas/ciclos, conservación de marcas, destinos inexistentes y área de lotes mixtos. Se comprobaron las identidades de las referencias y la igualdad de cobertura antes/después. No se probaron importaciones en la app porque este índice no es ese banco.
