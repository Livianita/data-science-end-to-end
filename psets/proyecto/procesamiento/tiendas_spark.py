from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# TODO: reemplaza "mi-job-spark" por un nombre propio de tu proyecto.
spark = (
    SparkSession.builder
    .appName("favorita-tiendas-por-ciudad")
    .master("local[*]")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

# TODO: reemplaza por la ruta real del archivo historico de tu proyecto
# (el mismo que tu pipeline orquestado de la Semana 4 genera o acumula).
historico = spark.read.csv(
    "C:/Users/lroja/Downloads/2KYdQok7ZT8eMLkv5SJbhk-tiendas_pipeline.csv",
    header=True,
    inferSchema=True
)
print(f"Particiones de lectura: {historico.rdd.getNumPartitions()}")
print(f"Filas leidas: {historico.count()}")

# TODO: reescribe aqui, con la API de Spark, la misma transformacion de pandas
# que ya usaste en una sesion anterior (por ejemplo, una columna calculada con
# withColumn y una agregacion con groupBy().agg()).
resultado = (
    historico
    .groupBy("city")
    .agg(F.count("*").alias("numero_tiendas"))
    .withColumnRenamed("city", "ciudad")
    .orderBy(F.desc("numero_tiendas"), F.asc("ciudad"))
)

resultado.show(30, truncate=False)

# TODO: guarda el resultado como salida del job.
from pathlib import Path

ruta_salida = Path(__file__).resolve().parent / "tiendas_por_ciudad"

resultado.write.mode("overwrite").csv(
    str(ruta_salida),
    header=True
)

import pandas as pd

datos_pandas = pd.read_csv(
    "C:/Users/lroja/Downloads/2KYdQok7ZT8eMLkv5SJbhk-tiendas_pipeline.csv"
)

conteos_pandas = datos_pandas.groupby("city").size().to_dict()

conteos_spark = {
    fila["ciudad"]: fila["numero_tiendas"]
    for fila in resultado.collect()
}

assert conteos_spark == conteos_pandas, "Los conteos no coinciden"

print(
    f"Comparacion OK: {len(conteos_spark)} ciudades, "
    f"{sum(conteos_spark.values())} tiendas"
)
spark.stop()
