import pandas as pd

def cargar_frases_desde_csv(*paths):
    frases = []
    for path in paths:
        df = pd.read_csv(path)
        cols_frase = [c for c in df.columns if "Frase" in c]
        if not cols_frase:
            raise ValueError(f"No se encontró ninguna columna con 'Frase' en {path}")
        frases += df[cols_frase[0]].dropna().tolist()
    return frases