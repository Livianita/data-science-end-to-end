# Semana 4, Sesión 1: Orquestación del pipeline de ingesta

> Objetivo de la sesión: convertir el script de ingesta de tu proyecto, que hasta ahora ejecutas a mano, en un pipeline programado con reintentos y backfill.

**Lectura previa de esta sesión:** ["Data Pipeline Orchestration"](https://towardsdatascience.com/data-pipeline-orchestration-9887e1b5eb7a/), Towards Data Science.

**Referencia de esta sesión:** [Data Engineering Zoomcamp, Módulo 2 (DataTalksClub)](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/02-workflow-orchestration/README.md). Este curso usa Kestra, el mismo orquestador que enseña la edición vigente de ese módulo.

## Requisitos antes de esta sesión

1. **Docker**, el mismo de las sesiones pasadas. Si trabajas en el Codespace, ábrelo para esta sesión con una máquina de 4 núcleos ("Change machine type"): Kestra y su Postgres necesitan más memoria que los laboratorios anteriores.
2. Levanta Kestra localmente antes de la sesión, con el `docker-compose.yml` de [`starter/docker-compose.yml`](./starter/docker-compose.yml):
   ```
   docker compose up -d
   ```
   Abre `localhost:8080` en el navegador (en el Codespace, desde la pestaña **Ports** de VS Code, puerto 8080): deberías ver la pantalla de inicio de sesión de Kestra. Entra con el usuario `admin@kestra.io` y la contraseña `Admin1234`, definidos en el mismo `docker-compose.yml`. Si es la primera vez que arranca, puede tardar 20-30 segundos en quedar lista.

Este `docker-compose.yml` es una versión simplificada del oficial de Kestra: quita el `healthcheck` de Postgres (fuera del vocabulario de Docker Compose de este curso) porque el reintento de conexión, igual que en la Sesión 2 de la semana pasada, se resuelve del lado de cada flow, no de Docker.

## Antes de empezar

A partir de la lectura previa:

**Según el artículo, ¿qué diferencia hay entre encadenar scripts con un cron job y usar una herramienta de orquestación?**

Un cron programa un comando. La orquestación centraliza las etapas, dependencias y seguimiento del pipeline. La lectura destaca visibilidad, documentación y control de versiones. Aplicado al ejercicio, Kestra permite revisar tareas y reintentar fallos sin reconstruir manualmente toda la secuencia.

**¿Por qué un cron job, que solo dispara un comando a una hora fija, no resuelve por sí solo el problema de un pipeline que falla a mitad de camino?**

Disparar un comando no registra por sí solo qué etapa debe recuperarse ni define reintentos, dependencias o backfill. Eso requiere lógica adicional o un orquestador.

## Pregunta de apertura

Tu script de ingesta corre perfecto cuando tú lo ejecutas a las 10 de la mañana, mirando la pantalla. Si tiene que correr todos los días a las 3 de la madrugada, sin que nadie esté despierto para revisarlo, ¿qué cosas pueden salir mal que hoy nunca has visto fallar?

Pueden fallar la red, la fuente, las credenciales, la disponibilidad de archivos o el almacenamiento. Necesito logs, alertas y reintentos, además de evitar duplicados al repetir una carga.

## Ejercicio 1: la ingesta diaria de una fuente inestable

Carpeta: [`starter/ejercicio1/`](./starter/ejercicio1/). [`ingesta_inestable.py`](./starter/ejercicio1/ingesta_inestable.py) simula una fuente de datos que falla la mitad de las veces. [`flow_ingesta.yml`](./starter/ejercicio1/flow_ingesta.yml) ya lo corre dentro de Kestra, con una imagen `python:3.11-slim` y el script subido como archivo del namespace (`namespaceFiles`), pero tiene tres `TODO`. Súbelo y ejecútalo antes de tocar nada:

```
cd laboratorios/semana-04-sesion-01/starter/ejercicio1
bash ../subir_a_kestra.sh flow_ingesta.yml ingesta_inestable.py
```

Después, en Kestra (`localhost:8080`, sección Flows), abre `proyecto.ingesta` → `ingesta_diaria` y presiona "Execute" tres veces.

**Respuesta 1, antes de ver la solución:** después de presionar "Execute" tres veces, ¿tienes un flow o tres? ¿Una ejecución o tres? ¿Cuántas esperas que fallen?

Es un flow con tres ejecuciones. Con probabilidad de fallo 0.5, el número esperado de fallos es 1.5; en tres ejecuciones concretas pueden fallar de cero a tres. En la prueba inicial se realizaron cinco ejecuciones de proyecto.ingesta: tres fallidas y dos exitosas. Los logs confirmaron el mensaje de error de conexión simulado.

**Respuesta 2 (TODO 1):** ¿qué le agregarías al flow para que una falla de la fuente no dependa de que alguien lo vuelva a correr a mano?

Un retry de tipo constant, con maxAttempts: 3 e interval: PT10S, como pide el TODO. Debe aplicarse a la tarea que puede fallar; no garantiza éxito si la fuente sigue caída.

**Respuesta 3 (TODO 3):** con el trigger agregado, si la ejecución de una noche agota sus reintentos y falla, ¿la ejecución programada de la noche siguiente también falla, o corre normal?

La siguiente ejecución programada es independiente y vuelve a intentar normalmente. Si la causa persiste puede fallar también, pero no por heredar automáticamente el estado fallido anterior.

**Lo que confirmó la ejecución, TODO por TODO:**

Se observó una ejecución que falló y tuvo éxito en el segundo intento, con unos 10 segundos entre intentos, y otra que agotó los tres intentos. La fecha impresa permaneció igual durante los reintentos. Para probar el Schedule se cambió temporalmente el cron a `35 19 * * *`: el 7 de noviembre de 2026 se procesó `2026-11-07T19:35:00-05:00` y el comando terminó con código 0. El archivo local quedó nuevamente con `0 6 * * *`, zona America/Guayaquil; cualquier cambio local debe actualizarse también en Kestra. El backfill se verificó en el ejercicio 2.

## Durante el ConcepTest

No requerido para esta entrega, según indicación de la estudiante.

## Ejercicio 2: la ingesta semanal de una estación de clima

Solo o en pareja. Carpeta: [`starter/ejercicio2/`](./starter/ejercicio2/). [`ingesta_clima.py`](./starter/ejercicio2/ingesta_clima.py) falla 3 de cada 10 veces y recibe como argumento la fecha que está registrando. Completa los TODO 1 a 4 de [`flow_clima.yml`](./starter/ejercicio2/flow_clima.yml) con el mismo patrón del Ejercicio 1, súbelo y ejecútalo:

```
cd laboratorios/semana-04-sesion-01/starter/ejercicio2
bash ../subir_a_kestra.sh flow_clima.yml ingesta_clima.py
```

**TODO 5:** recupera los tres últimos lunes con un backfill. En Kestra, abre el flow, ve a la pestaña **Triggers** y usa la opción de backfill del trigger de los lunes, con un rango de fechas que cubra los tres lunes anteriores a hoy.

`comprobar.py` lee el flow tal como quedó en Kestra y las ejecuciones del backfill:

```
python3 comprobar.py
```

**Respuesta 1:** en los logs de una ejecución del backfill, ¿qué fecha recibió `ingesta_clima.py`: la de hoy, o la del lunes que se estaba recuperando? ¿Qué pasaría si el script usara la fecha de hoy?

Los logs mostraron las fechas históricas `2026-10-19T07:00:00-05:00`, `2026-10-26T07:00:00-05:00` y `2026-11-02T07:00:00-05:00`, aunque las ejecuciones ocurrieron el 7 de noviembre. Usar la fecha actual produciría registros con una fecha equivocada y no reconstruiría el histórico. El backfill cubrió del 19 de octubre al 3 de noviembre de 2026; `comprobar.py` devolvió OK en los cinco TODO.

**Respuesta 2:** ¿alguna ejecución del backfill necesitó más de un intento? ¿Dónde lo ves en Kestra?

En la captura compartida del backfill aparecen tres registros exitosos y no se muestran fallos. Esto no demuestra por sí solo el número de intentos de cada tarea: se consulta en el detalle de la ejecución y sus logs. En el ejercicio 1 sí se observó explícitamente un intento fallido seguido de uno exitoso.

**Si terminas antes:** si la estación estuvo caída dos semanas seguidas, ¿subirías `maxAttempts` a 50, o harías un backfill cuando vuelva? ¿Qué problema resuelve cada uno?

Usaría reintentos acotados para fallos transitorios y backfill al recuperar la fuente tras dos semanas. Cincuenta intentos no sustituyen la reconstrucción de los periodos omitidos.

## Ejercicio 3: el flow de tu propio proyecto

Usa el mismo patrón de los Ejercicios 1 y 2, aplicado a la ingesta de tu proyecto. En vez de `python:3.11-slim` y un archivo del namespace, el flow corre la imagen de Docker que construiste en la Semana 3, Sesión 1: ahí ya están tu script y sus dependencias. Parte de la plantilla [`plantilla-flow/flow_proyecto.yml`](./plantilla-flow/flow_proyecto.yml): cópiala a `psets/proyecto/orquestacion/` y complétala ahí.

### Paso 1: el task que corre tu imagen (5 minutos)

Confirma con `docker images` que la imagen de tu proyecto existe en tu máquina (si no, vuelve a construirla con `docker build -t <nombre>:<tag> .`). Completa `id`, `namespace`, `containerImage` con el nombre y el tag de tu imagen, y el comando que corre tu script con la ruta completa de su `WORKDIR` (por ejemplo, `python /app/ingesta.py`): Kestra corre los comandos en su propia carpeta de trabajo, no en la de tu imagen. `pullPolicy: NEVER` le dice a Kestra que use la imagen local en vez de buscarla en Docker Hub.

Flow `exploracion_favorita`, namespace `proyecto.favorita`, tarea `explorar_tiendas`, imagen local `cfavorita-exploracion:latest` y pullPolicy NEVER. El comando es `python /app/explorar_tiendas.py --entrada stores.csv --salida diagnostico_tiendas.csv`. El CSV original se subió como archivo del namespace y `outputFiles` conserva el diagnóstico. La copia para el proyecto está en [psets/proyecto/orquestacion/flow_proyecto.yml](../../psets/proyecto/orquestacion/flow_proyecto.yml).

### Paso 2: decide el retry (5 minutos)

Piensa en tu fuente de datos: ¿es una API externa que a veces no responde? ¿un archivo que a veces todavía no está listo? Decide `maxAttempts` e `interval` según qué tan probable y qué tan larga es esa falla, y descomenta el bloque `retry`.

Se configuró retry constant con maxAttempts 2 e interval PT10S para fallos transitorios de ejecución. Si falta el CSV estático o hay una ruta incorrecta, hay que corregir la causa: repetir no lo resuelve. No se forzó un fallo en el flow de Favorita para probar sus reintentos.

### Paso 3: agrega el trigger Schedule (6 minutos)

Descomenta el bloque `triggers` y elige una expresión cron con la frecuencia que tenga sentido para tu proyecto. No todos los proyectos necesitan correr todos los días.

Se configuró `0 8 * * 1`, los lunes a las 08:00 en America/Guayaquil, como práctica semanal del laboratorio. Al ser stores.csv estático, cada ejecución analiza el mismo archivo hasta que se actualice el archivo del namespace. La programación está configurada; no se declara observada una ejecución automática semanal de Favorita.

Súbelo desde la raíz de tu fork con `bash laboratorios/semana-04-sesion-01/starter/subir_a_kestra.sh psets/proyecto/orquestacion/flow_proyecto.yml` (sin scripts: ya están en la imagen) y ejecútalo manualmente al menos una vez para confirmar que corre sin errores.

Kestra aceptó la revisión 2 y la estudiante confirmó el resultado correcto. La ejecución mostró 54 filas y 5 columnas: store_nbr, city, state, type y cluster, sin faltantes; sus valores distintos fueron 54, 22, 16, 5 y 17, respectivamente. Se generó y descargó diagnostico_tiendas.csv desde Outputs. Esta salida resume calidad por columna: no es una tabla de tiendas ni una ingesta de ventas. La conexión posterior con el warehouse sigue pendiente y debe respetar ese esquema.

## Al terminar

Apaga Kestra desde `starter/`, para que no siga ocupando memoria mientras trabajas en otra cosa:

```
docker compose down
```

Sin `-v`: los volúmenes `datos_postgres` y `datos_kestra` se conservan, y con ellos tus flows y su historial de ejecuciones. El laboratorio integrador de la Semana 7 parte de tu flow; la próxima vez que corras `docker compose up -d` ahí sigue. Mientras Kestra esté apagado, el `Schedule` de tu flow no dispara: en una empresa, el orquestador corre en un servidor que no se apaga.

## Antes de la próxima sesión

Ya tienes tu pipeline de ingesta corriendo solo, todos los días o con la frecuencia que decidiste.

Pregunta: ¿cómo sabes si los datos que trajo son datos buenos, o datos con problemas que ningún error de ejecución te va a avisar?

Aplicaría controles de duplicados, faltantes, tipos, rangos, formatos e integridad entre tablas. Que una ejecución termine bien solo demuestra que el código pudo correr, no que los datos sean correctos.
