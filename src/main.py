import argparse
from colorama import Fore, init
from contextlib import suppress
import generar_datos
from utils import construir_indice, recuperar_contexto, cargar_llama_model, responder_con_llama
from azure_openai_utils import configurar_azure_openai, responder_con_azure
from data_loader import cargar_frases_desde_csv
from sintetica_loader import cargar_noticias_json
import sintetica_loader
import json

noticias_sinteticas_dir = "./data/info_sintetica/noticias_titulizaciones.json"

# Inicializar colorama
init(autoreset=True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--modelo", choices=["local", "azure"], default="local", help="Modelo a usar: local o azure")
    args = parser.parse_args()

    generar_datos.main()

    path_bloomberg = "./data/todas_las_frases.csv"

    print(Fore.CYAN + "Cargando frases...")
    frases = cargar_frases_desde_csv(path_bloomberg)
    if not frases:
        raise ValueError("No se cargaron frases. Verifica los archivos de entrada.")

    print(Fore.CYAN + "Generando noticias sintéticas...")
    sintetica_loader.main()

    print(Fore.CYAN + "Cargando noticias sintéticas...")
    noticias = cargar_noticias_json(noticias_sinteticas_dir)
    frases += [n["contenido"] for n in noticias]

    print(Fore.CYAN + "Cargando frases regulatorias...")
    frases_regulatorias_path = "./data/info_sintetica/frases_regulatorias.json"
    with open(frases_regulatorias_path, "r", encoding="utf-8") as f:
        frases_regulatorias = json.load(f)
    frases += frases_regulatorias

    print(Fore.CYAN + "Generando embeddings y construyendo índice...")
    index, modelo_embed, frases = construir_indice(frases)

    if args.modelo == "local":
        print(Fore.CYAN + "Cargando modelo LLaMA local...")
        modelo_llm = cargar_llama_model("../models/mistral-7b-instruct-v0.1.Q4_K_M.gguf")
    else:
        print(Fore.CYAN + "Conectando con Azure OpenAI...")
        deployment_name = configurar_azure_openai()

    print(Fore.GREEN + "Todo listo. Haz tus preguntas:")

    try:
        while True:
            pregunta = input(Fore.YELLOW + "\nPregunta (o escribe 'salir'): ").strip()
            if pregunta.lower() == "salir":
                print(Fore.RED + "Saliendo del programa. ¡Hasta luego!")
                break
            if not pregunta:
                print(Fore.RED + "La pregunta no puede estar vacía.")
                continue

            contexto = recuperar_contexto(pregunta, frases, modelo_embed, index)
            print(Fore.MAGENTA + "\nContexto relevante recuperado:\n")
            print(Fore.WHITE + contexto)

            if args.modelo == "local":
                respuesta = responder_con_llama(contexto, pregunta, modelo_llm)
            else:
                respuesta = responder_con_azure(contexto, pregunta, deployment_name)

            print(Fore.BLUE + "\nRespuesta generada:\n")
            print(Fore.WHITE + respuesta)
    finally:
        with suppress(Exception):
            if args.modelo == "local":
                del modelo_llm

if __name__ == "__main__":
    main()