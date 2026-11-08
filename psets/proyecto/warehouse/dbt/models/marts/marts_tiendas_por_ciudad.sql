-- TODO: renombra a marts_<tu_pregunta_de_negocio>.sql
-- Agrega el resultado de tu modelo intermedio en la pregunta final que tu proyecto necesita responder.
select
    ciudad,
    count(*) as numero_tiendas
from {{ ref('int_tiendas_ubicacion') }}
group by ciudad