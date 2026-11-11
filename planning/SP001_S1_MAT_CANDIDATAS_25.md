# SP-001 · Matemáticas de primera sesión · candidatas

10 de noviembre de 2026. Propuesta de selección, no banco final ni reserva global. Solo 1–3 están cargadas en el editor de prueba. No se modificó la matriz de puestos ni se certifican unicidad, permisos o clasificación definitiva. Las ubicaciones proceden de `output/cotejo_30/indice_editorial.json`; 4–6 también fueron mostradas en capturas por el usuario, pero aún falta transcribirlas al editor. Las restantes requieren inspección del enunciado completo, contexto, opciones e imagen. Si depende de otras preguntas, conservar el contexto o sustituir la candidata, nunca inventarlo.

Objetivo editorial: 25 ítems, 9 interpretación/representación (IR), 11 formulación/ejecución (FE), 5 argumentación (ARG). Clasificaciones propuestas del catálogo, sujetas a contraste. No son cuotas oficiales por sesión.

| Orden provisional | ID catálogo | Tema | Página física / pregunta original | Objetivo | Formato propuesto |
|---|---|---|---|---|---|
|1|USB-04dc5257ed8b-Q001|Tarifa de parqueadero|2 / 1|IR|Dos columnas|
|2|USB-91836110f48e-Q002|Sucesión geométrica|2 / 2|FE|Ancho completo|
|3|USB-d4e43db6988a-Q001|Media de edades|2 / 1|FE|Dos columnas|
|4|USB-91836110f48e-Q004|Semejanza y ángulos|3 / 4|ARG|Dos columnas|
|5|USB-b39f1fd42a79-Q001|Promedio e inferencia individual|2 / 1|ARG|Ancho completo|
|6|USB-d4e43db6988a-Q004|Conteo de grupos|3 / 4|FE|Ancho completo|
|7|USB-eee9960ca52a-Q002|Muestra y población|2 / 2|IR|Dos columnas|
|8|USB-1bc205e23b46-Q027|Distribución porcentual|7 / 27|IR|Ancho completo|
|9|USB-04dc5257ed8b-Q002|Volumen de prisma|2 / 2|FE|Dos columnas|
|10|USB-04dc5257ed8b-Q010|Ordenación de frecuencias|4 / 10|IR|Dos columnas|
|11|USB-1bc205e23b46-Q026|Procedimiento algebraico inválido|7 / 26|ARG|Dos columnas|
|12|USB-04dc5257ed8b-Q004|Porcentajes de ahorro|3 / 4|FE|Dos columnas|
|13|USB-1c6462bf5377-Q001|Valor fijo y variable de una donación|2 / 1|IR|Dos columnas|
|14|USB-1c44481d3d4a-Q026|Perímetro de polígonos regulares|11 / 26|FE|Dos columnas|
|15|USB-1bc205e23b46-Q045|Tipo de variable y desviación estándar|12 / 45|IR|Dos columnas|
|16|USB-1c44481d3d4a-Q028|Probabilidad por complemento|11 / 28|FE|Dos columnas|
|17|USB-1c44481d3d4a-Q034|Áreas compuestas y simetría|14 / 34|ARG|Ancho completo|
|18|USB-1c6462bf5377-Q021|Temperaturas positivas y negativas|11 / 21|IR|Dos columnas|
|19|USB-04dc5257ed8b-Q011|Teorema de Pitágoras|4 / 11|FE|Dos columnas|
|20|USB-1bc205e23b46-Q042|Representación algebraica de crecimiento|11 / 42|IR|Dos columnas|
|21|USB-1bc205e23b46-Q041|Tarifas bancarias anuales|11 / 41|FE|Ancho completo|
|22|USB-234fa4e3ddce-Q002|Representación de datos por ternas|2 / 2|IR|Dos columnas|
|23|USB-04dc5257ed8b-Q013|Presupuesto y cambio|5 / 13|FE|Dos columnas|
|24|USB-1c44481d3d4a-Q049|Dimensiones del volumen de pirámide|19 / 49|ARG|Dos columnas|
|25|USB-04dc5257ed8b-Q021|Algoritmo aritmético|7 / 21|FE|Dos columnas|

## Revisión de distribución mixta

Propuesta actual: 19 preguntas en dos columnas y 6 a ancho completo (2, 5, 6, 8, 17 y 21). No es una cuota obligatoria ni una maquetación ya validada. Los formatos 1–6 se proponen con las capturas vistas; 7–25 son tentativos hasta inspeccionar el original. La 4 tiene un procedimiento largo: probar en columna y mantenerlo entero; si no es legible o no cabe, sustituir la candidata por otra compacta de argumentación en lugar de forzar el texto. Las preguntas 5–6 pueden compartir una página a ancho completo; no significan una página por pregunta. No asignar distribución por alternancia mecánica. Se conservan IDs, números y objetivos, sin cambiar los datos guardados del editor. Ajustar 1 y 3 manualmente a «Dos columnas con separador» y revisar paginación antes de aprobar.

## Maquetación

No usar ancho completo para todo. Elegir tras leer cada pregunta: dos columnas para texto y figura compactos; ancho completo para tablas anchas, procedimientos largos o alternativas extensas. Mantener orden, sin reordenar preguntas solo para llenar huecos. Imágenes ajustadas al contenido: horizontales, verticales o cuadradas según el original, nunca deformadas ni obligadas a 600×900. No garantizar tres preguntas por página.

Actual: sin contorno de pregunta, líneas horizontales finas, separador vertical en columnas. Área centrada en encabezado solo en su apertura. Fuente de texto 10 puntos; opciones de ecuación simple en Times con variables cursivas y superíndices. Introducción → imagen → pregunta → opciones. No cambiar datos para hacer variantes.

## Relevo operativo

Proyecto independiente `C:\Users\LENOVO 14ALC6\Desktop\SaberPlus-Cuadernillos`. Leer AGENTS.md, README.md, CONTEXTO.md, docs/EDITOR_LOCAL.md, este documento y docs/SP001_MATRIZ_COBERTURA.md. No tocar Flutter/backend/Docker/credenciales. No inicializar Git ni hacer commits/push/despliegues.

Editor activo usado: http://127.0.0.1:4186/, con datos separados en `tmp/pdfs/tamanos-imagenes-20261110/datos_editor_prueba/project.json`. Código actual SP-IMG-01, no confundir con proyecto final SP-001. No ejecutar `make_editor_size_demo.py --serve` para reiniciar porque primero regenera ejemplos. Usar `serve()` sobre el JSON ya existente. No reemplazar datos por muestras ni recargar con cambios sin guardar. Respaldar JSON antes de reinicios; importar también necesita imágenes en assets/uploads.

El usuario introduce el contenido manualmente. Guiarlo campo por campo: área, tema, subtema, orden, distribución, incluido, contexto, introducción, imagen, pregunta, A–D, clave, explicación y clasificación justificada. No exige revisor docente. `proposed` permite competencia y justificación con afirmación/evidencia nulas; nunca inventar códigos. El catálogo es fuente de localización, no transcripción completa ni clave oficial. Verificar claves por razonamiento, no por resaltados del original.

Las capturas de 4–6 están en la conversación anterior: banderín isósceles (error en paso2, B), libros/promedios (no inferir valores individuales, C), grupos de 4 mujeres y 2 hombres (Y y Z, D). Son referencias para localizar; pedir captura otra vez si no se dispone del texto exacto. Revisar cualquier incoherencia numérica del original, sin corregirla en silencio.

Antes de generar PDFs/capturas, explicar comando y archivos y obtener autorización. Usar copias en tmp/pdfs; nunca sobreescribir fuentes. Validar, generar y revisar PNGs antes de afirmar aprobación visual. Muestra reciente `tmp/pdfs/tres-preguntas-compactas/`: tres preguntas en página3; claves C/D/C; estudiante4páginas con portada, indicaciones y hoja. Esto no garantiza tres ítems arbitrarios por página.
