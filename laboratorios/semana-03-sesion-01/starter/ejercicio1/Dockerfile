# Ejercicio 1: imagen de procesar.py.
# Este Dockerfile ya construye. Construyelo y correlo antes de tocar nada
# (los comandos estan en el README).

FROM python:3.11-slim
WORKDIR /app

# TODO 1: cambia una linea de procesar.py y vuelve a construir: pandas se
# instala otra vez. Reordena estas lineas para que un cambio en el codigo
# no repita la instalacion de dependencias.
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY procesar.py .
# TODO 2: la imagen no dice que correr. Define el comando por defecto:
# python procesar.py
CMD ["python", "procesar.py"]

# TODO 3: agrega un argumento para que el script pueda recibir el nombre del archivo de entrada.
# Sin el montaje, la imagen no encuentra datos/ventas.csv. Con -v, el contenedor lee y escribe en mi carpeta local datos, por lo que puedo consultar el resultado después de que termina.cd