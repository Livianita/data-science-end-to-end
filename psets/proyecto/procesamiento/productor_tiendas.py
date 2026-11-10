import json
import time
from kafka import KafkaProducer


def serializar_evento(evento):
    return json.dumps(evento).encode("utf-8")

productor = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=serializar_evento,
)

# TODO: reemplaza "TODO_topico" por un nombre propio de tu proyecto
# (por ejemplo, el tipo de evento que tu proyecto generaria en tiempo real).
topico = "favorita_actualizaciones_tiendas"

# TODO: reemplaza esta lista por al menos 5 eventos representativos de tu
# propio proyecto, con las columnas reales que tu evento necesitaria.
eventos_a_publicar = [
    {
        "store_nbr": 1,
        "city": "Quito",
        "tipo_evento": "actualizacion_tienda",
        "simulado": True,
    },
    {
        "store_nbr": 2,
        "city": "Quito",
        "tipo_evento": "actualizacion_tienda",
        "simulado": True,
    },
    {
        "store_nbr": 3,
        "city": "Guayaquil",
        "tipo_evento": "actualizacion_tienda",
        "simulado": True,
    },
    {
        "store_nbr": 4,
        "city": "Cuenca",
        "tipo_evento": "actualizacion_tienda",
        "simulado": True,
    },
    {
        "store_nbr": 5,
        "city": "Guayaquil",
        "tipo_evento": "actualizacion_tienda",
        "simulado": True,
    },
]

for evento in eventos_a_publicar:
    productor.send(topico, value=evento)
    print(f"Publicado: {evento}")
    time.sleep(0.5)

productor.flush()
productor.close()
print("Productor terminado")
