> **Corrección posterior al cierre provisional:** main `519e1aa` publicó Ciencias SP-001 segunda. La revisión 20 de SP-003 contiene 13 coincidencias, incluida papa Q058/ d4e43db6988a-Q108. Se conserva como respaldo, no como entrega definitiva sin repeticiones. Sustituciones en curso; los controles y afirmaciones de cierre siguientes corresponden al registro anterior.

# SP-003 · Segunda sesión · Ciencias naturales completa

12 de noviembre de 2026. **29 preguntas de Ciencias guardadas en 4188, revisión 20**, números **51–79** de sesión. Reparto comprobado: **9 uso comprensivo / 8 explicación de fenómenos / 12 indagación**; componentes **9 biológico / 8 físico / 9 químico / 3 CTS**. Clasificación editorial SaberPlus, con afirmación, evidencia y nivel sin asignar. Revisión individual del usuario e integración del coordinador pendientes.

La segunda sesión reúne **79 de 134 preguntas**: 25 Sociales, 25 Matemáticas y 29 Ciencias. **Faltan las 55 de Inglés**. Proyecto: `data/parallel/SP-003-segunda-4188/project.json`. Continuar sobre ese proyecto sin importar una plantilla vacía ni el JSON de primera sesión.

## Entrega local

Carpeta `output/editor/SP003-segunda-sociales-matematicas-ciencias-rev20/`. Los PDF incluyen las tres áreas, con numeración continua:

| Archivo | Contenido | Páginas |
| --- | --- | ---: |
| [cuadernillo.pdf](../output/editor/SP003-segunda-sociales-matematicas-ciencias-rev20/cuadernillo.pdf) | Estudiante, sin respuestas | 50 |
| [cuadernillo_resuelto.pdf](../output/editor/SP003-segunda-sociales-matematicas-ciencias-rev20/cuadernillo_resuelto.pdf) | Resaltados, hoja marcada y explicaciones | 61 |
| [clave_docente.pdf](../output/editor/SP003-segunda-sociales-matematicas-ciencias-rev20/clave_docente.pdf) | Clave separada de 79 preguntas | 2 |
| [proyecto.json](../output/editor/SP003-segunda-sociales-matematicas-ciencias-rev20/proyecto.json) | Respaldo guardado; contiene claves | — |
| [paquete-local-con-imagenes.zip](../output/editor/SP003-segunda-sociales-matematicas-ciencias-rev20/paquete-local-con-imagenes.zip) | JSON y 62 recursos referenciados; integridad comprobada | — |

[29 códigos originales, uno por línea](SP003_S2_CIENCIAS_CODIGOS.txt). [Fuentes, páginas, puestos y justificaciones](SP003_S2_CIENCIAS_CANDIDATAS_29.md). [Clave razonada separada](SP003_S2_CIENCIAS_CLAVE.md). [Manifiesto sin claves para coordinación](SP003_S2_CIENCIAS_COORDINACION.json). [Cotejos locales y descartes](SP003_S2_CIENCIAS_COTEJOS.md).

## Contenido y revisión

Se conservan cinco contextos completos: metales, glifosato, telescopio, desalinizador y energía. Las preguntas seleccionadas de un mismo contexto permanecen juntas. El bloque de energía conserva las tres originales, Q067–Q069. No se incorporaron todas las preguntas vecinas de glifosato, telescopio y desalinizador: ninguna seleccionada necesita sus respuestas. Telescopio Q069 se descartó por ambigüedad entre dos representaciones.

Se retiraron las tres candidatas iniciales usadas en SP-002, el detergente enzimático y la extrapolación bacteriana, esta última coincidente con ACN1 Q086. Las preguntas de cromosomas/tamaño, ondas y fracking no forman parte de la selección final. Las advertencias de alcance de los modelos escolares están en las explicaciones: control de hormigas, tratamiento de luz, extrapolación, tintes, gases y prismas.

Se mejoraron cuatro diagramas con la habilidad [imagegen](C:/Users/modaf/.codex/skills/.system/imagegen/SKILL.md), mediante la herramienta integrada, y se cotejaron rótulos, cifras y conexiones. Se corrigió una conexión omitida entre espermatozoide y fertilización antes de incorporar el diagrama. Tablas y otras gráficas se compusieron a partir de los originales con recursos vectoriales. Se ampliaron los rótulos de las alternativas de tortugas, glifosato y papa, y se corrigió la representación de los subíndices de las fuerzas. [Recursos finales y conjunto de prompts](../output/editor/SP003-segunda-sociales-matematicas-ciencias-rev20/RECURSOS_Y_PROMPTS.md) permanecen locales.

Se inspeccionaron las páginas nuevas renderizadas del estudiante, resuelto, explicaciones y clave, incluida la portada actualizada. Los huecos corresponden a bloques indivisibles que no caben después del anterior; no se redujo la letra del cuadernillo para encajarlos. Algunos rótulos de los diagramas compartidos siguen siendo menores que el texto principal; la aprobación individual e impresión física siguen pendientes.

## Comprobaciones

- **79 códigos únicos, 79 claves coincidentes** con resaltados, hoja marcada y clave separada; 79 explicaciones numeradas. Estudiante sin resaltados ni círculos correctos rellenos. Texto dentro de los límites físicos en los tres PDF.
- Competencias y componentes comprobados en el JSON guardado. Las **50 preguntas anteriores permanecen exactamente iguales** a la revisión 16. Páginas **2–27** del estudiante y resuelto idénticas píxel a píxel a esa entrega; cambia la portada por el conteo de Ciencias y se agregan sus páginas y respuestas.
- Primera sesión **revisión 26 / 120**, SHA-256 `b47ae3ab762e32fdc7fc403c9b9d7341c5486597276d38f5bc4528e7aa403388`, intacta. No se escribió ni reinició su editor.
- Diez fuentes PDF de la selección abiertas y con SHA-256 cotejado durante la revisión. La USB dejó de estar accesible en la última comprobación: se conservan todos los renderizados seleccionados y las huellas previas; no se atribuye una nueva lectura de los originales al cierre. Cotejos locales: 74 pares de la cola que tocan la selección, 46 apariciones equivalentes y 28 preguntas distintas; no se consolidó ni modificó la cola global. Las equivalencias de enfriamiento ya constaban en el catálogo.
- Sin conflictos por códigos o equivalencias conocidas frente al registro y reservas publicados. La búsqueda por similitud textual contra primera SP-003/SP-002 no encontró coincidencias altas; es un control auxiliar, no una certificación de unicidad de la colección.
- Paquete local comprobado: JSON igual al guardado y 62 recursos con SHA-256 verificado dentro del ZIP. No se incluyen fuentes PDF.

Consulta: main **`8542df4`** ya integrado y SP-002 **`dfbe592`**. Maestro **291 usadas / 11 reservas** sin modificar. Reservas de la selección publicadas en **`3e743e1`**. Comando de cierre:

```powershell
uv run --offline python -B tool/sync_used_questions.py output/editor/SP003-segunda-sociales-matematicas-ciencias-rev20/proyecto.json --session segunda --check-only
```

Resultado: **sin repeticiones exactas; 370 registros en la integración hipotética**. El coordinador debe integrar desde el JSON y los manifiestos. Evidencias locales: `auditoria.json`, `cierre-local.json`, `comparacion-areas-previas.json`, `cotejos-locales.json`, `recursos-sha256.json` y `fuentes.json`. Scripts y renders en `tmp/sp003/segunda/ciencias/`.

Los PDF, imágenes, proyectos y respaldos permanecen locales. No se atribuye revisión externa, validación psicométrica, impresión física ni prueba interactiva completa del navegador. Pendientes: revisión individual del usuario, coordinación e Inglés.
