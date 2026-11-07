# Semana 5, Sesión 2: Modelado analítico (analytics engineering)

> Objetivo de la sesión: construir un modelo de datos en capas (staging, intermedia, marts) con pruebas y documentación para los datos de tu proyecto.

**Lectura previa de esta sesión:** ["What is analytics engineering?"](https://www.getdbt.com/blog/what-is-analytics-engineering), dbt Labs.

**Referencia de esta sesión:** [dbt, documentación oficial](https://docs.getdbt.com/docs/introduction). Este laboratorio usa `dbt-duckdb`, el adaptador que conecta dbt al mismo warehouse de DuckDB que construiste la sesión pasada: dbt corre igual de local que DuckDB, sin ningún servicio ni cuenta adicional.

## Requisitos antes de esta sesión

1. **El warehouse de DuckDB de la Sesión 1**, con los datos de tu proyecto ya cargados (el archivo `.duckdb` del Ejercicio 3 de la sesión pasada).
2. **dbt con el adaptador de DuckDB:** ya viene en el Codespace. En tu laptop, instálalo con `pip install -r requirements.txt` desde la raíz del repositorio. Verifica con:
   ```
   dbt --version
   ```
   Deberías ver `duckdb` listado en la sección de plugins.

## Antes de empezar

A partir de la lectura previa:

**Según el artículo, ¿qué hace un analytics engineer que no hace ni un ingeniero de datos puro ni un analista puro?**

El analytics engineer transforma, prueba y documenta datos para que otras personas puedan analizarlos con definiciones confiables. Aplica prácticas de ingeniería de software, como control de versiones, al código analítico. Complementa la ingesta e infraestructura del ingeniero de datos y el análisis del analista.

**El artículo describe el flujo de trabajo de dbt (escribir SQL, dbt lo convierte en tablas o vistas). ¿Qué gana ese SQL por vivir dentro de un proyecto de dbt en vez de pegarse directo en una consola de SQL?**

Gana modelos reutilizables, dependencias declaradas con ref(), pruebas, documentación y control de versiones. dbt puede construir el grafo de modelos y ejecutarlos en el orden adecuado.

## Pregunta de apertura

Imagina un solo archivo SQL de 200 líneas: limpia los datos crudos, calcula columnas de negocio, une varias tablas y agrega el resultado final, todo en una sola consulta con subconsultas anidadas. Funciona. ¿Por qué no dejarlo así?

Una consulta monolítica dificulta aislar errores, reutilizar cálculos y probar cada etapa. Separar staging, intermedia y marts permite cambiar una responsabilidad sin copiar toda la lógica.

## Ejercicio 1: pedidos por ciudad, en tres capas

Carpeta: [`starter/ejercicio1/`](./starter/ejercicio1/), un proyecto de dbt completo sobre las mismas tablas de la Sesión 1. Ya corre de principio a fin, pero cada capa tiene un `TODO`: staging con `select *`, sin prueba sobre `stg_pedidos`, un modelo intermedio que lee las tablas crudas por su nombre, y un mart sin agregar. Córrelo una vez antes de tocar nada:

```
cd laboratorios/semana-05-sesion-02/starter/ejercicio1
python3 cargar_raw.py
dbt run --profiles-dir .
dbt test --profiles-dir .
```

**Respuesta 1 (TODO 1), antes de ver la solución:** si `stg_pedidos` solo selecciona columnas de `raw_pedidos`, sin ningún cálculo, ¿qué sentido tiene un modelo aparte en vez de consultar `raw_pedidos` directamente?

Staging define una interfaz explícita y estable sobre los datos crudos: columnas, nombres y pruebas. Evita que cada consulta de negocio tenga que interpretar por separado la fuente.

**Respuesta 2 (TODO 2):** ¿sobre qué columna de `stg_pedidos` pondrías la prueba `unique`? ¿Qué tendría que pasar en `pedidos.csv` para que falle?

Sobre id_pedido. unique fallaría si el staging devolviera más de una fila con el mismo identificador. not_null comprueba por separado que no falte ese identificador.

**Respuesta 3 (TODO 3):** mira el orden en que `dbt run` construyó los modelos. ¿Por qué `int_pedidos_con_cliente` salió primero, antes que los modelos de staging de los que depende? ¿Qué cambia con `ref()`?

Al referirse a tablas crudas por nombre, dbt no ve la dependencia de staging y puede construir primero la intermedia. ref() declara las dependencias y permite ordenar staging antes que intermedia y marts.

**Respuesta 4 (TODO 4):** si mañana cambias cómo se calcula `monto_total` en el modelo intermedio, ¿tienes que tocar también el mart?

Si se conserva el nombre y significado de la salida monto_total, el mart puede seguir sumándola sin duplicar el cálculo. Hay que reconstruirlo y verificar el resultado. Si cambia el contrato de columnas o la semántica, también se debe revisar el mart.

**Lo que confirmó la salida, TODO por TODO:**

La ejecución inicial del ejercicio 2 construyó int_ventas_con_producto, marts_monto_por_categoria y después los staging; test informó Nothing to do porque models estaba vacío. Tras corregir columnas, YAML y referencias, dbt build del ejercicio 1 construyó primero stg_clientes y stg_pedidos, luego int_pedidos_con_cliente y finalmente marts_ventas_por_ciudad. Pasaron los 4 modelos y las 6 pruebas: PASS=10, ERROR=0. El ejercicio 2 sigue pendiente.

## Durante el ConcepTest

No requerido para esta entrega, según indicación de la estudiante.

## Ejercicio 2: ventas por categoría, en tres capas

Solo o en pareja. Carpeta: [`starter/ejercicio2/`](./starter/ejercicio2/), las ventas y productos de la Sesión 1 (con una diferencia en `ventas.csv` que vas a encontrar con una prueba). Son las mismas cuatro capas del Ejercicio 1 (TODO 1 a 4), más uno nuevo (TODO 5). Después de cada cambio, corre:

```
python3 cargar_raw.py
dbt run --profiles-dir .
dbt test --profiles-dir .
python3 comprobar.py
```

`comprobar.py` imprime `OK` o `revisa` por cada TODO: complétalos hasta que todos digan `OK`.

**Respuesta 1:** ¿qué prueba falló primero, y qué fila de `ventas.csv` la hizo fallar?

Pendiente de observar: la ejecución inicial no tenía pruebas configuradas. El ejercicio está diseñado para que unique sobre id_venta detecte un duplicado una vez agregado el TODO 2; falta guardar la salida de esa prueba e identificar la fila.

**Respuesta 2 (TODO 5):** corregiste la causa en `stg_ventas`, no en `ventas.csv`. ¿Por qué ahí y no en el archivo, si el archivo es el que está mal?

La corrección en staging hace la transformación explícita, repetible y versionada; conserva el archivo crudo para auditoría. Pendiente implementar y probar el TODO 5 del ejercicio 2.

**Si terminas antes:** sin el TODO 5, ¿cuánto daba el monto de papelería en el mart, y cuánto da después? ¿Qué habría pasado con ese número si nadie hubiera escrito la prueba?

Pendiente de ejecutar el ejercicio 2 y comparar el mart antes y después de corregir el duplicado. Sin la prueba, una duplicación podría aumentar el monto sin producir un error SQL.

## Ejercicio 3: modela en capas los datos de tu propio proyecto

Usa el mismo patrón de los Ejercicios 1 y 2 (staging, intermedia, marts), aplicado a la tabla que cargaste a tu warehouse en la Sesión 1. Parte de la plantilla [`plantilla-dbt/`](./plantilla-dbt/), que trae los `TODO` marcados en cada archivo en vez del proyecto en blanco: copia la carpeta completa a `psets/proyecto/warehouse/dbt/` y trabaja ahí, al lado del `.duckdb` de la Sesión 1.

### Paso 1: staging (7 minutos)

Renombra `models/staging/stg_TODO.sql` a `stg_<tu_tabla>.sql`, selecciona las columnas de tu tabla cruda, y agrega al menos una prueba (`unique` o `not_null`) en `schema.yml` sobre la columna que identifica cada fila.

Pendiente: la plantilla de modelado del proyecto Favorita conserva TODO. Como clave candidata del catálogo se usaría item_nbr con unique y not_null, después de verificarla en los datos.

### Paso 2: intermedia y marts (13 minutos)

Renombra y completa `models/intermedia/int_TODO.sql` con una transformación o combinación de tablas de staging (usando `{{ ref(...) }}`), y `models/marts/marts_TODO.sql` con la agregación final que responda una pregunta real de tu proyecto.

Pendiente: implementar staging, una transformación intermedia y un mart del proyecto usando ref(). Una pregunta posible es el número de productos por familia; aún no se declara como modelo ejecutado.

Corre y prueba tu proyecto:

```
dbt run --profiles-dir .
dbt test --profiles-dir .
```

Pendiente de ejecutar la plantilla del proyecto; no se dispone de resultados para afirmar que sus pruebas pasaron.

## Antes de la próxima sesión

Ya tienes tus datos organizados en capas, con pruebas que fallan si algo se rompe.

Pregunta: todo lo que hiciste hasta ahora (warehouse, capas, pruebas) asume que tus datos caben enteros en la memoria de tu computadora. ¿Qué pasa el día en que el historial completo de tu proyecto ya no cabe?

Hay que revisar el motor y la estrategia de procesamiento: particiones, lectura por bloques o un motor que pueda procesar datos fuera de memoria. Spark permite repartir el trabajo; en modo local sigue limitado por los recursos de una sola computadora.
