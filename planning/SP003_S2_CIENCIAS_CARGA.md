# SP-003 · Segunda sesión · Ciencias naturales completa

12 de noviembre de 2026. **29 Ciencias guardadas en 4188, revisión 22**, números **51–79**. Reparto **9 uso comprensivo / 8 explicación / 12 indagación**, componentes **9 biológico / 8 físico / 9 químico / 3 CTS**. Clasificación editorial SaberPlus; afirmación, evidencia y nivel sin asignar. La sesión reúne **79 de 134 preguntas**; faltan **55 Inglés**. Revisión individual e integración del coordinador pendientes.

**Esta entrega sustituye la revisión 20.** Se reemplazaron las 13 coincidencias con Ciencias SP-001 segunda reveladas por main `519e1aa`: los 12 cruces publicados por el coordinador y papa Q058, equivalente a d4e43db6988a-Q108. El paquete de revisión 20 se conserva como respaldo histórico; no usar sus códigos como selección vigente.

## Archivos locales

Carpeta `output/editor/SP003-segunda-sociales-matematicas-ciencias-rev22/`. Los PDF reúnen Sociales, Matemáticas y Ciencias:

| Archivo | Contenido | Páginas |
| --- | --- | ---: |
| [cuadernillo.pdf](../output/editor/SP003-segunda-sociales-matematicas-ciencias-rev22/cuadernillo.pdf) | Estudiante, sin respuestas | 51 |
| [cuadernillo_resuelto.pdf](../output/editor/SP003-segunda-sociales-matematicas-ciencias-rev22/cuadernillo_resuelto.pdf) | Resaltados, hoja marcada y explicaciones | 62 |
| [clave_docente.pdf](../output/editor/SP003-segunda-sociales-matematicas-ciencias-rev22/clave_docente.pdf) | Clave separada de las 79 preguntas | 2 |
| [proyecto.json](../output/editor/SP003-segunda-sociales-matematicas-ciencias-rev22/proyecto.json) | Respaldo igual al guardado; contiene claves | — |
| [paquete-local-con-imagenes.zip](../output/editor/SP003-segunda-sociales-matematicas-ciencias-rev22/paquete-local-con-imagenes.zip) | JSON y 60 recursos íntegros, con hashes | — |

[29 códigos originales](SP003_S2_CIENCIAS_CODIGOS.txt), [fuentes y clasificación](SP003_S2_CIENCIAS_CANDIDATAS_29.md), [clave razonada separada](SP003_S2_CIENCIAS_CLAVE.md), [manifiesto para coordinación](SP003_S2_CIENCIAS_COORDINACION.json), [trece sustituciones y cotejos](SP003_S2_CIENCIAS_COTEJOS.md).

## Correcciones y controles

- Cuatro contextos completos: glifosato, telescopio, desalinizador y energía, con las seleccionadas contiguas. Se retiró metales al quedar sin preguntas. Ninguna seleccionada necesita resolver una vecina excluida.
- La pregunta **56**, `USB-45e476387c60-Q057`, tiene clave **B**. El índice proponía C, pero B coincide con los cuatro pares de datos del inhibidor. Datos y orden de alternativas conservados; clave, resaltado y explicación reflejan B.
- Páginas renderizadas revisadas, incluidas gráficas, estructuras químicas, hojas y explicaciones. Coinciden **79 claves, resaltados, círculos marcados y explicaciones numeradas**. Estudiante sin respuestas; texto dentro de página.
- Las **50 anteriores permanecen exactamente iguales** a rev. 16; páginas **2–27** de estudiante y resuelto idénticas píxel a píxel. Primera sesión **rev. 26 / 120** intacta, SHA-256 `b47ae3ab762e32fdc7fc403c9b9d7341c5486597276d38f5bc4528e7aa403388`.
- USB reconectada en E:. **11 originales abiertos y SHA-256 cotejados**; 24 páginas seleccionadas y contextos renderizados. Fuentes sin modificaciones.
- Consulta: main **519e1aa**, integrado en **37e4063**, y SP-002 **dfbe592**, más reservas y proyectos guardados. Maestro de la rama: **320 usadas / 11 reservas**. **41 pares directos** cotejados: 25 apariciones equivalentes libres y 16 preguntas distintas. Dos pares apuntan a códigos ocupados pero comparan preguntas distintas: unidades de zinc/HCl frente a piedra, probeta y lápiz. Sin identidades ocupadas en esos controles.
- Comparación textual auxiliar contra Ciencias de primera SP-003 y proyecto SP-002: máximo 0,3667, sin coincidencias altas. No certifica unicidad de toda la colección ni trabajo privado no publicado.
- Paquete verificado: JSON igual al guardado y **60 recursos** íntegros dentro del ZIP. Tres ilustraciones de Ciencias se elaboraron con la habilidad [imagegen](C:/Users/modaf/.codex/skills/.system/imagegen/SKILL.md); demás figuras recompuestas desde originales con herramientas vectoriales. [Recursos y prompts](../output/editor/SP003-segunda-sociales-matematicas-ciencias-rev22/RECURSOS_Y_PROMPTS.md) locales.

Control de integración sin escribir el maestro:

```powershell
uv run --offline python -B tool/sync_used_questions.py output/editor/SP003-segunda-sociales-matematicas-ciencias-rev22/proyecto.json --session segunda --check-only
```

Resultado: **sin repeticiones exactas; 399 registros en integración hipotética**. Selección sustituta publicada en `806b872`. El coordinador debe integrar desde el JSON vigente y los manifiestos. Evidencias locales: `auditoria.json`, `cierre-local.json`, `comparacion-areas-previas.json`, `cotejos-locales.json`, `recursos-sha256.json`, `fuentes.json`. Scripts y renders: `tmp/sp003/segunda/ciencias/`.

PDF, imágenes, proyectos y respaldos permanecen locales. No se atribuye validación externa ni psicométrica. Pendientes: revisión individual, integración del coordinador e Inglés.
