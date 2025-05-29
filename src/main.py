import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from utils import cargar_frases, construir_indice, recuperar_contexto
from colorama import Fore, Style, init
import os
import sys
from contextlib import redirect_stdout, suppress
from llama_cpp import Llama

# Inicializar colorama
init(autoreset=True)

# -----------------------
# Cargar modelo sin logs
# -----------------------
def cargar_llama_model(model_path):
    with open(os.devnull, "w") as fnull:
        with redirect_stdout(fnull):
            llama = Llama(model_path=model_path)
    return llama

# Ruta al modelo .gguf descargado
MODEL_PATH = "models/mistral-7b-instruct-v0.1.Q4_K_M.gguf"
llm = cargar_llama_model(MODEL_PATH)

# -----------------------
# Respuesta generativa
# -----------------------
def responder_con_llama(contexto, pregunta):
    prompt = (
        f"### Contexto:\n{contexto}\n\n"
        f"### Pregunta:\n{pregunta}\n\n"
        f"### Respuesta:"
    )
    out = llm(prompt, max_tokens=300)
    return out["choices"][0]["text"]

# -----------------------
# Flujo principal
# -----------------------
def main():
    path_bloomberg = "./data/frases_bloomberg.csv"
    path_metricas = "./data/frases_metricas_titulizaciones.csv"

    print(Fore.CYAN + "Cargando frases...")
    frases = cargar_frases(path_bloomberg, path_metricas)

    print(Fore.CYAN + "Generando embeddings y construyendo índice...")
    index, modelo, frases = construir_indice(frases)

    print(Fore.GREEN + "Todo listo. Haz tus preguntas:")
    try:
        while True:
            pregunta = input(Fore.YELLOW + "\nPregunta (o escribe 'salir'): ").strip()
            if pregunta.lower() == "salir":
                print(Fore.RED + "Saliendo del programa. ¡Hasta luego!")
                break
            contexto = recuperar_contexto(pregunta, frases, modelo, index)
            print(Fore.MAGENTA + "\nContexto relevante recuperado:\n")
            print(Fore.WHITE + contexto)

            respuesta = responder_con_llama(contexto, pregunta)
            print(Fore.BLUE + "\nRespuesta generada:\n")
            print(Fore.WHITE + respuesta)
    finally:
        # Cierre limpio para evitar traceback de __del__
        with suppress(Exception):
            del llm

if __name__ == "__main__":
    main()
