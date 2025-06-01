import os
import json
import random
from pathlib import Path
from datetime import datetime, timedelta

# --- Generador de noticias sintéticas ---

temas = [
    "RMBS", "CMBS", "ABS", "CLO", "STS", "regulación", "riesgo crediticio", 
    "calificaciones", "impacto macroeconómico", "interés de inversores", 
    "mercado secundario", "precios", "volatilidad", "tipos de interés", 
    "transparencia", "retitulización", "datos ESG", "impagos", 
    "política monetaria", "nuevos productos"
]

plantillas = [
    "El mercado de {tema} muestra señales de {tendencia} debido a {razon}.",
    "Nuevas regulaciones en {region} afectan la emisión de {tema}.",
    "Analistas destacan {cambio} en los {tema} emitidos en los últimos meses.",
    "Los inversores institucionales incrementan su exposición a {tema} tras {evento}.",
    "El BCE comenta sobre el impacto de {tema} en la estabilidad financiera.",
    "Firmas de calificación como Moody's y Fitch revisan {tema} en sus nuevos informes.",
    "Empresas en {region} recurren más a {tema} para financiar activos tras {situacion}.",
    "El uso de criterios ESG en {tema} gana tracción entre gestores de fondos.",
    "Se detecta un aumento de impagos en {tema} vinculados a {sector}.",
    "{institucion} lanza una plataforma innovadora para facilitar la negociación de {tema}."
]

def generar_fecha_reciente(dias_max=90):
    return (datetime.now() - timedelta(days=random.randint(0, dias_max))).strftime('%Y-%m-%d')

def generar_noticia():
    tema = random.choice(temas)
    plantilla = random.choice(plantillas)
    contenido = plantilla.format(
        tema=tema,
        tendencia=random.choice(["fortaleza", "debilidad", "estabilidad", "crecimiento", "revalorización"]),
        razon=random.choice(["las políticas del BCE", "la baja morosidad", "el apetito de riesgo", "el contexto inflacionario", "los nuevos requerimientos regulatorios"]),
        region=random.choice(["Europa", "EE.UU.", "Asia", "Latinoamérica", "España", "Alemania", "Francia", "Italia"]),
        cambio=random.choice(["una mejora en la calidad", "un incremento de volumen", "una mayor estandarización", "una baja en las calificaciones"]),
        evento=random.choice(["la última decisión del BCE", "los cambios fiscales", "el aumento de rentabilidad", "el descenso de los spreads"]),
        institucion=random.choice(["Euroclear", "Bloomberg", "BlackRock", "JP Morgan", "AFME"]),
        situacion=random.choice(["la caída del crédito bancario", "el endurecimiento regulatorio", "la necesidad de liquidez"]),
        sector=random.choice(["el retail", "el turismo", "las oficinas", "la logística", "el residencial"])
    )
    return {
        "titulo": contenido.split(".")[0],
        "fecha": generar_fecha_reciente(),
        "contenido": contenido
    }

def generar_noticias(n=100):
    return [generar_noticia() for _ in range(n)]

# --- Gestión de archivos ---

def configurar_directorio_info_sintetica(base_dir="./data"):
    path = Path(base_dir) / "info_sintetica"
    path.mkdir(parents=True, exist_ok=True)
    return path

def guardar_noticias_json(noticias, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(noticias, f, ensure_ascii=False, indent=4)

def cargar_noticias_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# --- Ejecución principal ---
def main():
    dir_info = configurar_directorio_info_sintetica()
    path_json = dir_info / "noticias_titulizaciones.json"

    noticias_sinteticas = generar_noticias(10)

    print(path_json)
    guardar_noticias_json(noticias_sinteticas, path_json)
    print(f"Noticias guardadas en: {path_json}")

    noticias_cargadas = cargar_noticias_json(path_json)
    for noticia in noticias_cargadas[:5]:  # Mostrar solo las 5 primeras para no saturar
        print("-", noticia["titulo"])
