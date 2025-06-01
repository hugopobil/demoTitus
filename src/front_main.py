import streamlit as st
from contextlib import suppress
import generar_datos
from utils import construir_indice, recuperar_contexto, cargar_llama_model, responder_con_llama
from azure_openai_utils import configurar_azure_openai, responder_con_azure
from data_loader import cargar_frases_desde_csv
from sintetica_loader import cargar_noticias_json
import sintetica_loader
import json

noticias_sinteticas_dir = "./data/info_sintetica/noticias_titulizaciones.json"

st.set_page_config(page_title="Consulta de Noticias de Titulizaciones", layout="wide")
st.title("📰 Consulta Inteligente de Noticias de Titulizaciones")

modelo = st.selectbox("Selecciona el modelo a usar:", ["local", "azure"])

with st.spinner("Generando datos..."):
    generar_datos.main()

path_bloomberg = "./data/todas_las_frases.csv"

st.info("Cargando frases desde Bloomberg...")
frases = cargar_frases_desde_csv(path_bloomberg)
if not frases:
    st.error("No se cargaron frases. Verifica los archivos de entrada.")
    st.stop()

st.info("Generando noticias sintéticas...")
sintetica_loader.main()

st.info("Cargando noticias sintéticas...")
noticias = cargar_noticias_json(noticias_sinteticas_dir)
frases += [n["contenido"] for n in noticias]

st.info("Cargando frases regulatorias...")
frases_regulatorias_path = "../data/info_sintetica/frases_regulatorias.json"
try:
    with open(frases_regulatorias_path, "r", encoding="utf-8") as f:
        frases_regulatorias = json.load(f)
    frases += [frase["contenido"] for frase in frases_regulatorias]
except Exception as e:
    st.error(f"Error al cargar las frases regulatorias: {e}")
    st.stop()

st.info("Construyendo índice...")
index, modelo_embed, frases = construir_indice(frases)

if modelo == "local":
    st.info("Cargando modelo LLaMA local...")
    modelo_llm = cargar_llama_model("../models/mistral-7b-instruct-v0.1.Q4_K_M.gguf")
else:
    st.info("Conectando con Azure OpenAI...")
    deployment_name = configurar_azure_openai()

st.success("Modelo cargado. Puedes hacer tus preguntas.")
pregunta = st.text_input("Escribe tu pregunta sobre titulizaciones:")

if pregunta:
    with st.spinner("Buscando contexto relevante..."):
        contexto = recuperar_contexto(pregunta, frases, modelo_embed, index)

    st.subheader("📌 Contexto relevante")
    st.write(contexto)

    with st.spinner("Generando respuesta..."):
        if modelo == "local":
            respuesta = responder_con_llama(contexto, pregunta, modelo_llm)
        else:
            respuesta = responder_con_azure(contexto, pregunta, deployment_name)

    st.subheader("📣 Respuesta generada")
    st.write(respuesta)

    with suppress(Exception):
        if modelo == "local":
            del modelo_llm
