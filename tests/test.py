import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from llama_cpp import Llama

# Cargar modelo local
llm = Llama(model_path="models/mistral-7b-instruct-v0.1.Q4_K_M.gguf")


def responder_con_llama(contexto, pregunta):
    prompt = (
        f"### Contexto:\n{contexto}\n\n"
        f"### Pregunta:\n{pregunta}\n\n"
        f"### Respuesta:"
    )
    out = llm(prompt, max_tokens=300)
    return out["choices"][0]["text"]

def cargar_frases(*paths):
    """Carga frases desde uno o varios CSV con columnas tipo 'Frase*'."""
    frases = []
    for path in paths:
        df = pd.read_csv(path)
        col = [c for c in df.columns if "Frase" in c][0]
        frases += df[col].dropna().tolist()
    return frases

def construir_indice(frases, modelo_path="models/all-MiniLM-L6-v2"):
    # Cargar modelo local desde disco
    modelo = SentenceTransformer(modelo_path)
    emb = modelo.encode(frases, show_progress_bar=True)
    index = faiss.IndexFlatL2(emb.shape[1])
    index.add(np.array(emb))
    return index, modelo, frases

def recuperar_contexto(pregunta, frases, modelo, index, k=5):
    emb = modelo.encode([pregunta])
    _, idxs = index.search(emb, k)
    return "\n".join([frases[i] for i in idxs[0]])


def main():
    # Rutas a los CSV generados previamente
    path_bloomberg = "./data/frases_bloomberg.csv"
    path_metricas = "./data/frases_metricas_titulizaciones.csv"

    print("Cargando frases...")
    frases = cargar_frases(path_bloomberg, path_metricas)

    print("Generando embeddings y construyendo índice...")
    index, modelo, frases = construir_indice(frases)

    print("Todo listo. Haz tus preguntas:")
    while True:
        pregunta = input("\nPregunta (o escribe 'salir'): ").strip()
        if pregunta.lower() == "salir":
            break
        contexto = recuperar_contexto(pregunta, frases, modelo, index)
        print("\nContexto relevante recuperado:\n")
        print(contexto)

        # Aquí puedes conectar tu modelo generativo (como Mistral o GPT local)
        # usando el contexto + pregunta
        respuesta = responder_con_llama(contexto, pregunta)
        print("\nRespuesta generada:\n")
        print(respuesta)

if __name__ == "__main__":
    main()
