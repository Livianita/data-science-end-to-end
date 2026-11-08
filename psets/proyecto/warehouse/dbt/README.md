# Modelos de tiendas de Favorita

Flujo verificado el 2026-11-08:

`stores.csv` en el namespace de Kestra → flow `proyecto.favorita.exploracion_favorita` → `tiendas_pipeline.csv` → descarga manual → tabla `tiendas` en DuckDB → modelos dbt.

## Preparación

El flow conserva una copia del catálogo y un diagnóstico separado. Descargar `tiendas_pipeline.csv` desde Outputs. El script `laboratorios/semana-05-sesion-01/plantilla-warehouse/construir_warehouse_tiendas.py` carga ese CSV: ajustar su ruta de entrada al archivo descargado y ejecutarlo con el mismo Python del entorno `.venv-dbt` para evitar incompatibilidad de almacenamiento entre versiones de DuckDB.

El perfil usa una ruta relativa a la base del laboratorio. El archivo `.duckdb` no se versiona; se reconstruye con el script. dbt no descarga ni carga por sí solo la salida de Kestra en este proyecto.

## Ejecución

Desde esta carpeta, usar el ejecutable `dbt.exe` de `.venv-dbt/Scripts/` con estos argumentos:

```text
debug --profiles-dir .
build --profiles-dir .
```

## Modelos y validación

| Modelo | Materialización | Función |
|---|---|---|
| stg_tiendas | Vista | Selección de las cinco columnas del catálogo |
| int_tiendas_ubicacion | Vista | Renombrado de columnas para el análisis |
| marts_tiendas_por_ciudad | Tabla | Conteo de tiendas por ciudad |

Dependencias declaradas con `ref()`. Pruebas: `unique` y `not_null` sobre `stg_tiendas.store_nbr`.

Resultado observado: `dbt build` terminó con PASS=5 y ERROR=0 (tres modelos y dos pruebas). El mart contiene 22 ciudades y sus conteos suman 54 tiendas: Quito 18, Guayaquil 8, Cuenca 3 y Santo Domingo 3. Coincide con la consulta anterior en DuckDB. Las pruebas de clave no garantizan por sí solas exactitud geográfica ni calidad de otros datasets.
