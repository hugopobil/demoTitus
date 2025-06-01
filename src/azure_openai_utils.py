import openai
import os

def configurar_azure_openai():
    openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
    openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
    openai.api_type = "azure"
    openai.api_version = "2023-05-15"
    return os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

def responder_con_azure(contexto, pregunta, deployment_name):
    prompt = (
        f"### Contexto:\n{contexto}\n\n"
        f"### Pregunta:\n{pregunta}\n\n"
        f"### Respuesta:"
    )

    response = openai.ChatCompletion.create(
        engine=deployment_name,
        messages=[
            {"role": "system", "content": "Eres un experto en titulizaciones y métricas financieras."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return response['choices'][0]['message']['content']
