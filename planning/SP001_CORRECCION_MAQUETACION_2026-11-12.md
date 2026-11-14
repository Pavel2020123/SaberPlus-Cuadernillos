# Corrección de maquetación SP-001 (ambas sesiones) · 12/11/2026

Trabajo en copias separadas. Los JSON de partida no se modificaron (SHA-256 en `tmp/fix/HASHES_INICIALES.txt`): primera rev. 102 (`ba635bb4…`), segunda rev. 89 (`37d59eb0…`). El paquete `handoff/SP001_segunda_completa_2026-11-12_rev89/` sigue siendo el punto de retorno y verifica OK.

## Entregas (separadas, con imágenes, manifiesto SHA-256 y ZIP verificado al extraer)

| Sesión | Carpeta / ZIP | Preguntas | Estudiante / resuelto / clave | Antes |
|---|---|---|---|---|
| Primera | `handoff/SP001_primera_corregida_2026-11-12` | 120 | 63 / 91 / 1 págs. | 68 / 96 / 3 |
| Segunda | `handoff/SP001_segunda_corregida_2026-11-12` | 134 | 58 / 79 / 1 págs. | 60 / 81 / 3 |

Cada paquete regenera, con su motor copiado, los mismos PDF (comprobado tras extraer el ZIP).

## Cambios

1. **Hoja de respuestas y clave** (`tool/editor_pdf.py`): rediseñada según la foto del usuario. Marco «SABERPLUS», nombre y apellido, fecha, identificación, tipos de marcación, instrucciones, cinco columnas con una fila por pregunta (120 / 134), «S» de marca de agua como imagen (no entra en el texto) y sin referencias a la universidad. Se omitió «Tipo de prueba» (solo hay una versión) y las barras laterales de lector óptico (no hay calibración). Las filas A–G (80–84 de segunda) usan burbujas de 11 pt frente a 12 pt de las A–D; quedan legibles pero justas.
2. **Subíndices** (CO₂, F₂₃, F₁₃): ahora se dibujan como subíndice real; el texto del JSON no cambió.
3. **Bandas con contextos** (motor): las preguntas en columnas de un contexto compartido ya dibujado se reparten ahora en dos columnas en lugar de apilarse en la izquierda dejando la derecha vacía. Afecta a Lectura de la primera sesión (68 → 63 pág. junto con la hoja). Sin cambios para contextos `side_by_side`, Inglés ni preguntas con salto explícito.
4. **Imágenes mejoradas desde los originales** (segunda; originales conservados, nuevas con nombre distinto; ver `tmp/fix/s2/imagenes_cambiadas.json`): 51 y 53 (tablas: encabezados completos), 57 (cuatro alternativas con los dibujos originales y la secuencia de cada una cotejada), contexto 56–58 (sin marca de agua, texto superior cortado ni borde). Método: recorte a alta resolución del PDF fuente + ajuste de niveles para quitar la marca de agua gris; no se hizo limpieza morfológica porque alteraba cifras. **No se usó una herramienta generativa de imágenes** (no disponible en esta sesión).

## Composición: medición y decisión

- Todos los huecos de la segunda sesión se deben a que la pregunta siguiente no cabe completa (ninguno a saltos manuales). Faltan entre 0 y 178 pt en las págs. 12, 16, 20, 22, 23, 27, 32, 36, 37, 38, 42, 43.
- Se probó pasar a columnas todo lo elegible (texto puro o figura sin pérdida de tamaño): empeora (57 → 58–62 págs.), porque las figuras apaisadas (27, 29, 35, 36, 40, 42, 45, 52, 53, 59, 60, 72…) quedarían al 50 % de su tamaño impreso y el texto largo rinde más a ancho completo. Se mantiene ancho completo; no se reordenó ni se redujo nada.
- Optimizador por conmutación (sencillo y por pares/tríos): sin mejora útil; descartado.

## Verificaciones ejecutadas

- `unittest discover -s tool -p 'test*.py'`: 136 pruebas OK (132 previas + 4 nuevas en `test_answer_sheet_and_bands.py`; `test_editor_outputs.py` se adaptó al nuevo tamaño de burbuja y al círculo de ejemplo).
- `node tool/test_editor_live.mjs` OK, `node --check tool/editor_web/app.js` OK, `git diff --check` limpio.
- Integridad (`tmp/fix/verificar.py`): 134 y 120 incluidas; mismos IDs y orden; segunda: solo cambian `image`/`options.image` de 51, 53, 57 y la imagen del contexto 56–58; primera: ninguna diferencia. Claves = `numeracion_docente.json`; el PDF del estudiante no contiene «Respuesta correcta» ni explicaciones; la hoja tiene 1 fila por pregunta.
- Revisión visual: láminas de las páginas del estudiante de ambas sesiones (no se revisó una por una a pleno tamaño), páginas ampliadas de 51/53/56–58, hoja y clave de ambas sesiones.

## Pendientes

- Herramienta de imágenes para 52 y 59–62 (reconstrucciones por código), 55 (cotejo de la gráfica), 75 (manómetros pequeños), 33/38/44 (fórmulas pequeñas). Quedan restos tenues de marca de agua en las tablas 51/53 y una línea punteada del marco en la alternativa D de 57.
- Tabla de 59: texto cercano al borde derecho de la celda; revisar.
- Decisiones editoriales sin tomar: 39, 49, 60, 79 (ambigüedades), 40, 70, 71 (imprecisiones).
- Inglés (pp. 54–57 de la segunda): sin cambios; revisar tamaño impreso.
- Hoja: sin calibración óptica; A–G justas. Impresión física pendiente.
- Primera sesión: aún hay huecos de entre 20 % y 60 % en varias páginas (p. ej. 6, 19, 26, 36, 54, 62); no se hizo auditoría de imágenes ni de defectos finos como en la segunda.
- Sin commit ni push.
