# Ecuaciones y composición editorial

## Estado y preservación

Implementación local del 10 de noviembre de 2026. No migra, reemplaza ni completa automáticamente preguntas. Las fórmulas se guardan como texto editable en los mismos campos del JSON; los proyectos anteriores siguen siendo válidos. Los nuevos controles son opcionales. Ni el orden ni las distribuciones guardadas se cambian al abrir el editor.

## Iniciar

Desde la raíz: `uv sync` y `uv run --offline python -B tool/editor_server.py`. `pyproject.toml` y `uv.lock` fijan el entorno, incluido Matplotlib y ReportLab. No requiere LaTeX instalado, Node para renderizar fórmulas, CDN, una cuenta externa ni subir contenido. El servidor de prueba 4186 debe seguir apuntando a su JSON existente, no al ejemplo inicial.

## Escribir fórmulas

Coloca el cursor en una introducción, enunciado, opción, lectura o explicación y abre **Insertar ecuación matemática**. Los botones insertan plantillas editables en la selección actual y activan la vista previa normal. También se puede escribir directamente:

```text
Raíz: \(\sqrt{x^2+1}\)
Raíz cúbica: \(\sqrt[3]{8}\)
Fracción: \(\frac{a+b}{c}\)
Potencia: \(x^{n+1}\)
Subíndice: \(a_{n+1}\)
Sucesión: \(a_n=a_1r^{n-1}\)
Sumatoria: \(\sum_{k=1}^{n}k\)
Símbolos: \(\alpha\leq\beta\neq\pi\)
En línea separada: \[\frac{-b+\sqrt{b^2-4ac}}{2a}\]
```

Se usa el subconjunto Mathtext de TeX matemático, no un documento LaTeX completo: no admite `\begin{document}`, carga de archivos, HTML ejecutable, comandos de shell o paquetes externos. Los precios con `$` no se interpretan como fórmulas. Se conservan las opciones antiguas con superíndices Unicode. No se convierten automáticamente textos o respuestas anteriores.

Las fórmulas se dibujan con contornos vectoriales STIX al tamaño tipográfico del párrafo (normalmente 10 puntos). Su altura y profundidad se reservan en la composición; las líneas se ajustan antes de dibujarse. Se emplea el mismo motor para la vista previa PNG, el PDF del estudiante, el resuelto y sus explicaciones. El pequeño recurso transparente interno solo reserva espacio: la fórmula visible es vectorial. **Limitación:** esos contornos no son texto matemático seleccionable ni MathML accesible en el PDF; el código fuente permanece en el JSON. El motor no es un CAS ni comprueba si una ecuación es correcta matemáticamente.

Una fórmula indivisible más ancha que su columna produce un error claro; no se recorta ni se reduce la fuente silenciosamente. Se debe dividir la expresión en varias fórmulas o escoger ancho completo. Hay límites de 600 caracteres por fórmula, 40 fórmulas por párrafo y caché de 256 resultados. Los errores de sintaxis no borran el formulario ni declaran éxito. Guardar un borrador no garantiza que todas sus fórmulas sean exportables; la vista previa/exportación las compone y valida.

## Controlar la distribución sin automatismos

- **Distribución de pregunta:** columnas o ancho completo, independientemente de sus opciones.
- **Distribución de opciones:** vertical (valor heredado) o cuadrícula de dos columnas: A/B arriba, C/D abajo. Se conserva el orden de letras, las imágenes, los textos y la clave; el resaltado del resuelto usa los límites reales de cada celda.
- **Ancho/altura máximos de imagen:** puntos PDF (72 puntos = 1 pulgada). Se conserva la proporción y se limita al ancho disponible. Vacío conserva el valor predeterminado, no significa cero ni borra la imagen. La cuadrícula dimensiona las imágenes según el ancho de cada celda.
- **Página nueva:** salto antes de la pregunta, sin reordenar ni dividir su contenido.
- **Columna derecha:** solo para preguntas en columnas. Permite ubicar un bloque en el lado derecho antes de continuar con uno de ancho completo. Si ya se consumió esa columna, abre una nueva página; es una elección editorial explícita. Desmarcar antes de cambiar a ancho completo.

Las preguntas largas siguen siendo bloques indivisibles. No existe partición automática segura de un procedimiento o texto entre páginas; si no cabe en ninguna distribución, hay que crear un contexto compartido o dividir editorialmente el contenido sin alterar su sentido. No hay equilibrio automático de columnas ni garantía de tres preguntas por página. Una pregunta grande debe ocupar el espacio necesario, no encogerse por una cuota visual.

## Referencia inspeccionada

### Flujo mixto optativo

El selector **Flujo de columnas** permite activar `column_flow: "balanced"`. Agrupa preguntas consecutivas en dos columnas medidas, de izquierda a derecha, con una sola línea horizontal de cierre y un separador vertical hasta esa misma altura. Un bloque ancho puede preceder o seguir a las columnas en la misma página si cabe. No adelanta preguntas, no modifica el tamaño de letra y no divide preguntas. Los proyectos sin este campo conservan el modo secuencial anterior. La afirmación anterior sobre ausencia de equilibrio automático corresponde a ese modo heredado.

Los contextos compartidos, Inglés y los saltos manuales mantienen su tratamiento anterior, fuera del equilibrado. Una pregunta ancha posterior puede dejar espacio libre si no cabe; no se rellena cambiando el orden. Tampoco se garantiza que una pregunta muy alta quepa en una columna.

Muestra autorizada: `tool/verify_mixed_booklet.py` crea una copia JSON, un registro de cambios de anchura, los PDF y renders en `tmp/pdfs/flujo-mixto/`. Conserva IDs, contenido, imágenes, claves, exclusiones y orden del JSON corregido; comprueba los hashes de ese original y del proyecto del servicio. No importa ni guarda nada en el editor.

Se localizó `USB-1c6462bf5377-Q021` en el catálogo, PDF `2025-2-AAR1_USB-1c6462bf5377.pdf`, páginas físicas 2 y 11. Se inspeccionaron sus renders; no todo el documento. La página 11 contiene la pregunta de temperatura con cuatro gráficas A/B/C/D en una cuadrícula 2×2, seguida de otra pregunta. La página 2 mezcla preguntas de longitudes diferentes, un procedimiento y una figura con tabla. Conclusión editorial: ajustar los bloques al contenido, conservar las secuencias de pasos y mantener las alternativas gráficas juntas. No copiar marca, adornos oficiales ni una cantidad fija de preguntas por página. Autenticidad y permisos no se deducen del nombre del archivo.

Para revisar el cuadernillo actual completo, pedir al usuario su PDF más reciente; los problemas de distribución concretos deben evaluarse en ese archivo y no extrapolarse del ejemplo. No aplicar cambios masivos al JSON que el usuario está organizando.

## Verificación y muestra aislada

Regresión corregida durante la revisión del cuadernillo real: fórmula y espacio reservado se dibujan como un único objeto en línea. No se emplea un callback anterior de ancho cero, que podía quedarse en la línea anterior cuando la fórmula saltaba. La prueba comprueba los límites reales del dibujo, no solo las cajas de texto. La exportación también rechaza claves vacías o de varias letras; guardar borradores incompletos sigue permitido.

Pruebas: `uv run --offline python -B -m unittest discover -s tool -p 'test_editor*.py' -v` y `node tool/test_editor_live.mjs`. Cubren compatibilidad de datos, geometría, comandos inválidos, ancho de columna, plantillas, cuadrícula y seguimiento de la clave. No equivalen a prueba interactiva en navegador.

Con autorización previa: `uv run --offline python -B tool/make_math_layout_demo.py`. Genera datos técnicos de ejemplo únicamente en `tmp/pdfs/ecuaciones-maquetacion/`, con los tres PDF, guía auxiliar, PNG y dos renders de la referencia de USB. No se incorporan esas preguntas de demostración al proyecto ni al banco. Los originales y el proyecto guardado no se modifican.
