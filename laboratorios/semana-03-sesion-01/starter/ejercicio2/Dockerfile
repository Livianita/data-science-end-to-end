# Ejercicio 2: imagen de resumir_clientes.py, con el mismo patron del
# Ejercicio 1. Corre bash comprobar.sh para revisar tu avance.

# TODO 1: imagen base, con la misma version de Python del Ejercicio 1.


# TODO 2: carpeta de trabajo, dependencias y codigo, en el orden que
# aprovecha la cache.
FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY resumir_clientes.py contar_filas.py .

CMD ["python", "resumir_clientes.py"]
# TODO 3: comando por defecto: python resumir_clientes.py
