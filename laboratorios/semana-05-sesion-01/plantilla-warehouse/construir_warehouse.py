import duckdb

# TODO: conecta a un archivo .duckdb propio de tu proyecto (se crea solo si no existe).
con = duckdb.connect("favorita.duckdb")

# TODO: reemplaza por la ruta real del archivo que tu pipeline de la Semana 4 genera,
# y por un nombre de tabla propio de tu proyecto.
con.execute("""
    CREATE OR REPLACE TABLE items AS
    SELECT * FROM read_csv_auto('C:/Users/lroja/MSDS/Data Science/Cfavorita/items.csv/items.csv')
""")

# TODO: primera consulta, cuántas filas cargaste.
total_filas = con.execute("SELECT COUNT(*) FROM items").fetchone()[0]
print(f"Filas cargadas: {total_filas}")

# TODO: segunda consulta, una agregación (GROUP BY) que responda una pregunta real de tu proyecto.
resultado = con.execute("""
    SELECT family, COUNT(*) AS cantidad_productos
    FROM items
    GROUP BY family
    ORDER BY cantidad_productos DESC
""").df()
print(resultado)
con.close()
