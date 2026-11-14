# Ciencias de segunda sesión: cierre de carga local

12/11/2026. Proyecto `tmp/editor-sp001-segunda/project.json`, revisión 88 al cierre. Editor local: http://127.0.0.1:4188.

- Ciencias: 29 incluidas, 29 códigos únicos, puestos 51–79 completos. Coinciden los 29 códigos con `SP001_S2_CIENCIAS_SELECCION_29.md`, sin faltantes ni códigos ajenos.
- Clasificación editorial: 12 indagación, 8 explicación y 9 uso comprensivo.
- Segunda sesión: 134 incluidas (25 Sociales, 25 Matemáticas, 29 Ciencias, 55 Inglés).
- Contextos compartidos únicos: metales (56–58) y trituración criogénica (76–78).
- Puesto 75, USB-91836110f48e-Q105: clave previa A corregida a B por cotejo de termómetros y agujas de presión. Corrección registrada en la selección y explicación.
- Puesto 79, USB-d4e43db6988a-Q108: clave C. Mejoras de las cuatro alternativas cotejadas: A 30/60/30 s, escala 0–70; C 120/60/30 s, escala 0–140; circulares sin valores añadidos. Vista inspeccionada en `tmp/pdfs/naturales-s2-q079/vista-web.png`.

## Alcance de las comprobaciones

Validación estructural mediante `tool/editor_model.py`, guardados con revisión y comprobación posterior por API. Inspección de las páginas de vista previa de las cargas con imágenes. Esto no equivale a auditoría editorial y visual integral de los tres PDF finales, impresión física o validación psicométrica.

## Pendientes que NO están cerrados

- Corregir imágenes anteriores reconstruidas por código: el usuario exige mejorar las originales con la herramienta de imágenes. Revisar particularmente puestos 52 y 59–62; conservar escalas, alturas y geometría originales. No presentar los trazados aproximados de 60/62 como datos exactos.
- Pendientes previos del relevo: fondo del modelo de metales; dibujos de las alternativas del puesto 57 reemplazados por recuadros; cotejo de la gráfica del puesto 55.
- Revisar el tamaño impreso de números en los manómetros del puesto 75: los archivos mejorados son legibles ampliados, pero las cuatro alternativas se reducen en una página con enunciado extenso. No modificar silenciosamente el generador para resolverlo.
- La alternativa B del puesto 79 también ordena sectores por tamaño; mantener la observación editorial sobre la elección de barras frente a sectores y revisar la claridad de la clave C en la auditoría final.
- Pendientes generales previos: fórmulas pequeñas, observaciones de Matemáticas, subíndices, hojas de respuestas y auditoría conjunta de maquetación.
- Registro global de códigos: Ciencias todavía no sincronizadas. No se ejecutó sincronización, commit ni push. Hacerlo solo cuando el usuario lo indique; empezar por `--check-only`.
- El paquete portable anterior contiene Matemáticas e Inglés; no respalda esta carga de Ciencias. Preparar actualización solo cuando se solicite.

Los respaldos previos de cada carga y las imágenes de revisión de este chat se conservan bajo `tmp/pdfs/naturales-s2-*`. No se modificaron originales ni primera sesión.
