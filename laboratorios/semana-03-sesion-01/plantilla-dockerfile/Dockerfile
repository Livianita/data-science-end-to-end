# Ejercicio 3: Dockerfile de tu propio proyecto.
# Completa cada TODO. Usa el mismo orden de instrucciones que los Ejercicios 1 y 2:
# la base, despues las dependencias, despues tu codigo.

# TODO: elige la imagen base. Para la mayoria de proyectos de este curso: python:3.11-slim
FROM python:3.11-slim

# TODO: fija la carpeta de trabajo dentro del contenedor (ej. /app)
WORKDIR /app

# TODO: copia tu archivo de dependencias (ej. requirements.txt) ANTES que tu codigo
COPY requirements.txt .

# TODO: instala tus dependencias
RUN pip install -r requirements.txt

# TODO: copia el resto de tu codigo (ej. tu script principal, o la carpeta src/)
COPY explorar_tiendas.py .

# TODO: define el comando que corre tu proyecto por defecto
CMD ["python", "explorar_tiendas.py"]
