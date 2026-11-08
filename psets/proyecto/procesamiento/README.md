# Conteo de tiendas con Spark

`tiendas_spark.py` lee la salida `tiendas_pipeline.csv` de Kestra y cuenta tiendas por ciudad usando Spark local. Ajustar la ruta de entrada del script a la ubicación de la descarga; el mismo archivo se usa para la comparación con pandas.

El resultado se guarda en `tiendas_por_ciudad/`, junto al script, con encabezado y modo overwrite. Esa carpeta es regenerable y no se versiona.

Validación del 2026-11-08: 54 filas, una partición de lectura, 22 ciudades. Quito tiene 18 tiendas y Guayaquil 8. Todos los conteos coinciden con pandas mediante una aserción; se confirmó el marcador _SUCCESS de la escritura. El cálculo coincide con el warehouse y el mart de dbt.

Esta prueba utiliza un catálogo estático pequeño, no un histórico que exceda la memoria. Spark se ejecuta con local[*] sobre una sola computadora; la comparación mediante pandas requiere que el archivo de referencia quepa en memoria.

Requisitos del entorno probado: Python 3.11 y PySpark 3.5.3, pandas 2.2.2 y Java 17. En Windows se configuraron los componentes de Hadoop en el lanzador local `ejecutar_spark.cmd`, situado en la carpeta de trabajo sesion2 (fuera del repositorio). El lanzador acepta la ruta completa de este script como argumento. Las rutas del lanzador son propias de esa instalación.
