# Semana 5, Sesión 1: Data warehouse y data lake

> Objetivo de la sesión: elegir entre un data warehouse y un data lake para los datos de tu proyecto, justificando la decisión según el tipo de dato y el patrón de consulta.

**Lectura previa de esta sesión:** ["Data Lakes vs Data Warehouses Explained"](https://www.databricks.com/blog/data-lakes-vs-data-warehouses-what-your-organization-needs-know), Databricks.

**Referencia de esta sesión:** [BigQuery, documentación oficial](https://cloud.google.com/bigquery/docs/introduction). Este laboratorio usa DuckDB como warehouse local: cumple el mismo rol conceptual que BigQuery (base de datos analítica que recibe datos estructurados y sirve consultas SQL agregadas) sin necesitar ninguna cuenta de nube ni facturación, el mismo criterio que ya usó este curso con Docker/Terraform locales (Semana 3) y con Kestra local (Semana 4).

## Requisitos antes de esta sesión

1. **Python con `pandas` ya instalado**, el mismo de sesiones pasadas.
2. **DuckDB:** ya viene en el Codespace. En tu laptop, instálalo con `pip install -r requirements.txt` desde la raíz del repositorio, que fija la misma versión del Codespace. Verifica con:
   ```
   python -c "import duckdb; print(duckdb.__version__)"
   ```
3. Ten a mano el archivo (o los archivos) que tu pipeline orquestado de la Semana 4, Sesión 1 genera para tu proyecto. Si todavía no lo has corrido desde entonces, corre tu flow de Kestra al menos una vez antes de esta sesión.

## Antes de empezar

A partir de la lectura previa:

**Según el artículo, ¿qué tipo de dato y qué patrón de consulta hacen que un equipo prefiera un data warehouse en vez de un data lake?**

Un warehouse resulta adecuado para datos estructurados e integrados, con consultas SQL recurrentes, reportes y dashboards con definiciones estables.

**¿Y qué tipo de dato y qué patrón de consulta hacen que un equipo prefiera un data lake?**

Un lake permite conservar datos crudos en distintos formatos para exploración y usos futuros, como logs e imágenes para machine learning. Requiere gobierno y controles de calidad; no basta con acumular archivos.

## Pregunta de apertura

Un equipo de finanzas necesita generar el mismo reporte de ventas todos los lunes, con columnas fijas (fecha, producto, monto), para cargarlo directo a un dashboard. Un equipo de machine learning recolecta clics, logs de la aplicación e imágenes de producto, en formatos distintos, sin saber todavía qué de todo eso va a usar en un modelo futuro. ¿Cuál de los dos necesita un data warehouse, y cuál un data lake?

Finanzas necesita principalmente un warehouse para reportes repetibles. El equipo de ML puede usar un lake para conservar formatos heterogéneos y explorar usos futuros. Ambas arquitecturas pueden complementarse.

## Ejercicio 1: un warehouse local con pedidos y clientes

Archivo: [`starter/ejercicio1_warehouse.py`](./starter/ejercicio1_warehouse.py), sobre [`starter/pedidos.csv`](./starter/pedidos.csv) (pedidos de una tienda: categoría, cantidad, precio unitario) y [`starter/clientes.csv`](./starter/clientes.csv) (ciudad y segmento de cada cliente). El script ya se conecta al warehouse, imprime cada paso y cierra la conexión; faltan 4 `TODO`. Córrelo una vez antes de tocar nada:

```
cd laboratorios/semana-05-sesion-01/starter
python3 ejercicio1_warehouse.py
```

**Respuesta 1 (TODO 1), antes de ver la solución:** sin el TODO 1, `SHOW TABLES` sale vacío y aun así el Paso 3 devuelve filas. ¿De dónde las está leyendo? ¿Qué cambia cuando `pedidos` es una tabla del warehouse?

Lee directamente pedidos.csv con read_csv_auto. CREATE TABLE AS materializa los datos en la base almacen.duckdb; las consultas pasan a usar la tabla persistida.

**Respuesta 2 (TODO 1):** con la tabla ya creada, si alguien edita `pedidos.csv`, ¿la tabla `pedidos` se actualiza sola, o hay que volver a cargarla?

No se actualiza sola. Hay que volver a cargarla; en este ejercicio CREATE OR REPLACE TABLE sustituye la tabla con el contenido actual del CSV.

**Respuesta 3 (TODO 3):** sin el TODO 3, el Paso 3 devuelve 10 filas, una por pedido. ¿Cuántas esperas después de agregar por categoría?

Tres filas: electronica, hogar y ropa. COUNT(*) cuenta pedidos y SUM(cantidad * precio_unitario) obtiene el monto de cada categoría.

**Respuesta 4 (TODO 4):** ni `pedidos` ni `clientes` responden por separado "¿cuánto se vendió por ciudad?". ¿Qué instrucción de SQL las combina, y por qué columna?

JOIN combina pedidos y clientes por id_cliente. Desde clientes se obtiene ciudad y desde pedidos se calcula el monto.

**Lo que confirmó la salida, TODO por TODO:**

10 pedidos. Electrónica: 4 pedidos y 3148.0; hogar: 3 y 153.0; ropa: 3 y 144.0. Por indicación de clase, el ejercicio 1 excluye Quito con WHERE: quedan Guayaquil 994.5 y Cuenca 126.0. Sin ese filtro, Quito suma 2324.5.

## Durante el ConcepTest

No requerido para esta entrega, según indicación de la estudiante.

## Ejercicio 2: ventas por categoría

Solo o en pareja. Archivo: [`starter/ejercicio2_ventas.py`](./starter/ejercicio2_ventas.py), sobre [`starter/ventas.csv`](./starter/ventas.csv) y [`starter/productos.csv`](./starter/productos.csv). Son los mismos pasos del Ejercicio 1, más uno nuevo (TODO 5). Al final, el script imprime una comprobación por TODO: completa los 5 hasta que todas digan `OK`.

```
python3 ejercicio2_ventas.py
```

**Respuesta 1:** en el Paso 3 aparece un `id_producto` que no está en `productos.csv`. ¿Cuál, y qué le pasa a esa venta en el `JOIN` del Paso 4?

P9 no existe en productos.csv. Su venta queda fuera del INNER JOIN; son 4 unidades en una fila de venta.

**Respuesta 2:** el monto total del Paso 4 no incluye esa venta, y la consulta no dio ningún error. ¿Cómo te darías cuenta de esto en un warehouse con millones de filas?

Compararía el total de ventas con las coincidencias del JOIN y controlaría productos sin correspondencia mediante LEFT JOIN e IS NULL. En estos datos hay 12 ventas y 11 coincidencias. La comparación de conteos requiere que la clave del catálogo sea única.

**Si terminas antes:** ¿qué tipo de `JOIN` conservaría esa venta en el resultado, y qué valor tendría su `categoria`?

LEFT JOIN desde ventas conservaría P9, con categoria y precio NULL. Por ello su monto tampoco puede calcularse sin recuperar el precio.

## Ejercicio 3: el warehouse de tu propio proyecto

Carga el archivo real que tu pipeline orquestado (Semana 4, Sesión 1) genera para tu proyecto a un warehouse de DuckDB propio, y escribe tus primeras consultas. Parte de la plantilla [`plantilla-warehouse/construir_warehouse.py`](./plantilla-warehouse/construir_warehouse.py), que trae los `TODO` marcados en vez del script en blanco: cópiala a `psets/proyecto/warehouse/` y complétala ahí.

### Paso 1: conecta y carga tu archivo (5 minutos)

Reemplaza el nombre del archivo `.duckdb`, la ruta de tu CSV (o el formato que tu proyecto genere) y el nombre de la tabla.

La primera práctica utilizó favorita.duckdb y la tabla items sobre el CSV original. Para conectar con Kestra se cargó su salida tiendas_pipeline.csv en favorita_tiendas_dbt.duckdb, tabla tiendas, mediante [construir_warehouse_tiendas.py](./plantilla-warehouse/construir_warehouse_tiendas.py). La descarga desde Outputs y la carga al warehouse son pasos manuales. Se generó esta base con el Python de .venv-dbt para que su versión de DuckDB fuera compatible con dbt.

### Paso 2: primera consulta, cuántas filas cargaste (5 minutos)

Confirma que el número de filas coincide con lo que esperabas de tu archivo de origen.

La práctica inicial cargó 4100 productos del archivo original. La carga conectada con Kestra contiene 54 tiendas, coincidentes con las 54 filas del archivo procesado por el flow; son dos datasets diferentes.

### Paso 3: una agregación que responda una pregunta real de tu proyecto (10 minutos)

Elige una columna categórica de tu dataset y agrégala con `GROUP BY`, pensando en una pregunta que de verdad te interese para tu proyecto, no una agregación arbitraria.

Consulta: SELECT family, COUNT(*) AS cantidad_productos FROM items GROUP BY family ORDER BY cantidad_productos DESC. Responde qué familias tienen más productos: GROCERY I 1334, BEVERAGES 613 y CLEANING 446, entre 33 familias. Describe el catálogo, no ventas.

Cargué la salida tiendas_pipeline.csv de Kestra en la tabla tiendas de favorita_tiendas_dbt.duckdb. Se cargaron 54 filas. La consulta agrupa por ciudad y cuenta las tiendas: hay 22 ciudades, encabezadas por Quito con 18 tiendas y Guayaquil con 8. El resultado describe la distribución del catálogo de tiendas; no mide ventas.

## Antes de la próxima sesión

Ya tienes tus datos en un warehouse y corriste tus primeras consultas.

Pregunta: si mañana necesitas ese mismo tipo de consulta pero con una columna calculada nueva, y la próxima semana alguien más del equipo necesita otra variación de la misma lógica, ¿qué pasa si cada quien la escribe como un SQL nuevo desde cero?

Se duplicaría lógica y podrían aparecer definiciones incompatibles del mismo indicador. Conviene organizar transformaciones reutilizables, versionadas, probadas y documentadas en capas, como en dbt.
