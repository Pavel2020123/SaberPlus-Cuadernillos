# SP-003 · Entrega de ambas sesiones para Pavel

13 de noviembre de 2026. El usuario autorizó publicar esta entrega después de solicitar su preparación sin commit ni push. Destino: rama `trabajo/sp-003`, para ajustes de maquetación del equipo.

- [Descargar ZIP de entrega](../handoff/SP-003_dos_sesiones_2026-11-13_r26-r29.zip), **76.519.364 bytes (72,97 MiB)**.
- [SHA-256 del ZIP](../handoff/SP-003_dos_sesiones_2026-11-13_r26-r29.zip.sha256).
- [Resultado de la verificación final](../handoff/SP-003_dos_sesiones_2026-11-13_r26-r29_verificacion_final.json).

**Contiene claves y explicaciones. Compartir únicamente con el equipo SaberPlus.**

## Contenido y origen

| Carpeta del ZIP | Proyecto vigente | Revisión | Preguntas incluidas |
| --- | --- | ---: | ---: |
| `primera/` | Guardado de 4185, `data/project.json` | 26 | 120: Matemáticas 25, Lectura 41, Sociales 25, Ciencias 29 |
| `segunda/` | Guardado de 4188, `data/parallel/SP-003-segunda-4188/project.json` | 29 | 134: Sociales 25, Matemáticas 25, Ciencias 29, Inglés 55 |

Ambos contenidos cumplen los conteos previstos. No se tomaron muestras, proyectos vacíos ni respaldos antiguos. Cada carpeta incluye su `proyecto.json`, imágenes de preguntas, alternativas y contextos, dos imágenes de portada y la configuración de portada, conservando sus rutas relativas. Las sesiones llevan recursos separados.

El ZIP contiene 128 archivos: los dos proyectos, 118 imágenes, configuraciones y documentos de entrega. Incluye `LEEME.txt`, `SESIONES_Y_RECURSOS.json`, `ARCHIVOS_FALTANTES.txt`, `MANIFIESTO_SHA256.txt`, `VERIFICACION.json` y un comprobador de hashes. El manifiesto cubre los otros 127 archivos; excluye únicamente su propio archivo.

## Advertencia de primera sesión

El contenido de primera tiene sus 120 preguntas completas, pero el campo original `session` vale `"second"`. Se conservó exactamente como estaba, sin modificar preguntas, claves, identificadores, códigos, orden ni distribución.

Con ese valor, una exportación literal selecciona solo 79 preguntas y omite las 41 de Lectura. Pavel debe revisar el selector y elegir **Primera sesión en su copia de trabajo** antes de exportar sus 120 preguntas. La entrega no contiene un JSON corregido automáticamente.

La segunda corresponde correctamente a `session: "second"` y exporta sus 134 preguntas.

## Verificación realizada

- ZIP extraído de nuevo en una carpeta aislada: **127 hashes correctos, 118 imágenes verificadas y ningún archivo faltante**.
- Ambos JSON son idénticos byte por byte a sus originales; los originales permanecen intactos.
- Generación con el motor copiado al entorno aislado y bloqueo de acceso a recursos del proyecto fuera de esa extracción: segunda 134/134, con PDF de 64/82/3 páginas (estudiante/resuelto/clave).
- Primera, sin modificar: exporta 79/120 por la discrepancia descrita. Diagnóstico seleccionando `first` solo en memoria: exporta 120/120, con PDF de 71/93/3 páginas. No se guardó esa modificación en el JSON.
- Los PDF de diagnóstico permanecen locales, fuera del ZIP. El ZIP reúne los proyectos y recursos para que Pavel pueda trabajar la maquetación.
- Solo se pudo comprobar el estado guardado de 4185 y 4188, que coincidía con los archivos. No hubo acceso al estado interno de las pestañas para comprobar o guardar cambios pendientes del navegador.

SHA-256 del ZIP:

```text
5afec6cfd3f77d13667685371ac541f98738cfdb5e869330d09e2bbe7afa077c
```

## Apertura

Leer primero el `LEEME.txt` incluido. Trabajar en dos copias separadas del repositorio, una por sesión, con el motor del commit `97295f1` o posterior. Copiar los recursos y la configuración de cada sesión a las mismas rutas en su copia e importar su `proyecto.json` en el editor correspondiente. Importar reemplaza el proyecto de destino: usar copias de trabajo, sin mezclar sesiones ni sustituir trabajos ajenos.

La publicación del ZIP constituye la entrega autorizada de estos dos proyectos y sus recursos. Los editores originales, los otros respaldos y las demás entregas locales no se modificaron.
