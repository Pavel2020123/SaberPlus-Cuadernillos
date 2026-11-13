# SP-003 · Segunda sesión · Primer lote de Sociales

Fecha: 12 de noviembre de 2026. Responsable: equipo SaberPlus / rama `trabajo/sp-003`.

**Estado: cinco candidatas originales verificadas en sus páginas; propuesta pendiente de coordinación. No cargadas en el editor y no reservadas por el coordinador.** El usuario pidió comenzar la segunda sesión; se abre el trabajo por un lote pequeño siguiendo su prompt del equipo. No se interpreta este inicio como aprobación de estas cinco preguntas concretas.

## Proyecto independiente y distribución

Editor de segunda sesión: **http://127.0.0.1:4188/**. Archivo `data/parallel/SP-003-segunda-4188/project.json`, iniciado desde `planning/starter_projects/SP-003-segunda.json`. SP-003, segunda sesión, 270 minutos, revisión 0, cero preguntas y cero contextos. Reabrir conserva lo guardado:

```powershell
uv run --offline python -B tool/editor_parallel.py --port 4188 --workspace SP-003-segunda --template planning/starter_projects/SP-003-segunda.json
```

La primera sesión permanece en 4185. Al comenzar esta tarea tenía revisión **25** y 120 preguntas; no se escribió sobre ese archivo ni se importó la plantilla encima. No reutilizar el JSON de primera como base de segunda.

| Área, en orden | Preguntas | Numeración prevista | Reparto editorial |
| --- | ---: | --- | --- |
| Sociales y ciudadanas | 25 | 1–25 | 7 pensamiento social / 10 perspectivas / 8 sistémico |
| Matemáticas | 25 | 26–50 | 8 interpretación / 11 ejecución / 6 argumentación |
| Ciencias naturales | 29 | 51–79 | 9 uso / 8 explicación / 12 indagación; componentes 9 biológico / 8 físico / 9 químico / 3 CTS |
| Inglés | 55 | 80–134 | Partes 1–7: 5/6/6/10/9/6/13 |

Son cuotas de SaberPlus. La adaptación de inglés ya entregada para **SP-001** no significa que inglés de SP-003 esté cargado ni autoriza reutilizar sus preguntas. La distribución de SP-003 conserva por ahora la matriz acordada; cualquier ajuste por bloques completos debe quedar explícito antes de la carga.

## Candidatas 1–5

Las cinco son independientes entre sí, sin lectura compartida entre preguntas y sin figuras, tablas o gráficos que haya que limpiar. Conservar sus casos, citas completas, créditos y alternativas originales. No tomar las preguntas vecinas de cada página como parte del lote.

| Puesto de Sociales / sesión | Código USB | Fuente / página física / n.º original | Tema y subtema | Clasificación propuesta y justificación |
| --- | --- | --- | --- | --- |
| 1 / 1 | `USB-91836110f48e-Q076` | F1 / 24 / 76 | Historia y modelos económicos · Colectivización agraria | PS: aplica el concepto de colectivización a la intervención del Estado en la propiedad y distribución de tierra y recursos. |
| 2 / 2 | `USB-2543b7a34fb2-Q002` | F2 / 2 / 2 | Análisis de fuentes · Pertinencia de evidencia sobre riesgo | IP: compara fuentes y reconoce que el seguimiento reciente del río y del clima es la evidencia pertinente al caso. |
| 3 / 3 | `USB-234fa4e3ddce-Q058` | F3 / 21 / 58 | Ciudadanía y diversidad · Prejuicio étnico en un discurso | IP: identifica la atribución discriminatoria de la pobreza a la ascendencia indígena entre varios fragmentos del mismo discurso. |
| 4 / 4 | `USB-524d98b0a234-Q018` | F4 / 7 / 18 | Desarrollo sostenible · Relación economía–ambiente | RS: relaciona energía limpia, empleo y prosperidad en la defensa del desarrollo sostenible formulada por el fragmento. |
| 5 / 5 | `USB-1c44481d3d4a-Q018` | F5 / 8 / 18 | Políticas públicas y territorio · Acceso rural a educación superior | RS: identifica una condición territorial necesaria para reproducir el programa, considerando el transporte de alumnos y docentes. |

PS = pensamiento social; IP = interpretación y análisis de perspectivas; RS = pensamiento reflexivo y sistémico. Lote: **1 PS / 2 IP / 2 RS**. Si se acepta sin cambios, para completar Sociales quedarían 6 PS / 8 IP / 6 RS. Afirmaciones, evidencias y niveles no asignados.

Maquetación inicial por probar después de autorizar la carga: columnas o ancho completo según altura medida; orientación de un bloque por pregunta, sin reducir la letra. No hace falta generar una imagen de los enunciados: son texto editable. El cotejo presente es de las fuentes originales; todavía no certifica páginas nuevas del cuadernillo.

Lista copiable: [cinco códigos](SP003_S2_SOCIALES_LOTE01_CODIGOS.txt). Respuestas y razones aparte: [clave editorial propuesta](SP003_S2_SOCIALES_LOTE01_CLAVE.md).

## Fuentes realmente abiertas

| Fuente | Archivo de la colección | SHA-256 |
| --- | --- | --- |
| F1 | `Referencia_2026-1-declarado_Sesion-1_ACC1_Incompleto-131-de-143_USB-91836110f48e.pdf` | `68cf407d827856af596efebb8d8b3243db2e37b4f0134ea47a5a698b144f09e7` |
| F2 | `Referencia_2026-1-declarado_Sesion-2_ABU2_USB-2543b7a34fb2.pdf` | `999a9d6313aa10e9bb26f8427c774d50fc38de700c3a55337229b5f190e98a74` |
| F3 | `2026-1-ADB3_USB-234fa4e3ddce.pdf` | `f963de729924fc065b1fea2189285ac6136397118e3565a593797a30d99a2702` |
| F4 | `2026-2-ABJ2_USB-524d98b0a234.pdf` | `78c31d57f562a19c1f7f627c6ce2e42808fd0c8383e4391e0de2b02bc632d4e0` |
| F5 | `Referencia_2026-1-declarado_Sesion-2_ABV2_USB-1c44481d3d4a.pdf` | `73f4a0c626812d201c9cf701ab19f5dc106be94d5e4311288f366d0316c6b6fd` |

Los nombres pertenecen al catálogo y no certifican autenticidad ni calendario. Rutas completas, fichas y renderizados locales: `tmp/sp003/segunda/lote01-seleccion.json` y `lote01-01.png` a `lote01-05.png`. No se modificaron los PDF.

## Cotejo y coordinación

- Se hizo `git fetch origin`. `origin/main` **a450ec9** ya es ancestro de esta rama; no hizo falta fusionarlo otra vez. Reservas SP-002 consultadas en **ecb9881**.
- Registro consultado: **241 usadas / 11 reservas**. Se excluyeron además todos los códigos publicados en las reservas SP-002/SP-003 y las **120 preguntas actuales de primera sesión**, incluidas sus 54 incorporaciones aún no integradas en el registro global. No se cambió el registro maestro.
- Las cinco existen en `output/cotejo_30/INDICE.html`. Se cruzaron equivalencias catalogadas y relacionados de las fichas; se descartaron candidatas con alertas de clave o con algún par de cotejo pendiente que tocara sus equivalencias. Estas cinco no tienen esos pares pendientes en la cola consultada.
- Se abrieron cinco páginas originales, se comprobaron sus huellas y se leyeron casos, alternativas y créditos. Las claves se razonaron desde el contenido, sin tomar las marcas de los escaneos como validación oficial.
- **Equivalencia adicional detectada al revisar el texto:** F5 Q018 reaparece como `USB-77cc8ac26d2c-Q074`, física 34, en `2026-2-ACN1_USB-77cc8ac26d2c.pdf`. Se abrió esa sexta página y se compararon caso, pregunta y cuatro alternativas, sin cambios sustantivos identificados. Se propone solo F5 Q018; excluir también Q074 de otros lotes mientras esta elección siga activa. La pareja no figuraba enlazada en el catálogo consultado; no se modificó el catálogo global.

Esto cubre lo publicado y los archivos locales disponibles, sin certificar unicidad de toda la colección ni trabajo privado de otros equipos. Publicar el lote deja trazabilidad; no equivale a una reserva confirmada ni a la aprobación de sus preguntas. La futura carga requiere la coordinación indicada por el prompt del usuario.
