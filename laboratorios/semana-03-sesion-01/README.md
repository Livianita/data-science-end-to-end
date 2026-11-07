# Semana 3, Sesión 1: Contenedores para pipelines de proyectos

> Objetivo de la sesión: empaquetar el entorno de trabajo de tu proyecto propio en una imagen de Docker reproducible, y explicar qué problema de "funciona en mi máquina" resuelve un contenedor.

**Lectura previa de esta sesión:** ["How Docker Can Help You Become a More Effective Data Scientist"](https://medium.com/data-science/how-docker-can-help-you-become-a-more-effective-data-scientist-7fc048ef91d5), Towards Data Science / Medium.

**Referencia de esta sesión:** [Data Engineering Zoomcamp, Módulo 1 (DataTalksClub)](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/01-docker-terraform).

## Requisitos antes de esta sesión

Abre el Codespace de tu fork (ver [Tu ambiente de desarrollo](../../README.md#tu-ambiente-de-desarrollo) en el README del repositorio): Docker ya viene instalado. Confirma que funciona corriendo `docker run hello-world` en la terminal. Si prefieres trabajar en tu laptop, instala [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows, Mac o Linux) y corre la misma verificación. Si tu proyecto necesita GPU o un ambiente que no corre bien en ninguna de las dos opciones, avísame antes de esta sesión.

El Codespace también es un contenedor, pero no reemplaza el Dockerfile que construyes hoy. El Codespace trae las herramientas del curso, iguales para todos. La imagen de tu proyecto trae solo lo que tu proyecto necesita para correr en cualquier máquina, incluida una que nunca abrió este repositorio.

## Antes de empezar

A partir de la lectura previa:

**Según el artículo, ¿qué diferencia hay entre una imagen de Docker y un contenedor?**

Una imagen es una plantilla que contiene el entorno y los archivos necesarios para ejecutar una aplicación. Un contenedor es una instancia creada a partir de esa imagen. Puedo crear varios contenedores usando la misma imagen.

**¿Qué captura Docker, además de las librerías de Python, que un `requirements.txt` por sí solo no captura?**

El Dockerfile permite definir la versión de Python, el entorno base del sistema operativo, las dependencias del sistema, la carpeta de trabajo, el código y el comando de ejecución. Un requirements.txt solo especifica dependencias de Python. Los contenedores comparten el kernel del entorno donde se ejecutan.

## Pregunta de apertura

¿Por qué un notebook que corre perfecto en mi laptop podría fallar por completo en la tuya, aunque ambos tengan el mismo código?

El mismo notebook puede fallar en otra máquina por diferencias en las versiones de Python y sus librerías, dependencias del sistema, rutas, datos disponibles o variables de entorno. En este laboratorio observé que mi máquina y Docker tenían versiones distintas de Python y pandas.

## Ejercicio 1: la imagen de un script con pandas y datos

Carpeta: [`starter/ejercicio1/`](./starter/ejercicio1/). `procesar.py` lee `datos/ventas.csv` con pandas, imprime el total por producto y guarda `datos/resumen_ventas.csv`. El [`Dockerfile`](./starter/ejercicio1/Dockerfile) ya construye, pero tiene dos `TODO`. Constrúyelo y córrelo antes de tocar nada:

```
cd laboratorios/semana-03-sesion-01/starter/ejercicio1
docker build -t procesar-ventas .
docker run procesar-ventas
```

**Respuesta 1, antes de ver la solución:** el Dockerfile fija `python:3.11-slim` y no solo `python`. ¿Qué cambiaría en un año si dijera solo `python`?

Si utilizara solo python, Docker usaría la etiqueta latest, que con el tiempo podría apuntar a otra versión de Python y afectar la compatibilidad del código. python:3.11-slim mantiene la versión principal y secundaria y usa una variante reducida. Sin embargo, esa etiqueta también puede recibir actualizaciones; no fija una imagen exacta.

**Respuesta 2 (TODO 1):** si cambias una línea de `procesar.py` y vuelves a construir, ¿qué pasos se repiten? ¿Cómo reordenarías las líneas para que `pip install` no se repita?

Con COPY . . antes de pip install, modificar procesar.py invalida la capa de copia y obliga a ejecutar nuevamente la instalación. Lo resolví copiando primero requirements.txt, instalando las dependencias y copiando después el script. Al cambiar solo el código, pip install apareció como CACHED

**Respuesta 3 (TODO 2):** `docker run procesar-ventas` termina sin imprimir nada y sin error. ¿Qué le falta a la imagen?

Faltaba definir el comando por defecto para ejecutar el script. Agregué CMD ["python", "procesar.py"]. Antes de ese cambio, ejecutar el contenedor no iniciaba nuestro procesamiento.

**Respuesta 4 (TODO 3, el comando de `docker run`):** con los TODO 1 y 2 resueltos, la imagen solo copia `procesar.py`. ¿Encuentra `datos/ventas.csv` al correr? Y si lo encontrara, ¿dónde quedaría `resumen_ventas.csv` cuando el contenedor termina?

Como la imagen solo copia el script y requirements.txt, no encuentra datos/ventas.csv sin un montaje. Si el archivo de entrada estuviera dentro del contenedor, el resumen también se guardaría allí. Permanecería al detener el contenedor, pero se perdería al eliminarlo. Con un montaje puedo guardar el resultado directamente en mi máquina.

**Lo que confirmó la salida, TODO por TODO:**

El Dockerfile final sigue este orden: `FROM python:3.11-slim`, `WORKDIR /app`, `COPY requirements.txt .`, `RUN pip install -r requirements.txt`, `COPY procesar.py .`, `CMD ["python", "procesar.py"]`.

Comando reproducible en PowerShell, desde `starter/ejercicio1`:

```powershell
docker run --rm -v "${PWD}/datos:/app/datos" procesar-ventas
```

Comprobé que las dependencias se reutilizan desde la caché cuando solo cambia el código. Después de agregar CMD, el script arrancó, pero produjo FileNotFoundError porque faltaban los datos. Al montar la carpeta datos, generó el resumen en mi máquina: monitor 409.99, teclado 117.5 y mouse 33.5. Me llamó la atención que los archivos locales no están disponibles automáticamente dentro del contenedor.

## Durante el ConcepTest

No requerido para esta entrega, según indicación de la estudiante.

## Ejercicio 2: la imagen de un resumen de clientes

Solo o en pareja. Carpeta: [`starter/ejercicio2/`](./starter/ejercicio2/). `resumir_clientes.py` cuenta los clientes por ciudad y guarda `datos/clientes_por_ciudad.csv`; `contar_filas.py` guarda el total de clientes en `datos/conteo.txt`. Escribe el `Dockerfile` con el mismo patrón del Ejercicio 1 (TODO 1 a 3), y después:

- **TODO 4:** corre la imagen con un volumen para que `clientes_por_ciudad.csv` aparezca en tu carpeta `datos/`.
- **TODO 5:** corre `contar_filas.py` con la misma imagen, sin cambiar el Dockerfile ni volver a construir. Pista: lo que escribes después del nombre de la imagen en `docker run` reemplaza el `CMD`.

Revisa tu avance con:

```
bash comprobar.sh
```

**Respuesta 1:** ¿qué comando usaste en el TODO 5? ¿Qué significa, entonces, que `CMD` sea el comando "por defecto"?

Comando para ejecutar desde `starter/ejercicio2`, después de construir `resumir-clientes`:

```powershell
docker run --rm -v "${PWD}/datos:/app/datos" resumir-clientes python contar_filas.py
```

CMD es el comando por defecto porque se ejecuta cuando no proporciono otro después del nombre de la imagen. En esta ejecución lo reemplacé por python contar_filas.py, sin modificar el Dockerfile ni reconstruir la imagen.

**Respuesta 2:** si borras `datos/clientes_por_ciudad.csv` de tu carpeta y corres la imagen otra vez sin `-v`, ¿qué pasa?

Si borro el resultado local y ejecuto la imagen sin -v, el script no encuentra datos/clientes.csv, porque no copiamos los datos a la imagen. La ejecución falla y no vuelve a crear el resumen en mi carpeta local.
**Si terminas antes:** `contar_filas.py` no usa pandas. ¿Valdría la pena una imagen aparte para él, sin `pip install`? ¿Qué ganarías y qué perderías?

Una imagen separada para contar_filas.py podría ser más pequeña, tener menos dependencias y evitar instalar pandas. A cambio, tendría que mantener y construir dos imágenes. Para este ejercicio resulta práctico usar una sola imagen con ambos scripts; separarlas tendría más sentido si se desplegaran de forma independiente.

## Ejercicio 3: el Dockerfile de tu propio proyecto

Usa el mismo patrón de los Ejercicios 1 y 2, aplicado al ambiente de tu proyecto. Parte de la plantilla [`plantilla-dockerfile/Dockerfile`](./plantilla-dockerfile/Dockerfile), que trae los `TODO` marcados en vez del Dockerfile en blanco.

### Paso 1: identifica tus dependencias reales (5 minutos)

Lista las librerías externas que tu proyecto necesita (lo que normalmente instalarías con `pip install`). Si todavía no tienes un `requirements.txt`, créalo ahora con esa lista.

Para esta primera exploración de Cfavorita necesito pandas==2.2.2. argparse y pathlib forman parte de la biblioteca estándar de Python y no requieren instalación con pip. El script lee stores.csv y genera un diagnóstico por columna.

### Paso 2: completa el Dockerfile (10 minutos)

Edita `plantilla-dockerfile/Dockerfile`: resuelve cada `TODO`, decidiendo el orden de las instrucciones pensando en la cache (dependencias antes que código), y agrega un volumen en tus notas si tu proyecto lee o escribe datos.

### Paso 3: construye y verifica (5 minutos)

```
docker build -t <nombre-de-tu-proyecto> .
docker run <con -v si tu proyecto usa datos> <nombre-de-tu-proyecto>
```

Confirma que el resultado dentro del contenedor coincide con correr tu código directamente en tu máquina.


Ejecuté el mismo script con los mismos datos en mi máquina y en Docker. Los conteos de valores distintos y faltantes coincidieron. Las columnas city, state y type aparecieron como object dentro del contenedor y como str en el ambiente local. Los ambientes usan versiones diferentes: Python 3.11 y pandas 2.2.2 en Docker, frente a Python 3.14.7 y pandas 3.0.5 en mi máquina. Los archivos de diagnóstico no fueron idénticos, aunque las métricas coincidieron.

## Antes de la próxima sesión

Ya tienes tu proyecto empaquetado en una imagen reproducible.

Pregunta: ¿qué pasa si necesitas provisionar el almacenamiento de datos donde ese contenedor va a leer y escribir, sin hacerlo a mano cada vez?

Necesitaría automatizar la creación y configuración del almacenamiento mediante infraestructura como código. El contenedor empaqueta la aplicación, pero no provisiona por sí solo el almacenamiento externo que esta necesita.
