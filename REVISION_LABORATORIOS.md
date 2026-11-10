# Revisión y recuperación de laboratorios

Fecha: 2026-11-07. Alcance: Semana 3, sesión 1, hasta Semana 6, sesión 1.

El fork remoto recibió una actualización forzada. Los commits anteriores seguían disponibles localmente y se integraron con el material actualizado del curso mediante merge, sin sobrescribir el historial remoto. Se creó la rama local `respaldo-antes-recuperacion-20261107` antes de los cambios.

| Sesión | Estado y evidencia | Pendiente |
|---|---|---|
| 03-01 | Dockerfiles, scripts, resultados y respuestas recuperados; comandos de volúmenes documentados. | La estructura nueva del curso pide trasladar el proyecto a `psets/proyecto/`; la solución histórica sigue en `plantilla-dockerfile/`. No se repitieron las ejecuciones Docker en esta revisión. |
| 03-02 | Configuración de Compose y Terraform recuperada; README conserva la evidencia previa de 900000 viajes y plan sin cambios. | No se volvió a levantar ni destruir infraestructura durante esta revisión. |
| 04-01 | Actualizado el 2026-11-08: flows ejecutados en Kestra; retry y Schedule comprobados en ejercicio 1; backfill de tres lunes y cinco OK en ejercicio 2; Favorita generó un diagnóstico descargable de 54 tiendas. | Conectar la salida adecuada al warehouse. El diagnóstico generado tiene una fila por columna, no una fila por tienda o venta. |
| 04-02 | Scripts resueltos y diagnóstico de Favorita recuperados; respuestas conservadas junto con los notebooks nuevos del curso. | Trasladar soluciones y resultados a los notebooks y al directorio de proyecto requeridos por el material nuevo. |
| 05-01 | Recuperadas las soluciones de la otra carpeta de trabajo. Los dos ejercicios compartidos se ejecutaron correctamente; el ejercicio 2 muestra cinco OK. Se mantiene el filtro de clase que excluye Quito. Catálogo Favorita: 4100 registros y 33 familias, según la ejecución previa. | Usar la salida real del pipeline; hasta ahora se cargó el CSV original. Los archivos DuckDB creados con la versión local 2.0 deben abrirse con una versión compatible: no se reemplazaron al verificar. |
| 05-02 | Corregidas columnas de staging, referencias y YAML del ejercicio 1. `dbt build --profiles-dir .`: cuatro modelos y seis pruebas correctas, PASS=10 y ERROR=0. | Terminar el ejercicio 2 y los modelos del proyecto. |
| 06-01 | Ejercicio 1 de Spark resuelto y ejecutado previamente: electrónica 676.50, hogar 215.23 y ropa 214.92; escritura con `_SUCCESS`. | Completar el ejercicio 2 y el job del histórico del proyecto. |

Los ConcepTest no se requieren para esta entrega, según la indicación de la estudiante. No se inventaron votos ni discusiones en pareja.

Los archivos `.duckdb`, estados de Terraform, identificadores locales de dbt y salidas regenerables de Spark permanecen fuera de los commits. No se modificaron ni declararon resueltos los laboratorios posteriores al alcance de esta revisión.

## Avance del 2026-11-08: conexión del catálogo de tiendas

Se resolvió la conexión manual entre la salida de Kestra y DuckDB para el catálogo de tiendas. El flow ahora conserva también tiendas_pipeline.csv; el script construir_warehouse_tiendas.py carga 54 registros en favorita_tiendas_dbt.duckdb. Esta base se creó con el Python de .venv-dbt para compatibilidad con dbt.

El ejercicio 3 de Semana 5, sesión 2 quedó implementado en psets/proyecto/warehouse/dbt: staging, intermedia y mart. dbt build pasó tres modelos y dos pruebas (PASS=5, ERROR=0). El mart contiene 22 ciudades y 54 tiendas, coincidentes con DuckDB. Queda pendiente el ejercicio 2 compartido de esa sesión; no se confunde con este proyecto terminado. La descarga del CSV y su carga al warehouse todavía son manuales.

## Cierre del ejercicio 2 de dbt (2026-11-08)

Se completo el pendiente de ventas por categoria: id_venta=4 estaba duplicado de forma exacta; SELECT DISTINCT en staging conserva el origen crudo y devuelve 12 ventas. Papeleria paso de 122.0 a 109.5. dbt build: PASS=8, ERROR=0 (cuatro modelos y cuatro pruebas). comprobar.py: cinco TODO en OK. Este resultado reemplaza el estado pendiente de ese ejercicio en las filas historicas anteriores.

## Streaming verificado (2026-11-10)

Semana 6, sesión 2: ejercicio 1 con diez pedidos y conteo hogar 4, ropa 3 y electronica 3; ejercicio 2 con ocho lecturas, dos alertas de techo (31.5 y 33.0) y todas las comprobaciones OK. El ejercicio 3 publicó y consumió cinco actualizaciones ficticias de tiendas: Quito 2, Guayaquil 2 y Cuenca 1. Se documentó batch como decisión para el catálogo estático y streaming como simulación. No se ejecutó la prueba opcional con dos consumidores.
