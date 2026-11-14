# SP-002: revisión y aplicación de la plantilla actual

## Entrega vigente

Origen: `E:/SP-002-DOS-SESIONES`, primera revisión 5 y segunda revisión 24. El manifiesto original se comprobó sin fallas. Se trabajó en copias aisladas por sesión; no se mezclaron sus imágenes con SP-001 ni se sobrescribió el paquete recibido.

| Sesión | Preguntas | Estudiante | Resuelto | Clave |
|---|---:|---:|---:|---:|
| Primera | 120 | 58 páginas | 76 páginas | 1 página |
| Segunda | 134 | 50 páginas | 68 páginas | 1 página |

PDF para revisar: `output/SP002_entrega/`. Paquete completo y ZIP: `E:/SP-002-ENTREGA-CORREGIDA/` y `E:/SP002_DOS_SESIONES_PLANTILLA_ACTUAL_2026-11-13.zip`. Cada sesión incluye su JSON, todas sus imágenes vinculadas, motor, configuración, PDF, códigos, clave y equivalencias de numeración. El contenido docente es privado del equipo.

SP-001 quedó adicionalmente guardado, con sus dos ZIP actualizados de citas y seis PDF, en `E:/SP-001-ENTREGA-ACTUAL/`. No se modificó su contenido al preparar SP-002.

## Integridad y coordinación

- 254 preguntas, IDs y códigos únicos; 120 y 134. No faltan recursos: 61 rutas de imágenes en la primera y 43 en la segunda.
- Ningún código coincide con los 254 códigos de la entrega actual de SP-001. Esto comprueba coincidencias exactas; no certifica ausencia de preguntas visualmente equivalentes con códigos distintos ni comparación con SP-003.
- Orden de áreas conservado: Matemáticas, Lectura, Sociales y Ciencias; Sociales, Matemáticas, Ciencias e Inglés. Inglés conserva exactamente sus IDs y orden.
- Los grupos de lectura se mantienen juntos y en su orden interno. Se reorganizan preguntas o grupos completos dentro del área. Cada sesión incluye `numeracion_antes_ahora.json` y `CODIGOS_Y_CLAVES.csv`.
- Se conservan las 254 claves. Los PDF resueltos y la clave se generan desde los mismos JSON y su numeración efectiva; la hoja tiene una fila por pregunta.

## Maquetación

- Se aplicó el flujo adaptativo aprobado: columnas para texto y ancho completo para figuras que necesitan espacio, con rótulos de sesión, separadores y hoja nueva de respuestas.
- La primera composición compatible medía 62 páginas de estudiante y la segunda 54. El reordenamiento medido dio 55 y 50. Tras corregir y ampliar la figura de asteroides, la primera queda en 56 y la segunda en 50. La comparación usa el mismo motor actual; no son cifras de los PDF originales del compañero, que no venían incluidos.
- Los estímulos de las preguntas originales 4, 91 y 112 de la primera se trasladaron íntegros a contextos dimensionados. Así se conserva su legibilidad y se resuelve el uso de alturas de 360 pt que el campo de imagen de pregunta no admite. La figura de asteroides también pasa a un contexto de 400 pt de alto; el resto de las imágenes conserva sus archivos.
- Las alternativas gráficas de la pregunta original 15 se distribuyeron en cuadrícula: el bloque vertical medía 743 pt y excedía la página.
- Se corrigieron en el motor los títulos de área y encabezados de parte que podían quedar solos al pie de una página: ahora se reserva el espacio del primer bloque real.
- Se distinguen referencias bibliográficas en cursiva, gris oscuro y alineadas a la derecha. Se reconocen también fuentes separadas con un solo salto de línea. Las referencias existentes de las preguntas originales 77 y 88 de la primera y 3 de la segunda se identificaron expresamente como fuente.

## Adaptaciones editoriales registradas

Los números siguientes son los del paquete recibido; consultar equivalencias para la entrega reorganizada.

Primera sesión:

- **17:** la escala de la gráfica de asteroides tenía rótulos fuera de orden y no permitía leer coherentemente Hygiea en 220 km. Se corrigió con la herramienta `image_gen` integrada, en dos ediciones, cotejando los seis valores contra la tabla: Ceres 460, Eunomia 140, Hygiea 220, Pallas 260, Psyche 130 y Vesta 280 km. Se conservan la tabla, las barras, sus nombres, la fuente y la clave A; la primera salida que aún intercambiaba 200 y 220 se descartó. Imagen seleccionada: `assets/uploads/980cbeac244160322e7f9f8c6bdfed7b.png`, guardada tanto en el proyecto como en el respaldo. El prompt y el método están en `primera/PROMPT_IMAGEN_ASTEROIDES.txt` del paquete. El original recibido se conserva.
- **34:** errata «El Si» corregida a «Si».
- **77:** el fragmento sí describe cómo Hitler aprovechó el incendio del Reichstag. Se reemplazó la negación contradictoria del enunciado por una pregunta sobre la inferencia respaldada, con distractor B y explicación coherentes. La clave sigue siendo B; no se alteró el fragmento histórico citado.
- **85:** la explicación atribuía un vínculo familiar que no aparecía en el caso; se conserva únicamente el vínculo político.
- **92:** se precisa que al mezclar no se forman sustancias nuevas, en lugar de afirmar que no hay transformación de la materia.
- **94 y 96:** se reúnen bajo el contexto completo del DIU, que aparece una sola vez. Se retira la referencia frágil a la antigua pregunta 94 y el rango se calcula con la numeración real. La pregunta Wi-Fi permanece con su propio contexto y sus imágenes, sin sustituirla por la pregunta retirada anteriormente.
- **94:** se pregunta si los tres modelos de la tabla permiten generalizar a todos los DIU, evitando confundir la definición de hipótesis con la falta de evidencia suficiente. Se conservan los datos y la clave D; se documentan enunciado, opciones y explicación adaptados.
- **103:** se precisa que los microorganismos transforman la lactosa de la leche en ácido láctico.
- **118:** el alcohol al 96 % se identifica como el más concentrado de las dos presentaciones comparadas, sin afirmar que sea la máxima concentración posible.

Segunda sesión:

- **11:** se elimina la ambigüedad entre motivos ambientales y diplomáticos: se pregunta qué opción expresa una preocupación ambiental posible, conservando B. No se afirma cuál fue la prioridad diplomática real de China.
- **12:** en el discurso adaptado se corrige «firmó la independencia» por «firmó la Proclamación de Emancipación».
- **13:** se plantea expresamente un caso hipotético y una perspectiva religiosa particular, evitando afirmar una prohibición general del velo en Francia o una práctica universal de todas las mujeres musulmanas. Se conserva B.
- **56:** el organelo fotosintético se atribuye a las células de plantas descritas, no a todos los organismos autótrofos.

Los JSON originales se incluyen en el respaldo para comparar. `DIFERENCIAS_COMPLETAS.json` recoge todos los campos cambiados por ID, además de los registros editoriales. No se atribuye revisión de docente ni validación psicométrica.

## Comprobaciones y límites

- 136 pruebas automatizadas superadas, comprobación JavaScript del editor y `git diff --check` correctos.
- Control de IDs, cantidades, códigos, claves, grupos, orden de Inglés, numeración impresa, hojas y rótulos de sesión. Sin caracteres de sustitución ni texto fuera de los límites físicos de página en la extracción.
- Revisión visual mediante láminas de los seis PDF y ampliaciones de los bloques delicados. La revisión de láminas no equivale a leer cada palabra a tamaño impreso. Los textos y explicaciones se revisaron editorialmente con las correcciones registradas; no se certifica que los originales estén libres de toda ambigüedad.
- Persisten espacios inferiores por bloques completos y figuras anchas; cada sesión incluye `ESPACIOS_RESTANTES.md`. No se promete una paginación matemáticamente mínima.
- Falta impresión física para comprobar las leyendas más pequeñas de figuras y las burbujas A–G. No se hizo commit ni push ni se modificaron registros de otros compañeros.

## Ajuste posterior de legibilidad

Se ampliaron diez figuras o bloques sin modificar archivos de imagen, contenido, claves ni orden. Primera: preguntas actuales 95, 101, 104 y 109, y esquema de Wi-Fi de 102. Segunda: 61, 73 y 78, tabla del contexto 55-56 y figura del contexto 63-64. Solo cambian image_width e image_height; las proporciones se conservan. El detalle por ID queda en AJUSTES_REDIMENSIONADO.json de cada sesion. La entrega vigente queda en 58/76/1 paginas para la primera y 50/68/1 para la segunda. Las cifras de composiciones previas arriba son antecedentes.
