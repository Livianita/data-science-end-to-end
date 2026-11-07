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

Es un flow con tres ejecuciones. Con probabilidad de fallo 0.5, el número esperado de fallos es 1.5; en tres ejecuciones concretas pueden fallar de cero a tres. Pendiente ejecutar y observar los resultados reales.

**Respuesta 2 (TODO 1):** ¿qué le agregarías al flow para que una falla de la fuente no dependa de que alguien lo vuelva a correr a mano?

Un retry de tipo constant, con maxAttempts: 3 e interval: PT10S, como pide el TODO. Debe aplicarse a la tarea que puede fallar; no garantiza éxito si la fuente sigue caída.

**Respuesta 3 (TODO 3):** con el trigger agregado, si la ejecución de una noche agota sus reintentos y falla, ¿la ejecución programada de la noche siguiente también falla, o corre normal?

La siguiente ejecución programada es independiente y vuelve a intentar normalmente. Si la causa persiste puede fallar también, pero no por heredar automáticamente el estado fallido anterior.

**Lo que confirmó la ejecución, TODO por TODO:**

Pendiente de ejecución: los flows locales aún conservan TODO. No se dispone de logs de intentos ni backfill para registrar resultados observados.

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

El script debe recibir la fecha del lunes recuperado. Usar la fecha actual produciría registros con una fecha equivocada y no reconstruiría el histórico. Pendiente verificarlo en los logs.

**Respuesta 2:** ¿alguna ejecución del backfill necesitó más de un intento? ¿Dónde lo ves en Kestra?

Pendiente: revisar en Kestra las ejecuciones del backfill y los intentos de cada tarea. No se ha observado una ejecución para afirmar cuántos intentos necesitó.

**Si terminas antes:** si la estación estuvo caída dos semanas seguidas, ¿subirías `maxAttempts` a 50, o harías un backfill cuando vuelva? ¿Qué problema resuelve cada uno?

Usaría reintentos acotados para fallos transitorios y backfill al recuperar la fuente tras dos semanas. Cincuenta intentos no sustituyen la reconstrucción de los periodos omitidos.

## Ejercicio 3: el flow de tu propio proyecto

Usa el mismo patrón de los Ejercicios 1 y 2, aplicado a la ingesta de tu proyecto. En vez de `python:3.11-slim` y un archivo del namespace, el flow corre la imagen de Docker que construiste en la Semana 3, Sesión 1: ahí ya están tu script y sus dependencias. Parte de la plantilla [`plantilla-flow/flow_proyecto.yml`](./plantilla-flow/flow_proyecto.yml).

### Paso 1: el task que corre tu imagen (5 minutos)

Confirma con `docker images` que la imagen de tu proyecto existe en tu máquina (si no, vuelve a construirla con `docker build -t <nombre>:<tag> .`). Completa `id`, `namespace`, `containerImage` con el nombre y el tag de tu imagen, y el comando que corre tu script con la ruta completa de su `WORKDIR` (por ejemplo, `python /app/ingesta.py`): Kestra corre los comandos en su propia carpeta de trabajo, no en la de tu imagen. `pullPolicy: NEVER` le dice a Kestra que use la imagen local en vez de buscarla en Docker Hub.

Pendiente: la plantilla del flow todavía no define id, namespace ni imagen del proyecto. No se declara este ejercicio como terminado.

### Paso 2: decide el retry (5 minutos)

Piensa en tu fuente de datos: ¿es una API externa que a veces no responde? ¿un archivo que a veces todavía no está listo? Decide `maxAttempts` e `interval` según qué tan probable y qué tan larga es esa falla, y descomenta el bloque `retry`.

Propuesta pendiente de implementar: pocos reintentos separados por un intervalo razonable para fallos transitorios. Si falta un CSV estático de Favorita, primero hay que corregir la ruta o disponibilidad; repetir indefinidamente no lo resuelve.

### Paso 3: agrega el trigger Schedule (6 minutos)

Descomenta el bloque `triggers` y elige una expresión cron con la frecuencia que tenga sentido para tu proyecto. No todos los proyectos necesitan correr todos los días.

Pendiente de definir según la actualización de la fuente. Un catálogo estático no necesita reingesta diaria solo para simular actividad; la frecuencia debe corresponder a datos nuevos disponibles.

Súbelo con `bash ../starter/subir_a_kestra.sh flow_proyecto.yml` desde `plantilla-flow/` (sin scripts: ya están en la imagen) y ejecútalo manualmente al menos una vez para confirmar que corre sin errores.

Pendiente: construir y subir el flow del proyecto, ejecutarlo y guardar evidencia. La carga posterior del warehouse se hizo sobre el CSV original, no sobre una salida de este pipeline.

## Antes de la próxima sesión

Ya tienes tu pipeline de ingesta corriendo solo, todos los días o con la frecuencia que decidiste.

Pregunta: ¿cómo sabes si los datos que trajo son datos buenos, o datos con problemas que ningún error de ejecución te va a avisar?

Aplicaría controles de duplicados, faltantes, tipos, rangos, formatos e integridad entre tablas. Que una ejecución termine bien solo demuestra que el código pudo correr, no que los datos sean correctos.
