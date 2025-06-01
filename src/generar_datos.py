import pandas as pd
import numpy as np
import os
from colorama import Fore, Style, init
import shutil

# Inicializar colorama
init(autoreset=True)

def limpiar_y_crear_carpeta(data_dir="data"):
    """Limpia y crea la carpeta de salida."""
    if os.path.exists(data_dir):
        shutil.rmtree(data_dir)
    os.makedirs(data_dir)
    return data_dir

def generar_titulaciones_sinteticas(n=100, seed=42):
    """Genera datos sintéticos de titulizaciones."""
    np.random.seed(seed)
    activos = [
        "Hipotecas residenciales", "Hipotecas comerciales", "Préstamos personales",
        "Leasing vehículos", "Préstamos sindicados", "Tarjetas de crédito",
        "Factoring", "Créditos agrícolas"
    ]
    emisores = [
        "Banco Alfa", "Banco Beta", "Entidad Gamma", "Banco Delta",
        "Banco Epsilon", "Banco Zeta", "Cooperativa Lambda", "Financiera Omega"
    ]
    tramos = [
        "Senior", "Senior/Mezzanine", "Senior/Mezzanine/Equity", 
        "Senior/Equity", "Mezzanine", "Equity"
    ]
    calificaciones = ["AAA", "AA", "A", "BBB", "BB", "B", "CCC", "CC", "C"]
    anios = [2020, 2021, 2022, 2023, 2024]

    titulaciones = []
    for i in range(n):
        titulacion = {
            "ID": f"TIT{str(i+1).zfill(3)}",
            "Ano": np.random.choice(anios),
            "ActivoSubyacente": np.random.choice(activos),
            "Emisor": np.random.choice(emisores),
            "MoraMedia_3A": round(np.random.uniform(0.5, 3.5), 2),
            "Spread": np.random.randint(50, 200),
            "Calificacion": np.random.choice(calificaciones),
            "Tramos": np.random.choice(tramos)
        }
        titulaciones.append(titulacion)

    return pd.DataFrame(titulaciones)

def guardar_csv(df, filepath):
    """Guarda un DataFrame en un archivo CSV."""
    df.to_csv(filepath, index=False)
    print(Fore.GREEN + f"Archivo guardado: {filepath}")

def generar_todas_las_frases(df_titulaciones, data_dir):
    """Genera todas las frases (Bloomberg, resumen y activos) y las guarda en un único archivo CSV."""

    # Generar frases tipo Bloomberg
    frases_bloomberg = []
    for _, row in df_titulaciones.iterrows():
        frase = (
            f"En {int(row['Ano'])}, la titulización {row['ID']} respaldada por {row['ActivoSubyacente']} "
            f"emitida por {row['Emisor']} tuvo una mora media de {row['MoraMedia_3A']}%, un spread de "
            f"{row['Spread']} pb y una calificación {row['Calificacion']}. La estructura de tramos fue: "
            f"{row['Tramos']}."
        )
        frases_bloomberg.append({"Tipo": "Bloomberg", "ID": row["ID"], "Frase": frase})

    # Generar frases resumen por emisor y año
    resumen = df_titulaciones.groupby(["Emisor", "Ano"]).agg({
        "MoraMedia_3A": "mean",
        "Spread": "mean"
    }).reset_index()
    for _, row in resumen.iterrows():
        frase = (
            f"En {int(row['Ano'])}, el emisor {row['Emisor']} tuvo una mora media promedio de "
            f"{row['MoraMedia_3A']:.2f}% y un spread promedio de {row['Spread']:.2f} pb en sus titulizaciones."
        )
        frases_bloomberg.append({"Tipo": "Resumen", "ID": None, "Frase": frase})

    # Generar frases descriptivas por tipo de activo subyacente
    activos = df_titulaciones.groupby("ActivoSubyacente").agg({
        "MoraMedia_3A": "mean",
        "Spread": "mean"
    }).reset_index()
    for _, row in activos.iterrows():
        frase = (
            f"Las titulizaciones respaldadas por {row['ActivoSubyacente']} presentan una mora media promedio "
            f"de {row['MoraMedia_3A']:.2f}% y un spread promedio de {row['Spread']:.2f} pb."
        )
        frases_bloomberg.append({"Tipo": "Activos", "ID": None, "Frase": frase})

    # Guardar todas las frases en un único archivo CSV
    df_todas_las_frases = pd.DataFrame(frases_bloomberg)
    csv_todas_las_frases = os.path.join(data_dir, "todas_las_frases.csv")
    guardar_csv(df_todas_las_frases, csv_todas_las_frases)

def generar_frases_metricas(df_titulaciones, data_dir):
    """Genera frases métricas agregadas por activo."""
    agrupado = df_titulaciones.groupby(["ActivoSubyacente", "Ano"]).agg({
        "MoraMedia_3A": "mean"
    }).reset_index()

    agrupado["DefaultRate"] = (agrupado["MoraMedia_3A"] + np.random.normal(0.1, 0.3, len(agrupado))).round(2)
    agrupado["DelinquencyRate"] = (agrupado["DefaultRate"] + np.random.normal(0.2, 0.3, len(agrupado))).round(2)
    agrupado["InterestRate"] = np.random.normal(3.0, 0.5, len(agrupado)).round(2)

    frases_metricas = []
    for _, row in agrupado.iterrows():
        frase = (
            f"En {int(row['Ano'])}, las titulizaciones respaldadas por {row['ActivoSubyacente']} presentaron "
            f"un ratio de impago (default rate) del {row['DefaultRate']}%, una mora (delinquency rate) del "
            f"{row['DelinquencyRate']}% y un tipo de interés medio del {row['InterestRate']}%."
        )
        frases_metricas.append({
            "ActivoSubyacente": row["ActivoSubyacente"],
            "Año": row["Ano"],
            "FraseMetrica": frase
        })

    df_metricas = pd.DataFrame(frases_metricas)
    csv_metricas = os.path.join(data_dir, "frases_metricas_titulizaciones.csv")
    guardar_csv(df_metricas, csv_metricas)

def generar_metricas_tipos(data_dir, tipos_titulizacion, anios):
    """Genera métricas sintéticas por tipo de titulización."""
    metricas_tipos = []
    for tipo in tipos_titulizacion:
        for año in anios:
            default = round(np.random.normal(loc=2.0, scale=0.5), 2)
            delinquency = round(np.random.normal(loc=default + 0.5, scale=0.3), 2)
            interest = round(np.random.normal(loc=3.0, scale=0.7), 2)
            metricas_tipos.append({
                "TipoTitulizacion": tipo,
                "Año": año,
                "DefaultRate": max(default, 0.1),
                "DelinquencyRate": max(delinquency, 0.1),
                "InterestRate": max(interest, 0.1)
            })

    df_metricas_tipos = pd.DataFrame(metricas_tipos)
    csv_metricas_tipos = os.path.join(data_dir, "metricas_titulizaciones_sinteticas.csv")
    guardar_csv(df_metricas_tipos, csv_metricas_tipos)

def main():
    print(Fore.CYAN + "Generando datos sintéticos de titulizaciones...")
    data_dir = limpiar_y_crear_carpeta()

    df_titulaciones = generar_titulaciones_sinteticas()
    csv_base = os.path.join(data_dir, "titulaciones_sinteticas.csv")
    guardar_csv(df_titulaciones, csv_base)

    generar_todas_las_frases(df_titulaciones, data_dir)

    tipos_titulizacion = ["RMBS", "ABS", "CMBS", "CLO"]
    anios = [2020, 2021, 2022, 2023, 2024]
    generar_metricas_tipos(data_dir, tipos_titulizacion, anios)

if __name__ == "__main__":
    main()
