-- Columnas usadas por el modelo intermedio.
select
    id_pedido,
    id_cliente,
    fecha,
    categoria,
    cantidad,
    precio_unitario
from raw_pedidos
