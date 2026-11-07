# Semana 6, Sesión 1: Procesamiento por lotes de datos históricos

> Objetivo de la sesión: procesar los datos históricos de tu proyecto, que no caben en memoria, mediante un job de procesamiento distribuido por lotes.

**Lectura previa de esta sesión:** ["Batch and Streaming in the World of Data Science and Data Engineering"](https://medium.com/capital-one-tech/batch-and-streaming-in-the-world-of-data-science-and-data-engineering-2cc029cdf554), Capital One Tech.

**Referencia de esta sesión:** [Data Engineering Zoomcamp, módulo de batch processing (DataTalksClub)](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/06-batch). Este laboratorio usa Spark en modo local (`local[*]`), sobre los núcleos de tu propia máquina (tu Codespace o tu laptop), sin ningún clúster real: el mismo criterio que ya usó este curso con Docker/Terraform locales (Semana 3), Kestra local (Semana 4) y DuckDB local (Semana 5).

## Requisitos antes de esta sesión

1. **Java 17 y PySpark 3.5.3.** En el Codespace ya vienen instalados. En tu laptop, instala OpenJDK 17 (en Mac, con Homebrew: `brew install openjdk@17`) y después corre `pip install -r requirements.txt` desde la raíz del repositorio, que fija PySpark en la versión 3.5.3 (compatible con Java 8/11/17; la rama 4.x de PySpark exige Java 17 o superior). Verifica con:
   ```
   java -version
   python3 -c "import pyspark; print(pyspark.__version__)"
   ```
2. Ten a mano el archivo histórico real que tu pipeline orquestado de la Semana 4 genera para tu proyecto, y al menos una transformación de pandas que ya escribiste sobre ese archivo en una sesión anterior (Semana 4, Sesión 2, o Semana 5).

**Si ves un error de red al arrancar Spark (`UnknownHostException`) que no te deja ver la salida del programa:** corre el script con la variable de ambiente `SPARK_LOCAL_IP=127.0.0.1` antes del comando, por ejemplo `SPARK_LOCAL_IP=127.0.0.1 python3 mi_job.py`. No es un error de tu código. En el Codespace esta variable ya viene configurada, así que ahí no deberías verlo.

## Antes de empezar

A partir de la lectura previa:

**Según el artículo, ¿qué distingue a un job de procesamiento por lotes (batch) de un job de procesamiento en tiempo real (streaming)?**

Batch procesa conjuntos acumulados en ejecuciones delimitadas. Streaming procesa datos conforme llegan, con menor latencia. La lectura distingue además usar un modelo para predecir de actualizarlo: predicción en streaming no implica aprendizaje online.

**El artículo describe el procesamiento distribuido como una forma de repartir el trabajo entre varias máquinas o núcleos. ¿Qué problema resuelve repartir el trabajo, que un solo proceso de pandas no resuelve?**

Repartir datos y tareas permite aprovechar varios núcleos o máquinas y no exigir que un único proceso contenga todo el dataset. En este laboratorio local[*] usa la propia máquina: no demuestra ejecución en un clúster ni elimina todos los límites de memoria.

## Pregunta de apertura

Tu pipeline de la Semana 4 lleva semanas acumulando el histórico de tu proyecto. Un día ese archivo pesa más que la memoria RAM de tu laptop. ¿Qué le pasa exactamente a un script de pandas que intenta leerlo con `pd.read_csv()`, y por qué?

pd.read_csv() intenta construir el DataFrame completo en memoria por defecto, con memoria adicional para el parseo. Si no hay RAM suficiente, puede paginar intensamente, lanzar MemoryError o ser terminado por el sistema. Leer por chunks es una alternativa cuando el cálculo lo permite.

## Ejercicio 1: ventas por categoría, con Spark

Archivo: [`starter/ejercicio1_spark.py`](./starter/ejercicio1_spark.py), sobre [`starter/ventas.csv`](./starter/ventas.csv): la misma pregunta de la Semana 5 (monto total por categoría), ahora con la API de DataFrames de Spark. El script ya arranca Spark, lee el archivo e imprime cada paso; faltan 4 `TODO`. Córrelo una vez antes de tocar nada:

```
cd laboratorios/semana-06-sesion-01/starter
python3 ejercicio1_spark.py
```

**Respuesta 1 (TODO 1), antes de ver la solución:** con el filtro escrito, `spark.read.csv(...)` y `.filter(...)` todavía no ejecutan nada. ¿En qué línea del script se lee de verdad el archivo?

Para ejecutar el filtro, count() es la primera acción posterior que evalúa ese plan. Matiz: con inferSchema=True, spark.read.csv también puede recorrer datos para inferir tipos; por eso no es exacto afirmar que la lectura inicial nunca hace trabajo.

**Respuesta 2 (TODO 2 y 3):** ¿qué método de la API de Spark esperas que sea el equivalente del `GROUP BY` de SQL que usaste con DuckDB? ¿Cuántas filas tendrá `resumen`?

groupBy("categoria").agg(...) es el equivalente de la agregación SQL. resumen tiene 3 filas, una por categoría, usando todas las ventas de con_monto.

**Respuesta 3 (TODO 4):** cuando `resumen.write.csv(...)` corre, ¿esperas un solo archivo `.csv`, como `df.to_csv()` de pandas, o algo distinto?

Una carpeta con uno o varios archivos part-*.csv y un marcador _SUCCESS. El número de archivos depende de las particiones de salida; no se debe asumir un único CSV.

**Lo que confirmó la salida, TODO por TODO:**

Filtro: 3 ventas de electrónica. Agregación: electronica 3 y 676.5; hogar 5 y 215.23000000000002; ropa 4 y 214.92000000000002. Spark guardó resumen_por_categoria con part-*.csv, _SUCCESS y archivos CRC en Windows. Se configuraron componentes locales de Hadoop para resolver la escritura.

## Durante el ConcepTest

No requerido para esta entrega, según indicación de la estudiante.

## Ejercicio 2: costo de envíos por ciudad

Solo o en pareja. Archivo: [`starter/ejercicio2_envios.py`](./starter/ejercicio2_envios.py), sobre [`starter/envios.csv`](./starter/envios.csv). Son los mismos pasos del Ejercicio 1 sobre otro archivo, más uno nuevo (TODO 5): calcular el mismo total con pandas para confirmar el resultado de Spark. Al final, el script imprime una comprobación por TODO: completa los 5 hasta que todas digan `OK`.

```
python3 ejercicio2_envios.py
```

**Respuesta 1:** ¿qué ciudad tiene el costo total más alto, y cuántos envíos quedaron fuera por no estar entregados?

Pendiente ejecutar el ejercicio 2 de envíos. No se registra una ciudad ganadora ni un conteo observado hasta completar y comprobar el script.

**Respuesta 2:** en el TODO 5, pandas leyó el archivo completo en memoria. ¿Por qué tiene sentido verificar contra pandas en este archivo, y por qué no lo harías con el histórico de la pregunta de apertura, el que ya no cabe en la RAM de tu laptop?

El archivo pequeño permite comparar dos implementaciones de la misma transformación. Leer un histórico que no cabe en RAM con pandas completo repetiría el problema original; se necesita una muestra controlada o una verificación por bloques.

**Si terminas antes:** en el Ejercicio 1, `monto_total` de hogar salió `215.23000000000002`. ¿Es un error de Spark? ¿Lo verías también con pandas?

No es un error exclusivo de Spark: double usa punto flotante binario y algunos decimales no son exactos. También puede ocurrir con pandas. Para montos financieros se debe decidir una representación decimal y reglas de redondeo apropiadas.

## Ejercicio 3: reescribe una transformación de tu proyecto como job de Spark

Elige una transformación de pandas que ya escribiste sobre el archivo histórico de tu propio proyecto (una columna calculada, una agregación por categoría), y reescríbela con la API de DataFrames de Spark. Parte de la plantilla [`plantilla-spark/construir_job_spark.py`](./plantilla-spark/construir_job_spark.py), que trae los `TODO` marcados en vez del script en blanco: cópiala a `psets/proyecto/procesamiento/job_spark.py` y complétala ahí.

### Paso 1: lee tu archivo con Spark (5 minutos)

Reemplaza la ruta del archivo histórico real de tu proyecto.

Pendiente: la plantilla del proyecto conserva TODO y aún no se ha cargado allí un histórico real generado por el pipeline.

### Paso 2: reescribe tu transformación (10 minutos)

Con `withColumn()` para la columna calculada y `groupBy().agg()` para la agregación, reproduce exactamente el mismo cálculo que ya hacías con pandas.

Pendiente: escoger y portar una transformación del proyecto. La agregación del catálogo por family ya se conoce de DuckDB, pero no se presenta como un histórico procesado con Spark.

### Paso 3: corre el job y compara contra pandas (5 minutos)

Confirma que el resultado de Spark coincide con el resultado que ya conocías de pandas.

Pendiente: ejecutar el job del proyecto y comparar los resultados con una referencia equivalente. El ejercicio 1 compartido sí quedó ejecutado y guardado.

## Antes de la próxima sesión

Ya reescribiste una transformación de tu proyecto para que corra en particiones, sobre un histórico ya acumulado.

Pregunta: hoy procesaste un histórico ya acumulado, de una sola vez. ¿Qué pasa si tu proyecto necesita reaccionar a cada dato nuevo apenas llega, sin esperar a que se acumule un lote?

Se necesita un flujo de procesamiento continuo o por micro-lotes con latencia adecuada, además de controlar estado, duplicados y recuperación. No bastaría con esperar al próximo lote histórico programado.
