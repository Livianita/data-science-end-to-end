from pathlib import Path

import duckdb

ruta_csv = Path(
    "C:/Users/lroja/Downloads/"
    "2KYdQok7ZT8eMLkv5SJbhk-tiendas_pipeline.csv"
)

ruta_base = Path(__file__).parent / "favorita_tiendas_dbt.duckdb"
con = duckdb.connect(str(ruta_base))

con.execute(
    """
    CREATE OR REPLACE TABLE tiendas AS
    SELECT * FROM read_csv_auto(?)
    """,
    [str(ruta_csv)],
)

total = con.execute("SELECT COUNT(*) FROM tiendas").fetchone()[0]
print(f"Tiendas cargadas: {total}")
por_ciudad = con.execute("""
    SELECT
        city AS ciudad,
        COUNT(*) AS numero_tiendas
    FROM tiendas
    GROUP BY city
    ORDER BY numero_tiendas DESC, ciudad
""").df()

print(por_ciudad.to_string(index=False))
con.close()