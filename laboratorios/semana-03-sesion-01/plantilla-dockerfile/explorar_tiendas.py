import argparse
from pathlib import Path

import pandas as pd

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--entrada", default="/datos/stores.csv")
    parser.add_argument("--salida", default="/resultados/diagnostico_tiendas.csv")
    args = parser.parse_args()

    tiendas = pd.read_csv(args.entrada)
    diagnostico = pd.DataFrame({
        "columna": tiendas.columns,
        "tipo": tiendas.dtypes.astype(str).to_numpy(),
        "faltantes": tiendas.isna().sum().to_numpy(),
        "valores_distintos": tiendas.nunique().to_numpy()
    })

    salida = Path(args.salida)
    salida.parent.mkdir(parents=True, exist_ok=True)
    diagnostico.to_csv(salida, index=False)

    print(f"Filas; {len(tiendas)} | Columnas: {len(tiendas.columns)}")
    print(diagnostico.to_string(index=False))
    print(f"Guardado en {salida}")

if __name__ == "__main__":
    main()