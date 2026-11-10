# Prueba de una página: SP-001

Fecha: 31 de octubre de 2026.

PDF: `output/pdf/SaberPlus_prueba_una_pagina_SP-001.pdf`.
Proyecto editable aislado: `output/pdf/SaberPlus_prueba_una_pagina_SP-001.proyecto.json`.
Clave privada: `output/pdf/SaberPlus_prueba_una_pagina_SP-001.clave.json`.

Cinco preguntas originales de demostración sobre una feria ficticia, con gráfica propia y contexto compartido. No se copió contenido del catálogo USB. Clasificaciones propuestas, sin revisión docente ni validación psicométrica. No es un simulacro completo. El pie conserva el número 3 porque es la primera página interior tras las dos páginas preliminares de la plantilla existente.

Se utilizó `editor_pdf.generate` y se extrajo únicamente la página de preguntas. Se conserva la plantilla existente: una banda de área, encabezado de rango, dos columnas con separador vertical, reglas horizontales, código SP-001, S+ discreta y leyenda BORRADOR. No se modificó `data/project.json` ni se cargó el ejemplo automáticamente en el editor.

Comprobaciones: una página, cinco preguntas completas, bloques de texto dentro de márgenes, ausencia de apéndice de respuestas, gráfico y números legibles en el PNG revisado, identidad byte a byte del proyecto guardado antes/después. Cálculos: total 200 entradas, jueves 60/200 = 30 %, ingreso 200 × 4000 = 800000, promedio 200/4 = 50 sin igualdad de registros. Claves D, C, C, B, A; solo en archivo privado, no marcadas en la página del estudiante.

Para regenerar la prueba sin cargarla en el proyecto del usuario:

```powershell
uv run --with reportlab --with pymupdf --with pillow python tool/make_one_page_demo.py
```

Para ver las preguntas del catálogo, abrir `output/cotejo_30/INDICE.html`, buscar por tema/área y pulsar **Abrir fuente, página…**. Esas fichas son documentación; la pregunta completa está en el PDF de origen y requiere que PAVEL esté conectada en E:. La copia del índice está en `E:/Icfes_SaberPlus/_SaberPlus_catalogo/cotejo_30/INDICE.html`.
