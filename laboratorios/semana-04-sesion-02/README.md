# Semana 4, Sesión 2: Calidad de datos, diagnóstico y limpieza de los datos

> Objetivo de la sesión: diagnosticar problemas de calidad en el dataset de tu proyecto (duplicados, valores faltantes, inconsistencias de esquema) y justificar qué estrategia de limpieza aplica a cada uno.

**Lectura previa de esta sesión:** ["An Introduction to Data Quality"](https://medium.com/data-science/an-introduction-to-data-quality-951cc6fe0274), Hadi Fadlallah, TDS Archive / Medium, 9 de diciembre de 2018.

**Referencia de esta sesión:** *Designing Machine Learning Systems*, Cap. 3, Data Engineering Fundamentals (Chip Huyen).

## Requisitos antes de esta sesión

Confirma que tienes pandas (ya viene en el Codespace; en tu laptop, `pip install -r requirements.txt` desde la raíz del repositorio) y acceso al dataset real de tu proyecto, aunque sea en una versión parcial o de muestra.

Los laboratorios de hoy son notebooks de Jupyter (`.ipynb`), los primeros del curso: un diagnóstico es algo que lees para decidir, no algo que corre solo en el pipeline. En el Codespace, ábrelos desde el explorador de VS Code y, la primera vez, elige el kernel de Python 3.11 (sección "Notebooks y scripts" del README de la raíz del repositorio).

## Antes de empezar

A partir de la lectura previa:

**Según el artículo, ¿por qué un modelo puede entrenar sin ningún error y producir métricas razonables, aunque los datos de entrada tengan problemas serios de calidad?**

El artículo define la calidad según la utilidad de los datos en su contexto y distingue consistencia, exactitud, unicidad, completitud y oportunidad temporal. Aplicando esas ideas al entrenamiento, ejecutar sin errores no garantiza cumplir esas dimensiones: el modelo puede procesar valores incorrectos o duplicados. Esta conexión con modelos es una interpretación de la lectura, no una afirmación explícita del autor. En el laboratorio, las fechas se convertían sin error pero representaban días equivocados.

**El artículo distingue varias dimensiones de calidad de datos. ¿Cuál te parece más difícil de detectar solo con un vistazo rápido al dataset, sin código?**

Elegiría la exactitud: el artículo la relaciona con la correspondencia entre los valores almacenados y la realidad. Un monto puede tener formato correcto y aun así no coincidir con el comprobante. Detectarlo requiere contrastar la fuente o conocer el negocio. Esto también muestra el límite del diagnóstico de items.csv: no encontrar faltantes ni duplicados no prueba que todas sus categorías sean correctas.

## Pregunta de apertura

Tu modelo entrena sin ningún error, y las métricas se ven razonables. ¿Eso significa que los datos de entrada estaban bien?

No. Es necesario revisar duplicados, faltantes, tipos y formatos. En este laboratorio las fechas se interpretaban incorrectamente sin generar errores.

Las respuestas y resultados de esta entrega corresponden a los scripts `.py` ejecutados antes de la actualización del curso. Se conservan junto a los nuevos notebooks como evidencia recuperada. Trasladar las soluciones y salidas a los `.ipynb` y a `psets/proyecto/calidad/` queda pendiente.

## Ejercicio 1: diagnóstico completo de un archivo de sensores

Notebook: [`starter/ejercicio1_diagnostico.ipynb`](./starter/ejercicio1_diagnostico.ipynb), sobre [`starter/lecturas_sensores.csv`](./starter/lecturas_sensores.csv). Ya lee el archivo, muestra cada paso y guarda el resultado; faltan las líneas que hacen el diagnóstico, marcadas como `TODO 1` a `TODO 4`. Córrelo completo una vez antes de tocar nada (**Run All**).

**Respuesta 1 (TODO 1), antes de ver la solución:** sin el TODO 1, el notebook dice que quedan 10 filas. Mirando el CSV, ¿cuántas esperas que queden después de quitar las filas repetidas, y con qué método de pandas las contarías antes de quitarlas?

Quedan 8 filas después de quitar 2 duplicados completos. Se cuentan con datos.duplicated().sum() y se eliminan con datos.drop_duplicates(). Respuesta documentada después de resolver el ejercicio.

**Respuesta 2 (TODO 2 y 3):** `isna()` va a contar 1 temperatura faltante. ¿Cuántas esperas después de convertir `temperatura` a número con `errors="coerce"`, y de dónde sale la diferencia?

Quedan 2 temperaturas faltantes: el vacío de S5 y el texto N/D de S3, convertido a NaN mediante pd.to_numeric(..., errors="coerce").

**Respuesta 3 (TODO 4):** sin el TODO 4, el notebook convierte las fechas con `pd.to_datetime` sin indicar formato. ¿Qué fecha le asignó a S3 (`01/02/2026`) y a S8 (`03/02/2026`)? ¿Apareció algún error?

S3 se interpretó como 2026-01-02 y S8 como 2026-03-02, sin error. Sus fechas correctas son 2026-02-01 y 2026-02-03, respectivamente.

**Lo que confirmó la salida, TODO por TODO:**

TODO 1: 2 duplicados y 8 filas finales. TODO 2: 1 temperatura faltante visible. TODO 3: 2 faltantes después de convertir. TODO 4: todas las fechas quedaron en febrero. La conversión inicial de fechas mostró errores silenciosos.

## Durante el ConcepTest

No requerido para esta entrega, según indicación de la estudiante.

## Ejercicio 2: pedidos de una tienda

Solo o en pareja. Notebook: [`starter/ejercicio2_pedidos.ipynb`](./starter/ejercicio2_pedidos.ipynb), sobre [`starter/pedidos_tienda.csv`](./starter/pedidos_tienda.csv). Son los mismos pasos del Ejercicio 1 sobre otro archivo, más uno nuevo (TODO 5). La última celda imprime una comprobación por TODO: completa los 5 hasta que todas digan `OK`.

**Respuesta 1:** la columna `monto` usa dos marcadores distintos para un dato que no existe. ¿Cuáles son, y cuántos de ellos contó `isna()` antes de convertir?

Los marcadores son "sin dato" y "-". isna() contó 0 antes de convertir porque eran texto. Después de convertir monto a número aparecen 2 faltantes.

**Respuesta 2:** después de quitar los duplicados, el TODO 5 encuentra un `pedido_id` que todavía aparece dos veces. ¿Por qué `duplicated()` no lo marcó? ¿Qué necesitarías saber del negocio para decidir cuál de las dos filas conservar?

P07 aparece con montos 18.40 y 19.40. duplicated() compara todas las columnas y las filas son distintas. Consultaría el comprobante, el historial de correcciones y las reglas del negocio antes de decidir qué fila conservar.

**Si terminas antes:** `cantidad` también tiene faltantes, pero `dtypes` la muestra como `float64` aunque todas sus cantidades son enteras. ¿Por qué?

Los faltantes se representan como NaN y, en la lectura utilizada, la columna numérica se almacena como float64 para representarlos. Para enteros con faltantes se puede usar el tipo nullable Int64.

## Ejercicio 3: diagnóstico del dataset de tu proyecto

Copia la plantilla [`plantilla-diagnostico/diagnostico_proyecto.ipynb`](./plantilla-diagnostico/diagnostico_proyecto.ipynb) a `psets/proyecto/calidad/`. Ahí corres sobre tu propio dataset las mismas verificaciones de los Ejercicios 1 y 2 (`duplicated()`, `isna()`, `dtypes`, conversión con `errors="coerce"`, revisión manual de formatos mezclados), y documentas lo que encuentres en las celdas de texto, debajo de la verificación que lo muestra.

El resultado de hoy es el diagnóstico documentado y justificado, no todavía la limpieza completa implementada: antes de corregir hay que entender qué se está corrigiendo y por qué, como muestra el ConcepTest de esta sesión. La limpieza que decidas aquí pasa a un script de tu pipeline en la Semana 7.

### Paso 1: corre las verificaciones (10 minutos)

Reemplaza la ruta del archivo y corre las celdas de código de cada sección. En la sección de esquema, agrega las conversiones que necesiten tus columnas, adaptando el código de los Ejercicios 1 y 2.

Analicé items.csv del proyecto Corporación Favorita: 4100 filas. Revisé dtypes, duplicados completos, unicidad de item_nbr, isna(), conversión numérica con errors="coerce" y marcadores de texto. No se encontraron duplicados, IDs repetidos ni faltantes en estas comprobaciones.

### Paso 2: revisa manualmente lo que el código no captura solo (5 minutos)

Duplicados, faltantes y tipos se detectan con código; los formatos mezclados (fechas, categorías escritas de más de una forma, unidades distintas) muchas veces requieren mirar los valores distintos de una columna (`datos["columna"].unique()`) para notarlos. La celda de valores faltantes ya los muestra para cada columna de texto.

Hay 33 familias y perishable solo contiene 0 y 1. family no presenta espacios iniciales o finales; normalizar mayúsculas y espacios mantiene 33 categorías. No hay fechas. Estas verificaciones no prueban la exactitud de cada categoría frente a la fuente.

### Paso 3: documenta el diagnóstico (5 minutos)

Responde las preguntas de cada sección del notebook. Para cada problema encontrado, documenta la estrategia que aplicarías y por qué, no solo que el problema existe. Antes de hacer commit, reinicia el kernel y corre todo.

**Diagnóstico conservado y estado del traslado al notebook:**

Ver [diagnóstico del proyecto](./plantilla-diagnostico/diagnostico.md). No se justifican eliminaciones ni imputaciones con los resultados actuales. Se recomienda interpretar class como categoría y validar item_nbr al unir con ventas. El análisis utiliza el dataset original; el pipeline de Semana 4, Sesión 1 sigue pendiente.

## Antes de la próxima sesión

Ya diagnosticaste los problemas de calidad de tu dataset.

Pregunta: ¿cómo decides, con evidencia y no solo con intuición, qué variables de ese dataset ayudan a predecir lo que tu proyecto necesita predecir, y cuáles solo parecen ayudar?

Compararía un modelo base con variantes que incorporen o excluyan cada variable, usando las mismas métricas y datos de validación. En predicción de ventas usaría una separación temporal y solo información disponible al momento de predecir para evitar fuga de información. Una correlación aislada no demuestra capacidad predictiva.
