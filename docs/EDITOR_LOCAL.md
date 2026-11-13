# Editor local de cuadernillos

Estado: primer editor funcional para pruebas editoriales, independiente de la app y el backend.

## Trabajar al mismo tiempo · SP-003

**Cierre de segunda SP-003 · 13 de noviembre:** **4188, revisión 29 / 134**, Inglés 55/55. [PDF, revisión del trabajo del usuario y controles](../planning/SP003_S2_INGLES_CIERRE.md). Las 120 de rev. 28 conservadas y 14 agregadas. Filas de cuatro opciones en parte 7 sin imágenes; instrucciones genéricas resuelven numeración y omiten texto en blanco. 18 pruebas correctas; PDF 64/82/3 páginas. Solo 4188 recargado: recargar su página por token renovado. Primera sesión intacta; revisión individual e integración pendientes.

**Inglés partes 4–5 · 12 de noviembre:** **4188, revisión 26 / 115 preguntas**, Inglés 36/55. [PDF, códigos y controles](../planning/SP003_S2_INGLES_PARTES4Y5_CARGA.md). PDF 60/75/3 páginas; cuatro pasajes completos y adaptación autorizada del lobo ejecutada. El validador admite sufijos .1/.2 para Examen 1/2; dos pruebas de guardado/exportación/registro y 11 de integridad aprobadas. Solo 4188 recargado: recargar su página antes de editar por token renovado. Las 96 anteriores y primera sesión intactas. Quedan 19 Inglés, partes 6–7.

**Inglés parte 3 · 12 de noviembre:** **4188, revisión 25 / 96 preguntas**. Seis conversaciones 91–96; Inglés 17/55. [PDF, códigos y controles](../planning/SP003_S2_INGLES_PARTE3_CARGA.md). Parte 3 en una página con ejemplo textual; PDF 55/68/2 páginas. Las 90 anteriores y primera sesión intactas. Quedan 38 Inglés, partes 4–7; continuar sobre el proyecto actual.

**Inglés parte 2 · 12 de noviembre:** **4188, revisión 24 / 90 preguntas**. Seis avisos 85–90, Inglés 11/55. [PDF, códigos y controles](../planning/SP003_S2_INGLES_PARTE2_CARGA.md). Dos contextos según la fuente, con sus ejemplos; PDF 54/66/2 páginas. Las 84 anteriores y primera sesión intactas. Quedan 44 Inglés, partes 3–7; continuar en el proyecto actual.

**Inglés parte 1 · 12 de noviembre:** **4188, revisión 23 / 84 preguntas**. Cinco de At a Picnic, 80–84, con banco común A–G y ejemplo H. [Entrega y controles](../planning/SP003_S2_INGLES_PARTE1_CARGA.md). Las 79 anteriores y primera sesión intactas. Quedan 50 Inglés, partes 2–7; continuar en el mismo proyecto.

**Cierre de Ciencias de segunda sesión · 12 de noviembre:** **4188, revisión 22 / 79 preguntas**. 29 Ciencias (9/8/12; componentes 9/8/9/3), conservando las 50 anteriores. Se sustituyeron los 13 cruces con SP-001 detectados tras rev. 20 y se corrigió a B la clave del inhibidor. [Entrega, códigos y tres PDF](../planning/SP003_S2_CIENCIAS_CARGA.md). Continuar en `data/parallel/SP-003-segunda-4188/project.json`; faltan 55 Inglés. Primera sesión rev. 26 / 120 intacta. Revisión individual y coordinación pendientes.

**Cierre de Matemáticas de segunda sesión · 12 de noviembre:** **4188, revisión 16 / 50 preguntas**, 25 Sociales intactas y 25 Matemáticas (8/11/6). [Entrega, códigos y tres PDF](../planning/SP003_S2_MATEMATICAS_CARGA.md). Conservar `data/parallel/SP-003-segunda-4188/project.json` y continuar agregando áreas; faltan Ciencias 29 e Inglés 55. Primera sesión rev. 26 / 120 sin cambios. Revisión del usuario y coordinación pendientes. Los cierres anteriores describen revisiones históricas.

**Cierre de Sociales de segunda sesión · 12 de noviembre:** **4188, revisión 8 / 25 preguntas**, reparto 7/10/8, revisión del usuario pendiente. [Entrega y 25 códigos](../planning/SP003_S2_SOCIALES_CARGA.md). Su JSON sigue en `data/parallel/SP-003-segunda-4188/project.json`. Las otras áreas de segunda permanecen vacías. La primera conserva revisión 26 / 120 sin cambios durante este cierre. Reabrir con el mismo espacio y puerto conserva los datos; no importar una plantilla vacía. El estado inicial descrito a continuación es histórico.

**Segunda sesión iniciada:** se abrió **http://127.0.0.1:4188/**, independiente de la primera de 4185 y de los espacios antiguos. Se conserva en `data/parallel/SP-003-segunda-4188/project.json`, con plantilla de 134 puestos, revisión inicial 0 y sin preguntas cargadas. Reabrir: `uv run --offline python -B tool/editor_parallel.py --port 4188 --workspace SP-003-segunda --template planning/starter_projects/SP-003-segunda.json`. [Primer lote propuesto y estado](../planning/SP003_S2_SOCIALES_LOTE01.md).

**Estado posterior a la reanudación del 12 de noviembre:** por autorización del usuario, el principal 4185 reúne ahora la primera sesión completa, **120 preguntas, revisión 23**, incluidas Ciencias 29 y Sociales 25. Los espacios 4186/4187 conservan sus archivos históricos independientes. Ver [entrega y pendientes](../planning/SP003_S1_SESION_UNIFICADA.md). Los repartos de trabajo que siguen son antecedentes.

**Nuevo reparto del 12 de noviembre:** el usuario continúa Ciencias en el principal **4185**. El asistente terminó Sociales en un tercer espacio independiente, **http://127.0.0.1:4187/**, `data/parallel/SP-003-sociales-4187/project.json`, revisión 5, 25 preguntas. Para reabrirlo: `uv run --offline python -B tool/editor_parallel.py --port 4187 --workspace SP-003-sociales`. Su revisión y posterior integración están pendientes; no importar su JSON sobre el principal. El antiguo espacio 4186 conserva Lectura y no se modificó. Ver [informe de Sociales](../planning/SP003_S1_SOCIALES_CARGA.md).

Dos ventanas del mismo proyecto no se sincronizan en vivo: cada guardado envía el JSON completo. Para que el usuario trabaje otra área mientras el asistente carga Matemáticas, se habilitó un segundo editor independiente:

**Actualización del 12 de noviembre:** la integración ya se realizó. El principal tiene las 25 preguntas de Matemáticas y las 41 de Lectura, con 13 contextos, revisión 18. El paralelo conserva exactamente las 41 originales de Lectura, revisión 3. La creación vacía descrita abajo es histórica; reabrir conserva sus preguntas. Las siguientes ediciones no se sincronizan automáticamente. Paquete y límites en [integración y actualización](SP003_INTEGRACION_Y_ACTUALIZACION.md).

| Ventana | Uso acordado | Proyecto guardado |
| --- | --- | --- |
| http://127.0.0.1:4185/ | Proyecto principal; Matemáticas a cargo del asistente durante sus cargas. | `data/project.json` |
| http://127.0.0.1:4186/ | Trabajo del usuario en Lectura, Sociales o Ciencias. | `data/parallel/SP-003-usuario-4186/project.json` |

En 4186 aparece **TU ESPACIO · EDICIÓN PARALELA** y el título de pestaña «Tu trabajo paralelo». Se inició con el JSON vacío de SP-003, primera sesión, 270 minutos; no contiene copias de las 16 preguntas de Matemáticas ni ejemplos. Elegir el área en **Área del banco**, crear sus preguntas y usar **Guardar proyecto**. Descargar periódicamente el respaldo desde **Distribución prevista y respaldo del proyecto → Descargar proyecto JSON**.

La numeración que aparece en ese editor corresponde a su selección local; la definitiva se recalcula al integrar las áreas. No hace falta añadir preguntas vacías de Matemáticas para que Lectura comience en 26. La integración posterior debe reunir preguntas y contextos de ambos proyectos, comprobar códigos/duplicados y revisar los PDF; **importar el JSON paralelo sobre el principal reemplazaría el proyecto**, no lo combina. El asistente no modifica la ventana del usuario mientras este trabaja allí.

Para volver a abrir el segundo editor desde la raíz, si dejó de estar activo:

```powershell
uv run --offline python -B tool/editor_parallel.py --port 4186 --workspace SP-003-usuario
```

Al abrirlo de nuevo conserva el proyecto existente y sus respaldos. Cambiar el nombre del espacio o el puerto crea una ubicación distinta; conservar esos parámetros para continuar el mismo trabajo. No iniciar `editor_server.py --port 4186` para esta tarea: cambiar solamente el puerto mantiene el `data/project.json` principal y no aísla el guardado. No reiniciar el editor 4185 mientras haya ediciones sin guardar.

El lanzador `tool/editor_parallel.py` solo escucha en loopback, limita los nombres de espacio y asigna carpetas distintas por espacio/puerto. Cada proceso mantiene su token local y revisión independientes. Sus respaldos se guardan dentro de su propia carpeta; `data/parallel/` está excluida de Git. Las imágenes y las exportaciones conservan el almacén habitual con nombres UUID independientes; los guardados no sustituyen recursos ajenos.

Verificación: cuatro pruebas en `tool/test_editor_parallel.py` comprueban separación de rutas/revisiones/respaldos, conservación al reabrir y rechazo de plantillas con preguntas. Se comprobaron las dos rutas HTTP, el rótulo de la ventana paralela y el rechazo en 4186 del token de 4185 sin escribir datos. El principal mantuvo las 16 preguntas y su archivo no cambió. No se afirma una prueba completa de clics en navegador.

## Clasificación editorial sin requisito docente

Decisión del usuario, 10 de noviembre de 2026: el equipo SaberPlus clasifica las preguntas. Se elimina del formulario el selector «Propuesta para revisión / Revisada por docente» y los campos de responsable/fecha de revisión. En su lugar, «Añadir clasificación por competencia» permite registrar competencia, afirmación/evidencia y justificación, sin aprobación externa obligatoria.

Se conserva el valor interno `proposed` para compatibilidad y se presenta como «Clasificación editorial SaberPlus», no como validación docente. Los registros históricos `reviewed` conservan sus datos y sus controles de integridad; abrirlos no los modifica ni promueve preguntas nuevas. Editar su clasificación elimina el estado de revisión vigente, sin atribuir el cambio al responsable histórico. No se migran ni sobrescriben proyectos guardados.

Las preguntas sin clasificar generan un aviso informativo; no se exige docente para exportar. Permanecen los controles técnicos de claves, opciones, imágenes, pertenencia de afirmaciones/evidencias y justificación. La guía auxiliar usa el mismo lenguaje editorial. No se asignan niveles oficiales ni se afirma validación psicométrica.

Si hay cambios sin guardar en el navegador, guardar o descargar primero el respaldo JSON antes de recargar. No reiniciar el servicio mientras el usuario esté editando para evitar invalidar su token local. Los PDF antiguos no cambian: este ajuste se aplica al generar nuevos archivos con el servicio actualizado.

## Correcciones de integridad · 10 de noviembre de 2026

- Al cambiar de parte, las opciones que dejan de usarse se conservan en `option_drafts`, incluidas sus imágenes. Regresan al ampliar el formato; también viajan en el respaldo JSON. No se imprime ese archivo de reserva.
- Editar, importar o cargar la muestra oculta las descargas anteriores. Si se edita durante la generación, sus resultados no se presentan como actuales: hay que generar de nuevo.
- Los órdenes deben ser enteros no negativos. Los duplicados del mismo ámbito (área / parte de inglés) permiten guardar el borrador con advertencia, pero bloquean la exportación hasta corregirlos. Tema y subtema vacíos generan advertencias, sin inventar clasificación.
- Se dibujan las imágenes de cada descripción de vocabulario y las de enunciados de espacios. Si un enunciado tiene imagen, no se usa la fila compacta que la omitía.
- El contexto reserva la altura medida de su primera pregunta. Si ambos exceden una página, se pide dividir el contexto o ajustar el ancho; no se separan silenciosamente ni se recortan.
- Las páginas de explicaciones usan la identificación RESUELTO y el aviso de compartir después de la aplicación.

Verificación sin crear documentos: `node tool/test_editor_live.mjs` y `uv run --offline --with reportlab --with pymupdf --with pillow python -B -m unittest discover -s tool -p test_editor_integrity.py -v`.
En enunciados se puede usar `{{numero}}` para imprimir el número final de la pregunta. La demostración de espacios lo utiliza para no arrastrar su numeración histórica al cambiar el orden de sesión.
Los resultados históricos indicados más abajo no certifican esta revisión. La comprobación autorizada de los tres PDF usa `tmp/pdfs/audit-fixes-20261110/`, con una variante de imágenes sintéticas en `image-cases/`; no reemplaza el proyecto guardado.

### Comprobación autorizada de esta revisión

- Muestra de segunda sesión: 20 preguntas; estudiante de 9 páginas, resuelto de 12 y clave de 1. La clave se contrastó letra por letra contra las 20 respuestas seleccionadas.
- Se inspeccionaron las hojas de contacto de las 9 páginas del estudiante y 12 del resuelto, la clave completa y vistas individuales de los casos cambiados: imágenes en asociación/espacios, opción únicamente gráfica y encabezado de explicaciones. No se observaron recortes ni solapamientos en esas vistas. Ningún bloque textual de los tres PDF salió de los límites físicos de página en la comprobación automática.
- Pruebas de salida verifican imágenes mediante fixtures sintéticos, resaltado sobre la opción gráfica, numeración dinámica, continuidad de contexto con primera pregunta larga y rechazo explícito cuando no caben juntos.
- Se mantienen pendientes la prueba interactiva completa en navegador, impresión física y revisión docente de contenido/clasificación. No se certifica un banco comercial ni una distribución oficial por esta comprobación.

## Inicio y recorrido de prueba

### Muestra aislada de imágenes de distintos tamaños

`uv run --offline --with reportlab --with pymupdf --with pillow python -B tool/make_editor_size_demo.py --serve --port 4186`

- Abre http://127.0.0.1:4186. Contiene tres preguntas originales de prueba de Matemáticas, no el proyecto habitual del puerto 4185. Sus guardados van a `tmp/pdfs/tamanos-imagenes-20261110/datos_editor_prueba/`; no se lee ni reemplaza `data/project.json`.
- Imágenes: horizontal 1200×320, cuadrada 600×600 y vertical 360×1000. El generador conserva la proporción, limita ancho/alto y no amplía recursos pequeños. Esto no garantiza que cualquier fotografía de texto sea legible: revisa la resolución y el tamaño impreso.
- `comparacion_tres_paginas.pdf` contiene un extracto de una página del estudiante, una del resuelto y una de la clave. Es una comparación, no un cuadernillo para entregar: incluye las respuestas. Los archivos completos permanecen al lado; el resuelto completo añade las explicaciones al final.
- Para probar manualmente: selecciona cada pregunta, comprueba su imagen, modifica un texto, guarda y pulsa Generar los 3 PDF. Revisa las descargas y vuelve a cargar una imagen desde el equipo. Todo se conserva únicamente en los datos de esta instancia de prueba.
- `tool/check_editor_size_demo.py` verifica las rutas HTTP de carga, PNG de vista previa, guardado con revisión, rechazo de imagen inválida/conflicto y tres descargas. No es automatización de navegador. Su informe es `comprobacion_http.json` dentro de la carpeta de muestra. Las claves de las tres preguntas son A, C y B.

El control de navegador no estuvo disponible durante esta comprobación: no declarar probado el recorrido interactivo de clics. Los PNG de las tres páginas de comparación y del resuelto completo permiten revisar la maquetación sin simular esa prueba.

Desde la raíz de este proyecto:

```powershell
uv run --with reportlab --with pymupdf --with pillow python tool/editor_server.py
```

1. Abrir http://127.0.0.1:4185. Si ya estaba abierto tras una actualización, recargar con Ctrl+F5.
2. Elegir área y pulsar **Nueva pregunta**. Ingresar tema, enunciado y opciones; cargar imágenes cuando corresponda.
3. Observar **Así va tu cuadernillo**. Después de aproximadamente 1,1 segundos sin escribir se solicita la composición; el cálculo agrega su propio tiempo. No es una animación instantánea por pulsación.
4. Elegir dos columnas, recuadro o ancho completo. La vista usa el mismo generador del PDF de descarga, no una imitación HTML.
5. Navegar páginas, ampliar hasta 200 % o seleccionar otra pregunta para ir a su página. En pantallas estrechas el apartado se ubica debajo del formulario. Se puede pausar la actualización automática y usar **Actualizar**.
6. Completar clave y explicación, guardar y pulsar **Generar los 3 PDF**. Se habilitan tres enlaces y un selector para revisar cada archivo sin salir del editor.

## Tres salidas desde el mismo contenido

- `cuadernillo.pdf`: preguntas sin resolver y hoja de respuestas con círculos vectoriales vacíos, sin paréntesis.
- `cuadernillo_resuelto.pdf`: copia de las mismas páginas con la respuesta correcta resaltada y las explicaciones numeradas al final. Identificada como RESUELTO en portada y páginas. La hoja incluida también lleva las respuestas marcadas. En asociación de vocabulario se marca el círculo A–G bajo cada descripción, evitando resaltar un banco común de forma ambigua.
- `clave_docente.pdf`: clave compacta separada, agrupada por área y con un círculo relleno por pregunta. Adapta las letras a A–C, A–D o A–G según el formato.

El renderizado registra en memoria los límites de cada opción; el resuelto se construye sobre una copia exacta del cuadernillo. No marca ni modifica el archivo del estudiante. Las claves y explicaciones se ingresan una sola vez. Se conserva además la antigua `guia_docente.pdf` como salida auxiliar de revisión pedagógica, sin añadir un cuarto botón al flujo principal.

Las descargas son locales. Todavía no hay publicación en internet ni QR. El profesor debe compartir el resuelto únicamente después de la aplicación. Los círculos son para uso manual, no formularios interactivos ni una hoja certificada para lector óptico.

Para experimentar con la muestra: abrir **Distribución prevista y respaldo del proyecto** y cargar las 22 preguntas originales. Reemplaza el proyecto, con confirmación. Primera sesión selecciona 10 y segunda 20 de ese banco compartido: no son simulacros completos. Segunda sesión incluye las siete partes de inglés. No cargar una muestra sobre trabajo propio sin exportar antes su JSON.

## Persistencia y privacidad

- Escucha solo en 127.0.0.1:4185. No se publica en Internet ni conecta a estudiantes.
- Proyecto guardado: `data/project.json`. Copias anteriores: `data/backups/`. El guardado comprueba revisión para evitar sobrescrituras entre ventanas.
- Imágenes verificadas por contenido en `assets/uploads/`: PNG, JPG y WEBP estáticos, hasta 5 MiB y 20 megapíxeles.
- Exportaciones permanentes: `output/editor/<identificador>/`. Los archivos antiguos y referencias se conservan.
- La previsualización recibe una copia de los cambios sin guardar, trabaja en un directorio temporal y conserva hasta seis PDF en memoria del servicio. Páginas PNG se renderizan a petición. Reiniciar el servicio invalida esas vistas, no el proyecto.
- La vista previa no guarda ni genera guía docente; nunca muestra claves, explicaciones o clasificación privada. Preguntas y opciones vacías muestran marcadores visibles de pendiente. No basta para aprobar una exportación.
- El JSON no incorpora archivos binarios: al trasladar el proyecto a otro equipo también se debe copiar `assets/uploads/`.

## Reglas y límites actuales

- Un enunciado escrito íntegramente en **Introducción**, con **Enunciado** vacío, se conserva y se imprime una sola vez. La vista previa no añade un aviso de enunciado pendiente en ese caso; sigue siendo obligatorio que exista texto en al menos uno de los dos campos. Las fórmulas permiten espacios o saltos de línea junto a sus delimitadores, sin reescribir el texto guardado.
- **Encabezados y cambio de área** permite editar título (hasta 120 caracteres) e indicaciones iniciales (hasta 1500) de cada área. Cada área comienza en página nueva, con el título una sola vez en la banda gris; no repite el nombre arriba ni añade conteos. El nombre habitual permanece como encabezado en las páginas siguientes. Los rangos de preguntas se reservan para los contextos, salvo que el editor los escriba voluntariamente en las indicaciones.
- En **Contextos**, el campo **Encabezado del grupo** admite texto libre con `{{desde}}`, `{{hasta}}` y `{{cantidad}}`. Estos se sustituyen por el rango real después de ordenar y seleccionar. Los botones Según el texto / información / gráfica son modelos editables. Dejar vacío activa la frase automática, singular si solo hay una pregunta. No escribir números fijos si se desea actualización automática.
- El contexto incluye un crédito opcional **Fuente** visible en el cuadernillo. El editor no verifica permisos de uso: ingresarlos no concede derechos sobre material ajeno.
- Desde una pregunta se puede **Crear y vincular lectura / contexto**, o **Editar contexto vinculado**. Las demás preguntas se vinculan al mismo contexto mediante el selector. No duplicar la lectura por cada pregunta.
- Orden por perfil de sesión y por parte de inglés; contextos contiguos y numeración final automática. Perfil editorial basado en referencias, no garantía de distribución oficial vigente.
- Asociación A–G con banco común; espacios con opciones A–C o A–D; lecturas compartidas. En huecos usar `{{h1}}` y asignar `h1` al ítem. Deben coincidir los huecos y los ítems incluidos.
- Enunciados, opciones e imágenes se miden antes de dibujar. Los párrafos de contextos de ancho completo que exceden una página se dividen al exportar, con aviso de continuación, sin modificar el contexto guardado ni sus vínculos. Las imágenes y otros recursos indivisibles excesivos producen un error explícito; las lecturas laterales conservan su límite de una columna. Las figuras de preguntas admiten 40–240 puntos de altura en columnas y hasta 400 en ancho completo; el bloque total debe caber sin recortes. Las fórmulas químicas aceptan subíndices Unicode como CO₂ y CO₃²⁻.
- La previsualización tolera enunciados/opciones vacíos y clasificaciones a medio editar, pero no contextos incompatibles ni huecos sin vincular; conserva la última vista válida y explica el error.
- La descarga exige opciones, clave y explicación completas; muestra advertencias de cantidades, tiempo y revisión pedagógica pendientes. Sigue marcada como borrador.
- Catálogo de evidencias parcial. No asigna niveles oficiales ni puntajes ICFES, ni valida psicométricamente preguntas. La hoja de respuestas es de uso manual, no óptico.
- El máximo del modelo es 500 preguntas almacenadas, no una certificación de rendimiento o composición de 500 ítems.

## Comprobaciones realizadas

```powershell
uv run --with reportlab --with pymupdf --with pillow python -m unittest discover -s tool -p test_assessment_metadata.py -v
uv run --with reportlab --with pymupdf --with pillow python -m unittest discover -s tool -p test_editor_preview.py -v
node tool/test_editor_live.mjs
node --check tool/editor_web/app.js
uv run --with reportlab --with pymupdf --with pillow python -m unittest discover -s tool -p test_editor_headings.py -v
uv run --with reportlab --with pymupdf --with pillow python -m unittest discover -s tool -p test_editor_outputs.py -v
```

Resultados: 13 pruebas de clasificación y 8 de copia temporal, PDF, páginas PNG, rutas y protección local aprobadas. La prueba JavaScript comprueba espera al escribir, foco de página, límites, error conservando la imagen anterior, pausa, descarte de respuestas obsoletas, conservación de referencias del formulario al guardar y cambios concurrentes durante el guardado. No equivale a una prueba en navegador.

Inspeccionadas las nueve páginas de una muestra de segunda sesión con bloques de columna, recuadro, ancho completo y formatos de inglés. Pendiente revisar interactivamente en navegador las cargas, el flujo completo y los distintos anchos de pantalla, así como aprobar con el usuario el acabado final. La herramienta de navegador no estuvo disponible en la sesión anterior; no se inventa esa validación.

Actualización de encabezados: cinco pruebas adicionales verifican sustitución de rangos, singular, variables no válidas, límite del título, compatibilidad con proyectos anteriores y salida PDF tras excluir un ítem. La prueba JavaScript también verifica edición del encabezado y creación/vinculación del contexto. Se revisaron las nueve páginas renderizadas de segunda sesión con banda de área, indicaciones personalizadas y fuente. No se modificó el proyecto guardado del usuario para estas pruebas.

Actualización de salidas: cinco pruebas nuevas comprueban los tres archivos, conservación del proyecto, orden de preguntas, explicaciones al final, círculos vacíos/rellenos y marcas de las opciones normales y de inglés. Una prueba HTTP adicional genera los archivos en un directorio aislado y descarga los tres PDF. La prueba JavaScript verifica los tres enlaces y el selector de salida. Se renderizaron las páginas de la muestra de prueba; no se cargó esa muestra en el proyecto del usuario.
# Orden del texto y la imagen

Ajuste de tres preguntas completas: preguntas de ancho completo con separador usan 6 puntos de margen vertical interno y 8 entre bloques, en lugar de 9/14. La altura máxima predeterminada de su imagen pasa a 110 puntos, conservando proporciones, ancho máximo de 300 y fuente de 10 puntos. Los contextos/explicaciones conservan su espaciado. `question_height` mide el mismo margen de la pregunta completa. La muestra `tmp/pdfs/tres-preguntas-compactas/` comprobó las tres preguntas reales en una página; no garantiza tres por página para cualquier contenido.

Clasificación editorial parcial: `proposed` admite competencia y justificación con afirmación/evidencia vacías. Una afirmación explícita incompatible sigue siendo un error; tampoco se admite evidencia sin afirmación. No se rellenan códigos automáticamente. Las revisiones históricas `reviewed` mantienen sus controles completos. Si falla Guardar, no recargar: descargar primero el respaldo JSON del estado del navegador antes de reiniciar/importar.

Encabezado compacto solicitado el 10 de noviembre: el nombre del área aparece centrado entre SaberPlus y el código, únicamente en su página de apertura; no se repite en las páginas siguientes. Ya no se imprime banda gris de área. Las indicaciones personalizadas se conservan debajo del encabezado si existen. Las preguntas, incluidas las distribuciones históricas `boxed` y `full`, usan separación horizontal fina sin contorno redondeado; se conserva el ancho elegido y el separador vertical de columnas. Los contextos compartidos y cuadros de explicaciones no cambian con esta decisión. Los títulos personalizados demasiado largos deben acortarse, no solaparse con la marca/código.

Refinamiento editorial: introducciones y enunciados en letra normal de 10 puntos, separaciones de 5 puntos y opciones separadas por 2. Las imágenes de preguntas se dibujan sin márgenes exteriores casi blancos (tolerancia 8/255), únicamente en memoria; los archivos originales quedan intactos. En ancho completo se limita además el ancho de la figura a 300 puntos. Revisar siempre el resultado si hay marcas muy claras en los bordes. Las opciones que son ecuaciones simples completas, como `G = 2ⁿ⁻¹`, usan Times con variables en cursiva y exponentes reales; no es un editor LaTeX general. El texto común no se interpreta como fórmula ni como HTML. Estos cambios necesitan reiniciar el servicio para verse en la exportación.

Corrección de densidad del 10 de noviembre: las imágenes de preguntas a ancho completo tienen una altura máxima predeterminada de 120 puntos (antes 190), sin deformación ni ampliación. Las preguntas siguen indivisibles; no se garantiza un número fijo por página. El campo JSON opcional `image_height` admite 40–240 puntos. Las potencias pegadas con superíndices Unicode se convierten en texto elevado real, sin interpretar etiquetas HTML del usuario. Muestra aislada reproducible: `uv run --offline --with reportlab --with pymupdf --with pillow python -B tool/check_density_demo.py`, previa autorización de generación. Lee el proyecto guardado del editor de prueba y escribe solo en `tmp/pdfs/ajuste-densidad/`, sin modificarlo. No ejecutar después de añadir más preguntas suponiendo que aún cabrán en una página.

El formulario separa una introducción opcional del enunciado. El orden impreso es número e introducción, imagen, pregunta y opciones, tanto para estudiante como para resuelto. Sin imagen ni introducción se conserva número y enunciado juntos. Los proyectos anteriores no se reescriben: si todo estaba en Enunciado, separa manualmente la introducción al editar. Guarda antes de recargar; el motor Python necesita reinicio para aplicar cambios de generación. No reiniciar con cambios sin guardar.

