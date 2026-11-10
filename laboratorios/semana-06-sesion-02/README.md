# Semana 6, Sesión 2: Procesamiento en tiempo real: ¿lo necesita el proyecto?

> Objetivo de la sesión: decidir si tu proyecto necesita procesamiento en tiempo real, y producir/consumir un flujo simple de eventos con una herramienta de streaming.

**Lectura previa de esta sesión:** ["Introduction to Streaming for Data Scientists"](https://huyenchip.com/2022/08/03/stream-processing-for-data-scientists.html), Chip Huyen.

**Referencia de esta sesión:** ["Batch or Stream? The Eternal Data Processing Dilemma" (Towards Data Science)](https://towardsdatascience.com/batch-or-stream-the-ethernal-data-processing-dilemma/). Este laboratorio usa Redpanda en vez de Apache Kafka con Zookeeper: un solo binario que habla el mismo protocolo de red que Kafka, así que cualquier cliente de Kafka (incluida la librería de Python de este laboratorio) se conecta sin cambios. Es el mismo criterio que ya usó este curso con DuckDB en vez de BigQuery (Semana 5): la herramienta real de la industria es la referencia, y el laboratorio usa la alternativa más simple de levantar en una sola laptop sin perder compatibilidad de protocolo. La misma edición de Data Engineering Zoomcamp que ya sirve de referencia a este curso usa Redpanda en su propio módulo de streaming.

## Requisitos antes de esta sesión

1. **Docker y Docker Compose**, los mismos de la Semana 3.
2. **El cliente de Python para Kafka (`kafka-python`):** ya viene en el Codespace. En tu laptop, instálalo con `pip install -r requirements.txt` desde la raíz del repositorio.
3. Levanta Redpanda desde este laboratorio:
   ```
   docker compose -p lab-streaming up -d
   ```
   El archivo [`starter/docker-compose.yml`](./starter/docker-compose.yml) levanta un solo broker de Redpanda, escuchando en el puerto `9092`, el mismo puerto estándar de Kafka. Verifica que el contenedor arrancó con `docker compose -p lab-streaming ps`.

## Antes de empezar

A partir de la lectura previa:

**Según el artículo, ¿qué gana un sistema al procesar eventos uno por uno o en microlotes, frente a esperar y procesarlos todos juntos?**

Reduce la espera para actualizar indicadores, detectar problemas y utilizar información reciente en decisiones. La lectura muestra casos de predicción online y monitoreo en tiempo real; el beneficio depende de cuánto importe la latencia para el proyecto.

**El artículo advierte que streaming no es gratis: agrega complejidad operativa real. ¿Qué tipo de complejidad menciona, comparado con un job de batch?**

La lectura describe cálculo distribuido, resultados que cambian con el tiempo, fallos en cascada y decisiones entre disponibilidad y consistencia. También exige gestionar estado, checkpoints, recuperación y operación de procesos continuos. Esa complejidad debe justificarse por el caso de uso.

## Caso de apertura

Un compañero de clase construye un sistema de recomendación de productos y quiere que se actualice apenas un cliente hace clic en algo. Otro construye un modelo que predice el precio de una casa a partir de datos que se publican una vez al mes. ¿Cuál de los dos proyectos se beneficia de procesar los datos en tiempo real, y cuál no gana nada haciéndolo?

Las recomendaciones basadas en clics recientes pueden beneficiarse de streaming. Si los precios de viviendas solo se publican mensualmente y no hay otra entrada continua, procesar el mismo archivo en tiempo real no aporta información nueva; batch es suficiente.

## Ejercicio 1: producir y consumir pedidos

Archivos: [`starter/ejercicio1_productor.py`](./starter/ejercicio1_productor.py), que arma 10 pedidos, y [`starter/ejercicio1_consumidor.py`](./starter/ejercicio1_consumidor.py), que los lee del tópico `pedidos` y los cuenta por categoría. Los dos ya corren contra Redpanda, pero tienen 4 `TODO` entre los dos. Córrelos en orden antes de tocar nada:

```
cd laboratorios/semana-06-sesion-02/starter
python3 ejercicio1_productor.py
python3 ejercicio1_consumidor.py
```

**Respuesta 1 (TODO 1), antes de ver la solución:** el productor imprimió los 10 eventos y el consumidor no recibió ninguno. ¿Qué le falta al productor?

Faltaba productor.send("pedidos", value=evento). Imprimir el diccionario no lo publica en Redpanda; flush() espera el envío de los mensajes pendientes.

**Respuesta 2 (TODO 2):** con el TODO 1 resuelto, el consumidor sigue sin recibir nada si lo corres después del productor, pero sí los recibe si ya estaba corriendo cuando el productor publicó. ¿Por qué?

El consumidor empezaba al final por la configuración predeterminada latest. Con auto_offset_reset="earliest", y sin un offset guardado aplicable, puede empezar desde los primeros mensajes disponibles. Esta configuración no tiene group_id.

**Respuesta 3 (TODO 3):** ahora el consumidor imprime `b'{"id_pedido": 1, ...}'`. ¿Qué dos pasos de `serializar_evento` tiene que deshacer `deserializar_evento`, y en qué orden?

Primero datos.decode("utf-8") convierte los bytes en texto; luego json.loads(...) convierte el JSON en un diccionario de Python.

**Respuesta 4 (TODO 4):** si corres el consumidor una segunda vez, ¿vuelve a mostrar los 10 eventos? Y si corres el productor otra vez, ¿el tópico queda con 10 o con 20?

En esta configuración, sin grupo y con earliest, una nueva ejecución vuelve a leer los mensajes disponibles. Consumir no los elimina. Ejecutar otra vez el productor agrega diez mensajes: serían veinte si siguen disponibles los diez anteriores; no se deduplican por id_pedido.

**Lo que confirmó la salida, TODO por TODO:**

Inicialmente el resumen fue {}. Después de publicar y configurar earliest se recibieron diez mensajes como bytes. Tras deserializar llegaron como diccionarios. El conteo final fue hogar 4, ropa 3 y electronica 3; suma diez eventos. No se hizo una segunda publicación para afirmar un resultado observado de veinte mensajes.

## Durante el ConcepTest

No requerido para esta entrega, según indicación de la estudiante.

## Ejercicio 2: alertas de temperatura

Solo o en pareja. Archivos: [`starter/ejercicio2_productor.py`](./starter/ejercicio2_productor.py), que arma 8 lecturas de tres sensores, y [`starter/ejercicio2_consumidor.py`](./starter/ejercicio2_consumidor.py), que las lee del tópico `lecturas`. Son los mismos cuatro pasos del Ejercicio 1, más uno nuevo (TODO 5): una alerta cuando la temperatura pasa de 30 grados. Al final, el consumidor imprime una comprobación por TODO: complétalos hasta que todas digan `OK`.

```
python3 ejercicio2_productor.py
python3 ejercicio2_consumidor.py
```

**Respuesta 1:** ¿cuántas alertas aparecieron, de qué sensor, y en qué momento las imprimió el consumidor: al final, o a medida que llegaba cada lectura?

Aparecieron dos alertas del sensor techo: 31.5 y 33.0 grados. Se imprimieron dentro del bucle al procesar cada mensaje, antes del resumen final. Conteos: bodega 3, camara_fria 2 y techo 3. Todas las comprobaciones indicaron OK. El productor había publicado antes: se procesó un conjunto ya almacenado, no se midió latencia extremo a extremo en vivo.

**Respuesta 2:** si el productor corriera todo el día enviando una lectura por minuto, ¿en qué cambiaría tu consumidor? ¿Seguiría teniendo sentido `consumer_timeout_ms`?

Para una lectura por minuto, consumer_timeout_ms=10000 podría cerrar el consumidor entre mensajes. Un servicio continuo necesita una estrategia de espera y recuperación apropiada, supervisión y manejo del estado/offsets, en vez de terminar tras diez segundos de inactividad.

**Si terminas antes:** abre dos terminales y corre el consumidor del Ejercicio 2 en las dos al mismo tiempo, y después el productor. ¿Las dos reciben las 8 lecturas, o se las reparten? Compáralo con tu voto del ConcepTest.

No se ejecutó esta prueba opcional con dos terminales. Según la configuración sin group_id, cada consumidor puede leer todos los mensajes de forma independiente. Con el mismo grupo de consumidores, las particiones se reparten: no se garantiza un reparto de ocho lecturas entre ambos, pues depende del número de particiones. No hay voto del ConcepTest requerido.

## Ejercicio 3: tu propio proyecto, ¿streaming o batch?

Aplica las dos preguntas que decidieron el caso de apertura a tu propio proyecto, y produce/consume al menos un evento representativo de tu proyecto con Redpanda. Parte de la plantilla [`plantilla-kafka/`](./plantilla-kafka/), que trae los `TODO` marcados en `productor.py` y `consumidor.py` en vez del código en blanco: copia los dos archivos a `psets/proyecto/procesamiento/` y complétalos ahí.

### Paso 1: responde las dos preguntas de decisión para tu proyecto (5 minutos)

¿La decisión que tu proyecto habilita pierde valor si se toma con datos de hace una hora, un día o una semana? ¿Los datos de tu proyecto llegan de forma continua e impredecible, o en bloques ya definidos?

Para el alcance trabajado de Favorita se usa un catálogo estático descargado en CSV; no llega una fuente continua de cambios reales ni hay un requisito de reaccionar por segundo. Conclusión: batch para el catálogo actual. Un futuro flujo real de ventas o cambios operativos requeriría reevaluar latencia y fuentes. El streaming de este ejercicio es una simulación didáctica.

### Paso 2: escribe tu productor (7 minutos)

Reemplaza el tópico y los eventos de ejemplo por al menos un evento representativo de tu propio proyecto.

Tópico favorita_actualizaciones_tiendas. productor_tiendas.py publicó cinco eventos con store_nbr, city, tipo_evento="actualizacion_tienda" y simulado=True. Se usaron cinco IDs y ciudades ficticias de ejemplo: dos mensajes de Quito, dos de Guayaquil y uno de Cuenca. No se presentan como cambios reales ni como la ubicación real de esos IDs.

### Paso 3: escribe tu consumidor y confirma que recibe lo publicado (8 minutos)

consumidor_tiendas.py recibió los cinco diccionarios y mostró: Eventos por ciudad: {'Quito': 2, 'Guayaquil': 2, 'Cuenca': 1}. Cuenta mensajes, no tiendas únicas, y no actualiza el catálogo del warehouse. Si se repite el productor, se agregan nuevos mensajes y el conteo aumenta. Los scripts están en psets/proyecto/procesamiento/.

## Al terminar

Apaga Redpanda desde `starter/`:

```
docker compose -p lab-streaming down
```

Este broker no tiene volumen: down elimina el contenedor y sus mensajes. Para pausar conservando ese contenedor se utilizó docker compose -p lab-streaming stop, y start para retomarlo. Esto no sustituye un volumen persistente ni una copia de seguridad. Para el laboratorio integrador de la Semana 7 no los necesitas; si tu proyecto usa streaming, lo vuelves a levantar con `docker compose -p lab-streaming up -d` y tu productor genera los eventos otra vez.

## Antes de la próxima sesión

Ya decidiste si tu proyecto necesita streaming, y produjiste/consumiste tu primer flujo de eventos.

Pregunta: llevas cuatro semanas construyendo piezas sueltas del pipeline de tu proyecto (contenedor, infraestructura, orquestación, calidad, warehouse, modelado, batch, streaming). ¿Qué falta para que todas esas piezas corran juntas, de principio a fin, sin que tengas que ejecutarlas una por una a mano?

Falta integrarlas en un flujo con dependencias explícitas, entradas y salidas compatibles, pruebas y manejo de fallos. Kestra debe coordinar las etapas y conservar evidencia de ejecución. La descarga del CSV y su carga a DuckDB aún son manuales; los ejemplos de streaming no forman parte de una ingesta real continua de Favorita.
