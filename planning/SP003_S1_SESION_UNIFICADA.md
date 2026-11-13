# SP-003 · Primera sesión unificada · 12 de noviembre de 2026

Continuación autorizada por el usuario tras interrumpirse el chat: completar Ciencias naturales y reunir toda la primera sesión. Proyecto principal guardado: `data/project.json`, revisión **23**, SP-003, primera sesión, 270 minutos. El estado de 66 preguntas y la separación de Sociales descritos en documentos anteriores son antecedentes de esta integración.

## Contenido y conservación

| Área | Cantidad | Numeración de sesión |
| --- | ---: | --- |
| Matemáticas | 25 | 1–25 |
| Lectura crítica | 41 | 26–66 |
| Sociales y ciudadanas | 25 | 67–91 |
| Ciencias naturales | 29 | 92–120 |

Se recuperó el principal en revisión 22 con 67 preguntas: las 66 de Matemáticas/Lectura y la primera de Ciencias. Se añadieron las otras 28 de Ciencias y las 25 de Sociales del espacio 4187, revisión 5. Las 66 preguntas previas, sus 13 contextos y los 25 registros de Sociales se conservan exactamente. De la pregunta de Ciencias ingresada por el usuario se conservaron texto, opciones, clave, explicación y clasificación; solo se añadió la figura que faltaba y se corrigió su orden dentro del área de 67 a 1. Los espacios paralelos 4186 y 4187 se conservan.

Las 29 de Ciencias usan exactamente la selección publicada en [candidatas y fuentes](SP003_S1_CIENCIAS_CANDIDATAS_29.md). No se añadieron las demás preguntas de los grupos de biomasa y biodigestores. Se conservan sus contextos completos y recursos necesarios. Las explicaciones de las 28 preguntas nuevas son redacción editorial de SaberPlus; las claves se cotejaron con los enunciados y alternativas.

Listas para revisión: [120 códigos en orden definitivo](SP003_S1_CODIGOS_USADOS.txt), [29 códigos de Ciencias](SP003_S1_CIENCIAS_CODIGOS.txt), [25 códigos de Sociales](SP003_S1_SOCIALES_CODIGOS_USADOS.txt). Claves y explicaciones se entregan aparte del estudiante.

## Archivos locales de entrega

Carpeta estable: `output/editor/SP003-primera-unificada-rev23/`.

- `cuadernillo.pdf`: estudiante, **71 páginas**, sin respuestas señaladas.
- `cuadernillo_resuelto.pdf`: **93 páginas**, mismas preguntas, marcas y explicaciones al final.
- `clave_docente.pdf`: clave separada, **3 páginas**.
- `proyecto.json`: respaldo editable de las 120; contiene respuestas, para el equipo.
- `resultado-generacion.json`: mapa de páginas y resultado del generador.
- `auditoria-integracion.json` y `auditoria-pdf.json`: controles de conservación, conteos, claves y límites físicos.
- `SP003_primera_completa.zip`: paquete local para el equipo, con JSON, imágenes, tres PDF separados en estudiante/docente y manifiesto de hashes.

El paquete contiene **54 imágenes**, además del JSON y los documentos. Se verificó su integridad y que todas las rutas de imágenes referidas por el proyecto estén incluidas. El principal se reabrió en **4185**, revisión 23 y 120 registros; recargar la pestaña para recuperar el estado y token actuales.

Los PDF y recursos permanecen locales. El paquete histórico `handoff/SP003_primera/` contiene **66**, no 120: no importarlo para sustituir la sesión actual. Para trasladar la sesión completa usar el paquete local nuevo, con sus imágenes.

## Recursos y composición

Se abrieron los ocho PDF de la selección en modo lectura y se cotejaron sus páginas físicas con las transcripciones. Las fuentes y referencias permanecieron intactas. Se prepararon veinte recursos de Ciencias: dieciocho restauraciones con la herramienta integrada `imagegen` y dos reconstrucciones vectoriales para controlar las escalas de masa/volumen/longitud y la orientación de cargas en solvatación. Las tablas de puertas, isótopos y propiedades se compusieron como tablas nativas, conservando las cifras y la letra Ñ.

Fuentes, versiones descartadas, prompts, correcciones y registros locales: `tmp/sp003/ciencias/carga/`. Consultar `imagenes-finales.json`, `correcciones-imagenes.json`, `precision_vectorial.py` y `contenido.py`. Los recursos finales están dentro de `assets/uploads/` y del paquete local. En la figura de transporte se conserva el rótulo **ABP** tal como se lee en la fuente; queda señalado para revisión editorial como posible errata del original, sin corrección silenciosa.

El motor admite ahora la división de párrafos de contextos de ancho completo entre páginas, con aviso de continuación, sin recortar ni cambiar el JSON. Los recursos indivisibles excesivos mantienen un error explícito. En el avance recuperado de revisión 22, las lecturas caben sin necesitar esas continuaciones; el control coteja íntegramente su texto contra el PDF. No se afirma que el error histórico de revisión 18 siguiera presente en ese archivo recuperado.

Se amplió el límite explícito de figura a **400 puntos solamente en preguntas de ancho completo**; las columnas conservan 240. Se probó con los cuatro gráficos de crecimiento, los modelos de tsunami y las tablas de respuesta de biodigestores. Se añadieron subíndices tipográficos para las fórmulas químicas. No se cambió la letra de los enunciados ni la distribución guardada de las áreas anteriores.

También se corrigieron las descargas grandes del editor en Windows: HTTP/1.1, envío del archivo por bloques de 64 KiB y consumo del cuerpo acotado antes de rechazar una petición no autorizada. Se reprodujeron inicialmente dos errores `WinError 10054`; después de la corrección pasaron los controles de descarga y rechazo de token.

## Verificación y revisión pendiente

Se revisaron las páginas renderizadas del estudiante, el resuelto y la clave, con vistas ampliadas de los recursos corregidos. El control automático comprueba 120 claves, 120 opciones resaltadas del resuelto y 120 encabezados de explicación, además de hojas del estudiante sin círculos rellenos y texto sin salir de la página. Los conteos y hashes definitivos están en `auditoria-pdf.json`. La comprobación visual en pantalla no sustituye una impresión física al 100 %.

Pruebas: 78 del editor aprobadas; seis de superíndices/subíndices aprobadas; comprobación JavaScript del editor y sintaxis aprobadas. El detalle local se conserva en `tmp/sp003/ciencias/carga/pruebas-editor.log`. La prueba de contexto largo verifica que no se pierda ninguna línea, que se conserve el crédito y que el proyecto no cambie al exportar.

`sync_used_questions.py --session primera --check-only` no detecta repeticiones exactas; el registro hipotético pasa de 241 a 295, con las 54 incorporaciones nuevas. **No se sobrescribió el registro maestro**: se mantiene en 241 usadas y 11 reservas hasta la coordinación. El exportable local `uso-para-coordinacion.json` permite tramitar las 120. Continúan los límites históricos del cotejo de variantes y las 25 Matemáticas de SP-001 con códigos USB pendientes; no se certifica unicidad global.

La integración está completa por cantidad. La cobertura editorial sigue mostrando diferencias que no se disimularon cambiando etiquetas:

- Matemáticas: **8 interpretación / 12 ejecución / 5 argumentación**, frente a la meta 9/11/5.
- Lectura: 41 clasificadas en competencia lectora; **procesos específicos pendientes**.
- Sociales: **8 pensamiento social / 10 perspectivas / 7 sistémico**, igual al reparto previsto.
- Ciencias: **8 uso / 10 explicación / 11 indagación**, porque se conservó como explicación la clasificación del usuario en la primera pregunta. La propuesta anterior de 9/9/11 la contaba en uso. Componentes: **9 biológico / 9 físico / 8 químico / 3 CTS**; el cruce por celdas también queda para revisión.

La revisión final del usuario sobre Sociales/Ciencias y estas diferencias permanece pendiente. Se mantiene la condición de borrador editorial, clasificación interna SaberPlus y práctica independiente, sin atribuir validación docente externa o psicométrica.
