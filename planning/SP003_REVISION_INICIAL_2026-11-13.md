# SP-003: recepción y compatibilidad inicial

Origen intacto: `E:/SP-003_dos_sesiones_2026-11-13_r26-r29/`. Manifiesto recibido comprobado sin fallas; no faltan imágenes vinculadas. Copias de trabajo separadas: `E:/SaberPlus_SP003_preparado_2026-11-13/primera/` y `segunda/`.

## Contenido comprobado

- Primera: 120 preguntas, 25 Matemáticas, 41 Lectura, 25 Sociales y 29 Ciencias; 54 imágenes referenciadas.
- Segunda: 134 preguntas, 25 Sociales, 25 Matemáticas, 29 Ciencias y 55 Inglés; 60 imágenes referenciadas.
- Los 254 códigos recibidos son distintos. No hay coincidencias exactas con los 254 códigos de cada entrega actual SP-001 y SP-002. No se certifican equivalencias visuales con códigos distintos.

## Problemas y copias preparadas

La primera estaba marcada como segunda sesión: el selector omitía las 41 preguntas de Lectura. `sesion_corregida.json` corrige exclusivamente ese selector. `original.json` conserva el archivo recibido byte por byte.

En `compatible.json` se trasladaron a `stem` los enunciados existentes que estaban exclusivamente en `introduction`; se conservaron completos. Varias alturas de pregunta excedían 240 pt. Las imágenes sin contexto previo se trasladaron a contextos para conservar su altura; los campos sin imagen se normalizaron a 240; una imagen con contexto previo se limitó al máximo admitido y queda pendiente de revisión visual. Los bloques cuyo enunciado sigue dentro de una imagen trasladada reciben una instrucción neutra. Cada cambio está registrado por ID en `AJUSTES_COMPATIBILIDAD.json`.

Primera: pasa la validación de exportación con 120 preguntas. Esto no demuestra que su composición final esté aprobada.

Segunda: todavía bloqueada por siete códigos con sufijo de subítem que el validador no admite:

- `USB-60fb8a40c3bb-Q010.2`
- `USB-60fb8a40c3bb-Q011.2`
- `USB-60fb8a40c3bb-Q017.1`
- `USB-60fb8a40c3bb-Q018.1`
- `USB-60fb8a40c3bb-Q022.2`
- `USB-60fb8a40c3bb-Q023.2`
- `USB-60fb8a40c3bb-Q024.2`

No se han eliminado sufijos ni inventado códigos alternativos. Hace falta comprobar cómo deben representarse estos subítems antes de modificar el validador o su identificación.

## Alcance pendiente

No se ha completado la auditoría editorial pregunta por pregunta, la revisión visual de imágenes y citas, el reordenamiento dentro de áreas ni la generación y revisión de los seis PDF finales. Los JSON compatibles son copias intermedias, no una entrega final ni sustituyen los originales. SP-001 y SP-002 no se modificaron. Sin commit ni push.
