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
