import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from llama_cpp import Llama
import os
from contextlib import redirect_stdout

def cargar_llama_model(model_path):
    with open(os.devnull, "w") as fnull:
        with redirect_stdout(fnull):
            llama = Llama(model_path=model_path)
    return llama

def responder_con_llama(contexto, pregunta, modelo_llm):
    prompt = (
        f"### Contexto:\n{contexto}\n\n"
        f"### Pregunta:\n{pregunta}\n\n"
        f"### Respuesta:"
    )
    out = modelo_llm(prompt, max_tokens=300)
    return out["choices"][0]["text"]

def construir_indice(frases, modelo_path="../models/all-MiniLM-L6-v2"):
    modelo = SentenceTransformer(modelo_path)  # Usa la ruta local
    embeddings = modelo.encode(frases, show_progress_bar=True)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return index, modelo, frases

def recuperar_contexto(pregunta, frases, modelo, index, k=5):
    emb = modelo.encode([pregunta])
    _, idxs = index.search(emb, k)
    return "\n".join([frases[i] for i in idxs[0]])
