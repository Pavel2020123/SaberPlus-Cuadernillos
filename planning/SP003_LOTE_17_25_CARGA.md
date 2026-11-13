# SP-003 · Carga de Matemáticas 17–25

El usuario pidió retomar el lote después de recibir los códigos de Lectura. Se agregaron las nueve preguntas con sus textos del adjunto, claves, explicaciones y clasificación editorial. **Guardadas por la API de 4185 en `data/project.json`, revisión 17: 25 preguntas de Matemáticas.** Las primeras 16 se conservaron exactamente, incluida la 11, que el usuario pidió no modificar. No se accedió al proyecto paralelo de 4186 para esta carga.

## Códigos cotejados

Todos los prefijos del adjunto eran `USB-1c6462bf5377`; se sustituyeron por las fuentes correctas sin alterar datos, enunciados ni orden de opciones. Las páginas son físicas del PDF.

| Puesto | Código original cotejado | Página física | Clave | Competencia guardada |
| --- | --- | --- | --- | --- |
| 17 | USB-04dc5257ed8b-Q012 | 5 | D | FE |
| 18 | USB-1bc205e23b46-Q040 | 11 | D | ARG |
| 19 | USB-d4e43db6988a-Q017 | 7 | D | IR |
| 20 | USB-2722e7c48dfd-Q039 | 14 | D | FE |
| 21 | USB-d4e43db6988a-Q023 | 9 | A | IR |
| 22 | USB-578d9b20297e-Q027 | 10 | C | FE |
| 23 | USB-e4489f150183-Q024 | 9 | D | ARG |
| 24 | USB-d4e43db6988a-Q006 | 3 | C | FE |
| 25 | USB-d4e43db6988a-Q016 | 7 | B | FE |

Se comprobaron las huellas SHA-256 de seis PDF contra el índice y se inspeccionaron ocho páginas físicas distintas: la misma página del Cóndor Andino contiene los originales de los puestos 19 y 25. Los originales no se modificaron. Referencias completas y huellas en `tmp/sp003/lote17_25/fuentes.json` y en la guía de las 25 candidatas.

## Recursos y composición

- Ocho recursos nuevos mejorados con la herramienta integrada **imagegen**: tabla inicial y cuatro opciones de la 17, Venn de la 19, gráfica polar de la 21 y tabla de la 25. Se conservaron cantidades, regiones, coordenadas, unidades y distractores al comparar visualmente las salidas con los recortes originales.
- Archivos mejorados conservados en `tmp/sp003/lote17_25/*_mejorada-v1.png`, con copia cargada bajo nombres independientes en `assets/uploads/`. Índice local de originales, salidas y rutas cargadas: `tmp/sp003/lote17_25/RECURSOS.md`. Prompts exactos: `tmp/sp003/lote17_25/prompts_imagegen.json`. Las salidas originales de imagegen se conservaron también en su carpeta de generación.
- Preguntas 17 y 21 a ancho completo; las demás en columnas. Opciones de la 17 en cuadrícula A/B, C/D; las restantes verticales. Ninguna comparte contexto. Se eliminaron únicamente el artefacto «Copiar», los valores «Ninguno» de campos opcionales y la repetición del mismo enunciado en «Texto después».
- La expresión de potencias de la 24 se conserva con notación matemática editable: el exponente `x` pasa de carácter Unicode a `\(2^{0} + 2^{1} + \cdots + 2^{x}\)` para imprimirse correctamente. No se cambió la expresión ni su cálculo.

## Verificación y límites

Se comprobaron las nueve claves mediante cálculo independiente: masas 6/2/1 kg, áreas 4/4/4/10 cm², total de las siete regiones 160 y conjunto bicicleta 100, níquel 30 g, radios 20/30/40/60 km, proporcionalidad 1,96 L, dados 2 frente a 6 casos entre 36, ahorro acumulado 750.000 en cuatro meses y media 7 piezas.

Estudiante completo de 25 preguntas: **18 páginas**. Inspeccionadas visualmente las páginas nuevas **15–17** y la hoja de respuestas **18**, sin respuestas marcadas. Se revisó además el lote aislado: tres páginas de preguntas, cinco del resuelto con explicaciones y una de clave; las cinco páginas del resuelto y la clave se inspeccionaron visualmente. No se observaron recortes ni solapamientos en esas vistas. Las cajas de texto del lote quedaron dentro de página, las explicaciones no aparecen en el estudiante y las nueve marcas coinciden con sus claves. No se atribuye una nueva revisión visual completa de las 14 páginas anteriores.

Persiste el error previo de fórmula con saltos de línea en la explicación de la pregunta 2 (`A_{\text{pintar}}...`). Impide el resuelto completo de las 25; no se modificó esa pregunta ni se presenta como verificada esa salida. El estudiante completo y el resuelto/clave aislados del lote sí se generaron. Salidas y comprobaciones locales en `tmp/sp003/lote17_25/`.

El conjunto guardado suma **8 IR / 12 FE / 5 ARG** frente al objetivo 9/11/5. Se mantuvieron las clasificaciones solicitadas; queda un ajuste editorial pendiente sin forzarlas ni sustituir preguntas guardadas sin indicación. No asignar niveles de desempeño ni validación externa.

Consulta tras `git fetch origin`: `origin/main` `d92903a`, registro con 120 usadas y 11 reservas, y propuestas SP-002 `ecb9881`. Sin coincidencia de códigos o equivalencias catalogadas ocupadas para los nueve. `sync_used_questions.py --check-only` sobre la propuesta de 25 no detectó repeticiones exactas y no modificó el registro. La coordinación y el cotejo global de variantes siguen pendientes; estar cargadas no confirma reservas ni permisos comerciales.

Los proyectos, respaldos, imágenes y PDF quedan locales; el commit contiene solo documentación y estados de propuesta/carga. El editor paralelo del usuario continúa independiente.
