# SP-001 · Relevo para montar preguntas en equipo

Estado de partida: copia `tmp/pdfs/flujo-mixto/SP-001-flujo-mixto.json` del 10 de noviembre de 2026. Contiene 25 preguntas incluidas de Matemáticas, primera sesión, y un registro excluido. La clasificación editorial de esas 25 suma 9 interpretación, 11 formulación/ejecución y 5 argumentación; eso coincide con el objetivo planificado para ese bloque, pero no certifica que cada clasificación sea correcta. Ninguna de las 25 incluye todavía el código `USB-...-Q...` en el JSON: los vínculos con sus fuentes deben comprobarse visualmente antes de proclamar unicidad global.

## Qué debe cubrir cada cuadernillo

La matriz maestra está en `planning/SP001_MATRIZ_COBERTURA.json`; el desglose legible y sus límites están en `docs/SP001_MATRIZ_COBERTURA.md`. Tiene **254 puestos**, no 254 preguntas listas. Son 120 puestos para la primera sesión y 134 para la segunda. Cada sesión cuenta desde la pregunta 1. Es una planificación de SaberPlus basada en la guía 2026-2; las cuotas enteras por sesión no son oficiales.

| Sesión | Área | Cantidad | Distribución de objetivos |
| --- | --- | ---: | --- |
| Primera | Matemáticas | 25 | Interpretación 9; formulación/ejecución 11; argumentación 5 |
| Primera | Lectura crítica | 41 | Información local 10; articulación/sentido global 17; reflexión/evaluación 14 |
| Primera | Sociales y ciudadanas | 25 | Pensamiento social 8; perspectivas 10; reflexivo/sistémico 7 |
| Primera | Ciencias naturales | 29 | Uso comprensivo 9; explicación 9; indagación 11; también cruzar componente |
| Segunda | Sociales y ciudadanas | 25 | Pensamiento social 7; perspectivas 10; reflexivo/sistémico 8 |
| Segunda | Matemáticas | 25 | Interpretación 8; formulación/ejecución 11; argumentación 6 |
| Segunda | Ciencias naturales | 29 | Uso comprensivo 9; explicación 8; indagación 12; también cruzar componente |
| Segunda | Inglés | 55 | Partes 1–7: 5, 6, 6, 10, 9, 6, 13; respetar letras y contextos de cada formato |

Lectura tiene una competencia lectora con tres procesos/objetivos, no tres competencias oficiales. En Ciencias los componentes biológico, físico, químico y CTS se cruzan con las mismas preguntas; no son preguntas adicionales. No asignar afirmación o evidencia sin comprobar qué exige el ítem. No atribuir nivel de desempeño a una pregunta aislada.

## Demostración de una pregunta

1. Abrir `output/cotejo_30/INDICE.html` y buscar por área/tema. Abrir la ficha y luego **el PDF original**, página física y número de pregunta. La ficha orienta; hay coincidencias y variantes todavía pendientes.
2. Leer enunciado, contexto completo, tabla/gráfico, opciones y respuesta. Si pertenece a un conjunto, reservar el conjunto y mantenerlo unido. Si la clave señalada no cuadra, dejar pendiente y razonar antes de publicar.
3. Consultar el registro único `PREGUNTAS_USADAS_GLOBAL.json` y solicitar al coordinador la reserva del código canónico `USB-...-Q...` antes de transcribir. Comunicar PDF/página/pregunta, puesto y responsable. Buscar ese código, posibles apariciones enlazadas y preguntas visualmente similares. El mismo nombre de archivo no prueba igualdad; distinto archivo no prueba diferencia.
4. En el editor: área y sesión; tema/subtema; orden; distribución; introducción, imagen y enunciado en su posición; opciones A–D (o letras del formato inglés); clave, explicación y competencia con justificación. Conservar literalmente datos, sentido y opciones del original. Las fórmulas usan `\(...\)`; revisar vista previa y PDF a escala de impresión.
5. Guardar proyecto y descargar JSON. El coordinador actualiza el registro con `tool/sync_used_questions.py` y publica el commit. Anotar la ruta de la imagen y el estado de derechos/permiso por separado; una foto mejorada no debe cambiar números, ejes, letras ni geometría.
6. Una sola persona integra los JSON de cada compañero en el proyecto final. Revisar claves, contexto, numeración y los tres PDF antes de marcar **integrada**. No importar un JSON ajeno sobre un proyecto con cambios sin respaldar.

## Cómo evitar que se repitan

Trabajar en bloques distintos: el bloque de Matemáticas de primera sesión está ocupado por la copia actual; los demás pueden tomar, por ejemplo, Lectura de primera sesión y Sociales de segunda sesión. Cada quien usa **su propio JSON y su propia carpeta de imágenes**. El editor local no sincroniza cambios entre equipos y `127.0.0.1` solo apunta al equipo de quien abre el enlace.

El registro único se consulta y actualiza **antes de usar una pregunta**, no al terminar el PDF. El campo `simulacro` permite conservar en un mismo registro SP-001, SP-002 y siguientes: la prohibición de repetir se aplica a todos los cuadernillos, no solo a las dos sesiones de SP-001. Una fila por pregunta canónica; las apariciones en otros PDF van en la misma fila o se enlazan a ella. Si cambia el número o el formato, cotejar enunciado, opciones, datos, contexto e imagen. Las coincidencias exactas pueden detectarse por texto/archivo, pero un escaneo diferente o una pregunta casi igual requiere revisión humana. No marcar como duplicado solo porque comparta tema.

Las 25 filas iniciales están **ocupadas provisionalmente** con los IDs internos del editor, pero sus códigos USB están pendientes. Hasta resolver esos códigos, ningún filtro automático puede garantizar que un compañero no elija alguna de ellas. Como medida inmediata, compartir también el PDF de la primera sesión y prohibir reutilizar visualmente esas 25 preguntas en otro bloque. El registro maestro tiene que estar en una ubicación compartida con un coordinador o control de cambios; repartir copias desconectadas causará conflictos.

## Prompt para usar con Chat al seleccionar

> Trabajamos en el simulacro SP-001 de SaberPlus. Usa únicamente preguntas que estén en los PDF que te mostraré; no redactes preguntas nuevas ni cambies números, opciones o datos. Necesito candidatos para [sesión, área, objetivo y cantidad], según `docs/SP001_MATRIZ_COBERTURA.md`. Para cada candidato entrega: código USB de la ficha, PDF y página física, número original, tema/subtema, tarea cognitiva que realmente exige, competencia propuesta y por qué, dependencia de contexto, tipo de imagen, clave razonada y dudas. Contrasta cada código con nuestro `REGISTRO_PREGUNTAS_SP001.csv`; si ya está reservado, usado o hay una variante pendiente, descártalo o señálalo. No inventes afirmaciones/evidencias ni declares validado lo que no inspeccionaste. Cuando te pase una captura, dame los campos exactos para transcribirla al editor y dime qué debe comprobarse en el original.

En otro chat se puede preparar cada imagen para impresión. Pedir limpieza de ruido/contraste y conservación exacta de rótulos, escalas, valores, símbolos y proporciones; comparar el resultado con el original antes de cargarlo. El chat no ve automáticamente una USB local: hay que adjuntar la página/captura o proporcionar acceso explícito al archivo.

## Límite actual del registro

`PREGUNTAS_USADAS_GLOBAL.json` es el registro maestro para SP-001, SP-002 y los siguientes. Ahora contiene 66 registros usados: 25 de Matemáticas con códigos USB por cotejar y 41 de Lectura crítica (26–66) con códigos vinculados. No quedan reservas de SP-001; ver `planning/SP001_S1_LECTURA_GRUPOS_COMPLETOS.md`. `tool/sync_used_questions.py` agrega preguntas incluidas desde cada JSON guardado, pasa sus reservas al estado usado y rechaza el mismo código o texto normalizado exacto; una variante de escaneo requiere revisión humana. La reserva de candidatos aún es coordinación manual del responsable, no bloqueo en tiempo real. Si dos personas piden la misma candidata, el coordinador decide cuál mantiene el puesto antes de que ambas transcriban.
