# Conteo de tiendas con Spark

`tiendas_spark.py` lee la salida `tiendas_pipeline.csv` de Kestra y cuenta tiendas por ciudad usando Spark local. Ajustar la ruta de entrada del script a la ubicación de la descarga; el mismo archivo se usa para la comparación con pandas.

El resultado se guarda en `tiendas_por_ciudad/`, junto al script, con encabezado y modo overwrite. Esa carpeta es regenerable y no se versiona.

Validación del 2026-11-08: 54 filas, una partición de lectura, 22 ciudades. Quito tiene 18 tiendas y Guayaquil 8. Todos los conteos coinciden con pandas mediante una aserción; se confirmó el marcador _SUCCESS de la escritura. El cálculo coincide con el warehouse y el mart de dbt.

Esta prueba utiliza un catálogo estático pequeño, no un histórico que exceda la memoria. Spark se ejecuta con local[*] sobre una sola computadora; la comparación mediante pandas requiere que el archivo de referencia quepa en memoria.

Requisitos del entorno probado: Python 3.11 y PySpark 3.5.3, pandas 2.2.2 y Java 17. En Windows se configuraron los componentes de Hadoop en el lanzador local `ejecutar_spark.cmd`, situado en la carpeta de trabajo sesion2 (fuera del repositorio). El lanzador acepta la ruta completa de este script como argumento. Las rutas del lanzador son propias de esa instalación.


## Streaming simulado de tiendas

Decisión para el catálogo estático actual: batch. Los scripts productor_tiendas.py y consumidor_tiendas.py solo practican el transporte y conteo de eventos; no son una fuente de cambios reales de Favorita ni actualizan el warehouse.

Requieren Redpanda en localhost:9092 y kafka-python==2.0.2 (entorno probado: Python 3.11). Desde laboratorios/semana-06-sesion-02/starter, levantar el broker con `docker compose -p lab-streaming up -d`. Ejecutar primero productor_tiendas.py y después consumidor_tiendas.py con el Python del entorno .venv-dbt.

Se publicaron y consumieron cinco eventos con simulado=True. Sus asignaciones de tienda y ciudad son ficticias. Resultado observado el 2026-11-10: Quito 2, Guayaquil 2 y Cuenca 1. Estos valores cuentan mensajes, no tiendas únicas ni ventas. El consumidor usa earliest y no define group_id: al ejecutarlo de nuevo puede releer el tópico; al repetir el productor se agregan mensajes. Termina tras diez segundos de inactividad para facilitar la prueba.

Para pausar el broker sin eliminar su contenedor: `docker compose -p lab-streaming stop`; para retomarlo: `docker compose -p lab-streaming start`. El Compose de práctica no configura un volumen: `down` elimina el contenedor y se pierden los mensajes.
