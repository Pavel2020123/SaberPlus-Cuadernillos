# SP-001 · Informe final de maquetación (ambas sesiones) · 13/11/2026

Continúa y sustituye como estado vigente a `planning/SP001_CORRECCION_MAQUETACION_2026-11-12.md` (avance parcial, que se conserva). Sin commit ni push.

## Paquetes

| Paquete (carpeta + ZIP en `handoff/`) | Estado | Preguntas | Estudiante / resuelto / clave |
|---|---|---|---|
| `SP001_primera_final_2026-11-13` | **Completo y verificado tras extraer** | 120 | 64 / 92 / 1 págs. |
| `SP001_segunda_final_2026-11-13` | **Completo y verificado tras extraer** | 134 | 59 / 80 / 1 págs. |
| `SP001_primera_corregida_2026-11-12` | Avance parcial conservado (sin tocar) | 120 | 63 / 91 / 1 |
| `SP001_segunda_corregida_2026-11-12` | Avance parcial conservado (sin tocar) | 134 | 58 / 79 / 1 |
| `SP001_segunda_completa_2026-11-12_rev89` | Punto de retorno original (sin tocar) | 134 | 60 / 81 / 3 |

Cada paquete final trae `proyecto.json`, `assets/` (imágenes vinculadas y portada), `pdf/` (estudiante, resuelto, clave, guía), `tool/` (motor copiado), `MANIFIESTO_SHA256.json`, `verificar_manifiesto.py`, `LEEME_RESTAURAR.md`, `HUECOS_CONSERVADOS.md`, `comparaciones/` y este informe. Los JSON de partida (primera rev. 102 `ba635bb4…`, segunda rev. 89 `37d59eb0…`) no se modificaron.

## Qué cambió desde el avance parcial

**Motor (afecta a las dos sesiones)**
- Fracciones: antes salían en tamaño de subíndice (33, 38, 44 de segunda; 9, 19 de primera y toda fórmula con fracción). Ahora se imprimen a tamaño completo. Las fórmulas en línea aparte ya no acumulan líneas en blanco. Corregido el solape de opciones cuando una fracción saltaba sola de línea.
- Nuevo control opcional `option_image_height` (40–240 pt) para el alto de las imágenes de las alternativas.
- La imagen de un contexto compartido respeta ahora su `image_height` (antes se ignoraba y siempre se limitaba a 220 pt).
- Se mantienen del avance: hoja de respuestas nueva, subíndices CO₂/F₂₃, bandas de dos columnas para preguntas de un contexto.

**Segunda sesión**
- 30 y 43 (solas en media columna) a ancho completo. 75: alternativas +12 % (máximo que cabe en una página). 57-D: recorte sin la línea del marco.
- Contextos: las imágenes de 63 y 76–78 usan ahora el alto que ya tenían guardado (240 pt, algo mayores); la 78 pasa a la página siguiente. Al contexto 56–58 se le fijó 220 pt, el tamaño con el que ya se imprimía (tenía 235 guardado sin efecto), para no separar la 56 de su estímulo.
- Composición: se probaron combinaciones locales ancho/columnas alrededor de cada hueco, sin reducir imágenes; ninguna mejora. 59 páginas (una más que el avance, por las fracciones a tamaño legible).

**Primera sesión**
- Figuras: ninguna tenía tamaño asignado y caían en el tope por defecto (300×110 pt, letra de ~4 pt en tablas). Se ampliaron 25 figuras con el criterio de la segunda (≈4,6 px por punto, hasta 470×235 pt). Lista en `tmp/fix/s1/figuras_ampliadas.json`.
- Tablas apaisadas comprimidas en columna (6, 18, 20, 24) y 13, 23 a ancho completo conservando o aumentando su tamaño.
- 15 preguntas solas en media columna pasaron a ancho completo (7, 14, 19, 37, 50, 58, 61, 63, 67, 73, 88, 93, 110, 113, 115).
- Combinaciones locales aceptadas: 12–13 y 101–102 en columnas; 53–54 a ancho completo.
- Infografías de contexto: «Pétricor» (38–41) y «Filosofía en viñetas» (57–58) estaban limitadas a 220 pt de alto y su texto no se podía leer; ahora 440 pt. El mapa de «Energías renovables» (92–94) pasa a 300 pt. Es el máximo que deja caber cada contexto con su primera pregunta en la misma página.
- Resultado: 64 páginas (el avance tenía 63 con figuras ilegibles; sin las mejoras de composición habrían sido 67).

No se cambió ningún enunciado, opción, clave, explicación, orden ni contexto. Solo `layout`, `options_layout`, `image_width`, `image_height` (preguntas y contextos), `option_image_height` y las rutas de las imágenes mejoradas de 51, 53, 57 y el contexto 56–58 (segunda).

## Verificaciones ejecutadas (sobre los proyectos finales)

- `unittest discover -s tool -p 'test*.py'`: 136 OK. `node tool/test_editor_live.mjs`: OK. `git diff --check`: limpio.
- Integridad (`verificar_cambios.py` en cada paquete): 120 y 134 incluidas, mismos IDs y orden; diferencias solo en los campos de maquetación/imagen citados; claves = `numeracion_docente.json`; el PDF del estudiante no contiene respuestas ni explicaciones; hoja con una fila por pregunta; todas las imágenes vinculadas presentes (69 y 93).
- ZIP: cada uno se extrajo en una carpeta aislada, el manifiesto dio 0 fallas y el motor copiado regeneró los mismos números de página.
- Revisión visual: segunda, páginas 15–58 en láminas de 8 más ampliaciones de 33, 38, 44, 51, 53, 56–58, 75 y hoja; primera, láminas de todas las páginas de contenido (3–63) de la versión final y ampliación de los tres contextos con imagen y de las fórmulas de 9, 19 y 116; segunda, también las páginas 3–14 (Sociales). Búsqueda automática de cuadrados de sustitución en el texto de estudiante y resuelto de ambas sesiones: ninguno. El resuelto se comprobó en páginas de muestra de ambas sesiones. **No se revisó cada página a tamaño real ni se imprimió.**

## Huecos que se conservan y por qué

Tabla completa por página en `HUECOS_CONSERVADOS.md` de cada paquete (23 páginas en cada sesión con más de 150 pt libres). Motivos:
- La pregunta siguiente no cabe completa (no se divide enunciado/opciones ni se reduce figura o letra).
- Contexto compartido + su primera pregunta no caben: no se separa el estímulo de su primera pregunta (segunda: 56–58, 63; primera: 28–32, 44–48, 52–54, 57–58, 64–66…).
- Cambio de área (cada área empieza en página nueva).
- Un salto manual guardado en el proyecto (59 de segunda), que además necesitaría 688 pt.
No se adelantó ninguna pregunta para rellenar.

## Pendientes

- **Imágenes para Codex** (herramienta de imágenes): lista separada en `planning/SP001_PENDIENTES_IMAGENES_CODEX_2026-11-13.md` (52, 55, 59–62, 75, 49, 42, restos de marca de agua en 51/53, Spider-Wedding; primera sesión sin auditoría de imágenes).
- **Decisiones editoriales del usuario (sin tocar)**: segunda 39 y 49 (dos opciones compatibles), 60 y 79 (alcance/unicidad), 40, 70, 71 (imprecisiones documentadas en la explicación).
- **38 de segunda: no es errata.** Cotejada con el original (`USB-1c44481d3d4a-Q042`, página física 16; captura en `tmp/fix/sheets/orig_q042_p16.png`): el desarrollo del profesor usa x/3 + x/6 y la pregunta final pide x/2 + x/6, igual que en el proyecto. Las opciones (5x/6, 4x/6, 3x/6, 2x/6) y la clave B (4x/6) coinciden. No se modificó.
- Primera sesión, 116: «H₂O₂» salía con cuadrados porque el párrafo lleva una fórmula; corregido en el motor (subíndices también en párrafos con fórmulas).
- Primera sesión, figuras aún pequeñas tras la revisión de 59–63: 118 (rampa; el original solo tiene 688 px de ancho) y las cuatro gráficas de las alternativas de 120. Para herramienta de imágenes o decisión de disposición.
- Segunda sesión, 11 (pág. 7): la cita en imagen tiene letra pequeña en la referencia bibliográfica; legible pero justa.
- Hoja de respuestas: A–G (80–84) con burbuja de 11 pt; sin «Tipo de prueba» ni barras de lector; sin calibración óptica. Impresión física pendiente.
- Primera sesión, textos sobrantes dentro de los contextos (contenido, no se tocó): «Copiar», «Copiar contexto», «Copiar contexto completo», «Copiar texto completo» aparecen impresos en el encabezado o la fuente de los contextos 28–32, 33–37, 42–43, 44–48 y 49–51; la pregunta 33 termina en «…del texto? Copiar». Parecen restos de la carga: confirmar y borrar.
- Primera sesión, alternativas gráficas pequeñas en 95 (ciclo lítico) y 97 (gráficas de barras): la cuadrícula 2×2 limita su ancho; decidir si pasan a una por fila (más páginas) o se mejoran con la herramienta de imágenes.
- Inglés (segunda, págs. 51–58): sin cambios de composición; la Parte 6 es densa, revisar impresa.
- No se añadió prueba automática específica para el solape de fracciones en opciones (se comprobó visualmente en 9 y 19 de primera, 33 y 38 de segunda).
