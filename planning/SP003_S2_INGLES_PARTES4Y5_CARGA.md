# SP-003 · Segunda sesión · Inglés · Partes 4 y 5 cargadas

12 de noviembre de 2026. **4188, revisión 26 / 115 preguntas**: 25 Sociales, 25 Matemáticas, 29 Ciencias y **36 de Inglés**. Se agregaron **19 preguntas**, parte 4 (10, puestos 97–106) y parte 5 (9, puestos 107–115). Quedan **19 Inglés, partes 6–7**. Se mantiene el reparto previsto 5/6/6/10/9/6/13.

| Sesión | Parte | Código original | Clave | Física / original / examen |
| --- | --- | --- | --- | --- |
| 97 | 4 | `USB-709bc037689b-Q100` | A | 37 / 100 / — |
| 98 | 4 | `USB-709bc037689b-Q101` | B | 37 / 101 / — |
| 99 | 4 | `USB-709bc037689b-Q102` | A | 37 / 102 / — |
| 100 | 4 | `USB-709bc037689b-Q103` | C | 37 / 103 / — |
| 101 | 4 | `USB-709bc037689b-Q104` | B | 37 / 104 / — |
| 102 | 4 | `USB-709bc037689b-Q105` | A | 37 / 105 / — |
| 103 | 4 | `USB-709bc037689b-Q106` | B | 37 / 106 / — |
| 104 | 4 | `USB-709bc037689b-Q107` | C | 37 / 107 / — |
| 105 | 4 | `USB-60fb8a40c3bb-Q010.2` | B | 16 / 10 / 2 |
| 106 | 4 | `USB-60fb8a40c3bb-Q011.2` | A | 16 / 11 / 2 |
| 107 | 5 | `USB-7882c8f9ae2f-Q108` | C | 32 / 108 / — |
| 108 | 5 | `USB-7882c8f9ae2f-Q109` | A | 32 / 109 / — |
| 109 | 5 | `USB-7882c8f9ae2f-Q110` | A | 32 / 110 / — |
| 110 | 5 | `USB-7882c8f9ae2f-Q111` | B | 32 / 111 / — |
| 111 | 5 | `USB-7882c8f9ae2f-Q112` | C | 32 / 112 / — |
| 112 | 5 | `USB-7882c8f9ae2f-Q113` | A | 32 / 113 / — |
| 113 | 5 | `USB-7882c8f9ae2f-Q114` | B | 32 / 114 / — |
| 114 | 5 | `USB-60fb8a40c3bb-Q017.1` | A | 10 / 17 / 1 |
| 115 | 5 | `USB-60fb8a40c3bb-Q018.1` | C | 10 / 18 / 1 |

## Entrega local

Los PDF reúnen las cuatro áreas cargadas en `output/editor/SP003-segunda-ingles-partes4y5-rev26/`:

- [Estudiante](../output/editor/SP003-segunda-ingles-partes4y5-rev26/cuadernillo.pdf): 60 páginas; parte 4 en 54–55 y parte 5 en 56–57.
- [Resuelto](../output/editor/SP003-segunda-ingles-partes4y5-rev26/cuadernillo_resuelto.pdf): 75 páginas; explicaciones nuevas en 73–75.
- [Clave separada](../output/editor/SP003-segunda-ingles-partes4y5-rev26/clave_docente.pdf): 3 páginas.
- [Proyecto](../output/editor/SP003-segunda-ingles-partes4y5-rev26/proyecto.json) y [paquete con 60 recursos](../output/editor/SP003-segunda-ingles-partes4y5-rev26/paquete-local-con-imagenes.zip), con claves. JSON idéntico al del editor; ZIP y hashes de recursos comprobados.

## Fuentes y adaptación autorizada

Se abrieron tres PDF en E: y se comprobaron sus huellas. Se revisaron las páginas originales renderizadas y la tabla de claves de 2019:

| Fuente | Físicas consultadas | SHA-256 |
| --- | --- | --- |
| USB-709bc037689b, 2026-1-ACC2 | 37 | `fbf1ad538fa4ceb1782ed4577449c6f12806b898e6a51158c3080751cf7e3752` |
| USB-7882c8f9ae2f, Santuario de Las Lajas | 32 | `22510fdc6a75c4239aa6f81e2f04a361e0100a54a0b74bc3ce6465befe503cc6` |
| USB-60fb8a40c3bb, Inglés 2019 | 9, 10, 16, 20 | `9ff08eb8dfaf2ce225a4f3c76c280131498e31bda9518174a224d5e301760459` |

Se conservan completos **Jane Austen (8)**, **The Ethiopian Wolf (2)**, **I’ll Be a Nurse (7)** y **James Salter’s Days in Film (2)**, con todos los enunciados y opciones seleccionados. Los cuatro ejemplos 0 conservan respuesta A y no cuentan como ítems. Se recompusieron textos y opciones sin copiar marcas, fotografías ni ilustraciones; no se agregaron recursos gráficos.

En The Ethiopian Wolf se ejecutó la adaptación ya autorizada: espacios originales **12 These, 13 largest, 14 in** completos en el cuerpo del pasaje, sin número ni ítem evaluado. Solo se evalúan los originales 10 y 11, ahora 105–106. No se modificaron sus opciones. La adaptación de Valentine’s Day (parte 7) sigue pendiente.

Los sufijos **.1/.2** se conservaron en proyecto, manifiestos y registro para distinguir los exámenes de la fuente de 2019. Se actualizó `tool/editor_model.py` para admitirlos, con dos pruebas que comprueban guardado, exportación y registro sin truncarlos, y rechazo de otros sufijos. Pasaron además las 11 pruebas de integridad del editor. Se recargó únicamente 4188 con el mismo espacio y el archivo guardado intacto; **recargar la página de 4188 antes de seguir editando**, pues cambió su token local. La primera sesión y otros editores no se modificaron.

## Revisión y coordinación

Se inspeccionaron los renders de las cuatro páginas nuevas del estudiante y resuelto, las explicaciones y la clave. Las **115 claves, 115 resaltados y 115 explicaciones numeradas** coinciden. Texto y opciones de los cuatro pasajes completos comprobados en el PDF, incluidas las tres palabras no evaluadas. El pasaje de Salter coincide con el texto extraído de su original. La 115 conserva C según la tabla del Examen 1; la explicación responde al relato fuente sin atribuir verificación biográfica externa. Clasificación editorial SaberPlus: competencia comunicativa, partes 4/5, sin nivel ni validación externa.

El estudiante no contiene respuestas de ítems evaluados; conserva solo ejemplos y las palabras completadas expresamente autorizadas. Texto dentro de los límites de página. Las **96 preguntas y todos los contextos anteriores permanecen iguales**; páginas **2–53** del estudiante y resuelto idénticas píxel a píxel a rev. 25. Primera sesión rev. 26 / 120 intacta: SHA-256 `b47ae3ab762e32fdc7fc403c9b9d7341c5486597276d38f5bc4528e7aa403388`.

Referencias remotas actualizadas: main `519e1aa`, SP-002 `d0f6e31`, sin novedades. Sin repeticiones exactas detectadas en el control del registro; equivalencias conocidas excluidas. No se certifica unicidad de toda la colección.

Maestro: **489 usadas = 254 SP-001 + 235 SP-003**; **98 reservas = 11 previas + 19 Inglés pendientes + 68 equivalencias**. Se conservaron los 470 registros usados anteriores; se agregaron estas 19 y se retiraron sus reservas principales. Publicar documentación, ajuste de validación, pruebas y registros en trabajo/sp-003. PDF, proyectos, imágenes y respaldos permanecen locales. Revisión individual e integración del coordinador a main pendientes.

Evidencias: `auditoria.json`, `cierre-local.json`, `fuentes.json`, `recursos-sha256.json`; scripts, fuentes renderizadas y respaldo previo en `tmp/sp003/segunda/ingles/partes45/`.

**Siguiente:** parte 6, seis preguntas 116–121. Luego parte 7, trece preguntas 122–134, con la adaptación ya autorizada de Valentine’s Day.
