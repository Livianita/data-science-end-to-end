import json
from kafka import KafkaConsumer


def deserializar_evento(datos):
    return json.loads(datos.decode("utf-8"))

# TODO: usa el mismo nombre de topico que en productor.py.
topico = "favorita_actualizaciones_tiendas"

consumidor = KafkaConsumer(
    topico,
    bootstrap_servers="localhost:9092",
    value_deserializer=deserializar_evento,
    auto_offset_reset="earliest",
    consumer_timeout_ms=10000,
)

eventos_por_ciudad = {}

for mensaje in consumidor:
    evento = mensaje.value
    print(f"Consumido: {evento}")

    ciudad = evento["city"]
    eventos_por_ciudad[ciudad] = (
        eventos_por_ciudad.get(ciudad, 0) + 1
    )

consumidor.close()
print("Eventos por ciudad:", eventos_por_ciudad)
