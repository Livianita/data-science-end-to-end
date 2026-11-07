# Diagnóstico de calidad de datos: Corporación Favorita

Dataset: items.csv, archivo original del catálogo. Fecha: 2026-11-06.

## Duplicados

Se analizaron 4100 filas. Duplicados completos: 0. Identificadores item_nbr repetidos: 0. No hay evidencia para atribuir duplicados a una causa ni se justifica eliminar filas. Se recomienda validar la unicidad en futuras cargas.

## Valores faltantes

isna().sum() devolvió 0 en item_nbr, family, class y perishable. No se encontraron marcadores N/D, -, sin dato ni cadenas vacías después de quitar espacios. Las conversiones numéricas de item_nbr, class y perishable no produjeron faltantes.

No hay faltantes detectados para evaluar patrones. Esto no demuestra que el catálogo real esté completo. No se propone imputar ni eliminar registros sin evidencia adicional.

## Inconsistencias de esquema

item_nbr, class y perishable son int64; family es texto. item_nbr es un identificador y class un código categórico: su almacenamiento numérico no implica que sean magnitudes continuas.

Se encontraron 33 familias, sin espacios iniciales o finales. Normalizar mayúsculas y espacios mantiene 33 categorías. perishable solo contiene 0 y 1. No hay columnas de fecha.

No se detectaron inconsistencias en estas comprobaciones. Se recomienda contrastar códigos y categorías con el diccionario de datos antes de recodificarlos y validar el dominio de perishable en futuras cargas.

## Resumen

No se justifican eliminaciones ni imputaciones con la evidencia actual. La prioridad es preservar la unicidad de item_nbr y verificar coincidencias al unir con ventas. Este diagnóstico solo cubre items.csv, no todos los archivos del proyecto.

Se usó el dataset original. El pipeline de Semana 4, Sesión 1 y el diagnóstico de su salida siguen pendientes.
