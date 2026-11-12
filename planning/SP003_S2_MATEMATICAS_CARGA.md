# SP-003 · Segunda sesión · Matemáticas completa

12 de noviembre de 2026. **25 preguntas de Matemáticas guardadas en 4188, revisión 16**, números **26–50** de sesión. Reparto comprobado: **8 interpretación y representación / 11 formulación y ejecución / 6 argumentación**, clasificación editorial SaberPlus. Revisión individual del usuario e integración del coordinador pendientes.

La segunda sesión reúne **50 de 134 preguntas**: 25 Sociales y 25 Matemáticas. Faltan Ciencias 29 e Inglés 55. Proyecto: `data/parallel/SP-003-segunda-4188/project.json`; continuar agregando áreas a este archivo. Las 25 de Sociales se conservan exactamente como en su revisión 8. La primera sesión conserva revisión 26 / 120 y SHA-256 `b47ae3ab762e32fdc7fc403c9b9d7341c5486597276d38f5bc4528e7aa403388`; no se escribió ni reinició su editor.

## Entrega local para revisar

Carpeta `output/editor/SP003-segunda-sociales-matematicas-rev16/`. Estos PDF contienen **ambas áreas**, con numeración continua:

| Archivo | Contenido | Páginas |
| --- | --- | ---: |
| [cuadernillo.pdf](../output/editor/SP003-segunda-sociales-matematicas-rev16/cuadernillo.pdf) | Estudiante y hoja sin respuestas | 28 |
| [cuadernillo_resuelto.pdf](../output/editor/SP003-segunda-sociales-matematicas-rev16/cuadernillo_resuelto.pdf) | Resaltados, hoja marcada y explicaciones al final | 34 |
| [clave_docente.pdf](../output/editor/SP003-segunda-sociales-matematicas-rev16/clave_docente.pdf) | Clave separada de 50 preguntas | 1 |
| [proyecto.json](../output/editor/SP003-segunda-sociales-matematicas-rev16/proyecto.json) | Respaldo de la revisión guardada; incluye claves | — |
| [paquete-local-con-imagenes.zip](../output/editor/SP003-segunda-sociales-matematicas-rev16/paquete-local-con-imagenes.zip) | JSON y recursos de sus preguntas para trasladar al equipo | — |

[25 códigos, uno por línea](SP003_S2_MATEMATICAS_CODIGOS.txt). [Fuentes, páginas, puestos y justificaciones](SP003_S2_MATEMATICAS_CANDIDATAS_25.md). [Clave razonada separada](SP003_S2_MATEMATICAS_CLAVE.md). [Manifiesto sin claves para coordinación](SP003_S2_MATEMATICAS_COORDINACION.json). Los originales, PDF generados y recursos permanecen locales.

## Contenido y ajustes

Las 25 preguntas tienen caso propio; ninguna requiere un contexto compartido entre preguntas. Se conservan los datos y alternativas de sus originales. Competencia, justificación, tema y subtema presentes; afirmación, evidencia y nivel sin asignar.

- La **45 definitiva es `USB-578d9b20297e-Q039`**, plano del estante. Se retiró `USB-d4e43db6988a-Q009`, caso de 2.000 papas, al identificarlo en la primera sesión de SP-003 con otro código. No usar la propuesta retirada como parte de esta entrega.
- Octubre del gráfico de la 44 conserva **18 °C**, valor del original, frente a 19 del resumen del catálogo. La clave sigue siendo A.
- Se amplió la fracción larga de tarjetas (29), se mejoraron las cabeceras de las cuatro tablas de barcos (42) y se ampliaron las seis fracciones del participante 1 (33). La revisión 16 solo modifica la presentación de esas seis fracciones respecto a la 15; la explicación del estante ya decía correctamente **W y X**.
- Se conservan espacios cuando el siguiente bloque indivisible no cabe. La página 23 contiene solo la 43 y la 24 necesita ancho completo para su gráfico y cuatro carteles. Algunos recursos son recortes del escaneo con ruido de fondo; no se atribuye limpieza completa ni prueba de impresión.

## Controles y alcance

Se inspeccionaron las páginas renderizadas del estudiante, el resuelto y la clave. Frente a la revisión 15 inspeccionada, únicamente cambia la página 18 del estudiante y del resuelto, revisada de nuevo; las otras páginas y la clave coinciden píxel a píxel.

- 50 códigos únicos, 50 claves coincidentes con resaltados, hoja marcada y clave separada; 50 explicaciones numeradas. Las 25 claves de Matemáticas coinciden con las fichas cotejadas y sus razonamientos.
- Estudiante sin resaltados de respuesta ni marcadores pendientes; texto dentro de los límites físicos de los tres PDF.
- Once PDF originales de Matemáticas abiertos, SHA-256 comprobados de nuevo y 19 páginas físicas seleccionadas. La lectura y transcripción visual de fuentes se realizó durante los lotes documentados.
- Sin conflictos por código, equivalencias conocidas o texto exacto en los controles con registro común, reservas publicadas, primera SP-003 y primera SP-002. [Cotejos entre fuentes y descartes](SP003_S2_MATEMATICAS_COTEJOS.md).
- Las 25 primeras de Matemáticas SP-001 se cotejaron recuperando sus fuentes a partir del registro: [mapeo y límites](SP003_S2_MAT_COTEJO_SP001_FUENTES.md). **El PDF/JSON final no se localizó**; no se afirma inspección de ese archivo ni de sus correcciones o maquetación.

Consulta tras `git fetch origin`: main **`8542df4`**, ya integrado; SP-002 **`dfbe592`**. Maestro conservado en **291 usadas / 11 reservas**, sin añadir las nuevas 50. Comando ejecutado:

```powershell
uv run --offline python -B tool/sync_used_questions.py output/editor/SP003-segunda-sociales-matematicas-rev16/proyecto.json --session segunda --check-only
```

Resultado: **sin repeticiones exactas; 341 registros en la integración hipotética**. El coordinador debe integrar desde el JSON y los manifiestos. Los cotejos locales no consolidan el catálogo global ni certifican unicidad de toda la colección. No se atribuye validación psicométrica, revisión externa, prueba interactiva de navegador o impresión física. Evidencia: `auditoria.json`, `cotejo-cierre.json` y `comparacion-renders-rev15.json` junto a los PDF; scripts y fuentes renderizadas en `tmp/sp003/segunda/matematicas/`.

La siguiente área en orden es Ciencias. Mantener retiradas las tres propuestas iniciales ocupadas por SP-002 (`USB-524d98b0a234-Q061`, `USB-709bc037689b-Q051`, `USB-e4489f150183-Q063`) y actualizar main y reservas antes de escoger nuevos lotes.
