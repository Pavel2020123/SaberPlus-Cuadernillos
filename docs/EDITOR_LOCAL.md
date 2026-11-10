# Editor local de cuadernillos

Estado: primer editor funcional para pruebas editoriales, independiente de la app y el backend.

## Inicio y recorrido de prueba

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

- **Encabezados y cambio de área** permite editar título (hasta 120 caracteres) e indicaciones iniciales (hasta 1500) de cada área. Cada área comienza en página nueva, con el título una sola vez en la banda gris; no repite el nombre arriba ni añade conteos. El nombre habitual permanece como encabezado en las páginas siguientes. Los rangos de preguntas se reservan para los contextos, salvo que el editor los escriba voluntariamente en las indicaciones.
- En **Contextos**, el campo **Encabezado del grupo** admite texto libre con `{{desde}}`, `{{hasta}}` y `{{cantidad}}`. Estos se sustituyen por el rango real después de ordenar y seleccionar. Los botones Según el texto / información / gráfica son modelos editables. Dejar vacío activa la frase automática, singular si solo hay una pregunta. No escribir números fijos si se desea actualización automática.
- El contexto incluye un crédito opcional **Fuente** visible en el cuadernillo. El editor no verifica permisos de uso: ingresarlos no concede derechos sobre material ajeno.
- Desde una pregunta se puede **Crear y vincular lectura / contexto**, o **Editar contexto vinculado**. Las demás preguntas se vinculan al mismo contexto mediante el selector. No duplicar la lectura por cada pregunta.
- Orden por perfil de sesión y por parte de inglés; contextos contiguos y numeración final automática. Perfil editorial basado en referencias, no garantía de distribución oficial vigente.
- Asociación A–G con banco común; espacios con opciones A–C o A–D; lecturas compartidas. En huecos usar `{{h1}}` y asignar `h1` al ítem. Deben coincidir los huecos y los ítems incluidos.
- Enunciados, opciones e imágenes se miden antes de dibujar. Un bloque que excede la página produce un aviso; hay que dividir el contexto o elegir ancho completo. No existe aún división automática de lecturas largas ni ajuste manual de saltos.
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
