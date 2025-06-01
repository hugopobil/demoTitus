
# Proyecto: Sistema de Extracción, Tratamiento y Consulta de Datos sobre Titulizaciones

## 1. Fuentes de datos utilizadas y arquitectura de backend

La arquitectura del sistema está diseñada para ofrecer un procesamiento robusto, escalable y modular de grandes volúmenes de información financiera. Las fuentes de datos, descritas a continuación, se integran a través de un proceso ETL (Extract, Transform, Load) que estructura los datos para su posterior análisis y consulta inteligente.

### Arquitectura técnica y flujo de datos

1. **Extracción (Extract)**
   - Conexión a APIs externas (Bloomberg, Refinitiv) y repositorios internos.
   - Descarga de documentos (PDFs, Excel, CSV).
   - Scraping de noticias desde portales web y RSS feeds.

2. **Transformación (Transform)**
   - Limpieza y estandarización de datos.
   - Procesamiento de documentos mediante OCR y NLP.
   - Enriquecimiento y creación de metadatos.

3. **Carga (Load)**
   - Inserción en bases de datos relacionales (PostgreSQL, SQL Server).
   - Indexación en motores vectoriales (FAISS, ChromaDB).

4. **Integración**
   - APIs para consulta por usuarios y modelos.
   - Control de versiones y trazabilidad de datos.

### Arquitecturas posibles

- Microservicios orquestados con Docker/Kubernetes.
- Flujos ETL con Airflow o Prefect.
- Arquitectura híbrida nube/on-premise.

## 2. Procesamiento de la información

Cada fuente requiere un tratamiento específico:

- **Datos de mercado**: Normalización, validación, homogeneización.
- **Documentación legal (PDF)**: OCR, extracción de entidades, clasificación.
- **Noticias financieras**: Análisis de sentimiento, detección de eventos, extracción de tópicos.
- **Ficheros internos**: Validación estructural y mapeo a esquema común.

## 3. Estructura de la base de datos

| Módulo         | Descripción |
|----------------|-------------|
| Mercado        | Datos por activo, fecha, tipo de spread, valor y fuente. |
| Documentación  | Tipo, origen, fecha, entidades extraídas. |
| Noticias       | Resumen, fuente, sentimiento, tópicos. |
| Activos        | ISIN, emisor, tipo, rating, fecha emisión. |

## 4. Flujo funcional

1. Ingesta desde múltiples fuentes.
2. Identificación y clasificación.
3. Procesamiento específico.
4. Homogeneización.
5. Almacenamiento relacional y vectorial.
6. Vectorización para búsquedas semánticas.
7. Generación textual.
8. Consulta por GPT.
9. Validación de respuestas.

## 5. Optimización del rendimiento

- Clustering temático previo.
- Indexación eficiente.
- Filtrado por metadatos.
- Cacheo de respuestas.
- Prompts adaptativos.

## 6. Tecnologías utilizadas (Python)

- Extracción: `requests`, `blpapi`, `pdfplumber`, `pytesseract`
- NLP: `spaCy`, `flair`, `BERTopic`, `transformers`
- Almacenamiento: `pandas`, `SQLAlchemy`, `pymongo`, `Azure SDK`
- Vectorización: `sentence-transformers`, `FAISS`, `ChromaDB`
- LLM: `openai`, `langchain`, `llama-index`
- Frontend: `FastAPI`, `Streamlit`, `Dash`

## 7. Público objetivo y usos dentro del banco

- Unidad de titulizaciones: análisis y comparación de activos.
- Riesgos de crédito y mercado: evaluación de exposiciones.
- Tesorería: decisiones de financiación.
- Legal/Compliance: acceso estructurado a documentos.
- Inversores: generación de informes comprensibles.
- Comunicación: seguimiento de noticias y análisis de sentimiento.

**Casos de uso:**
- Comparativas de precios.
- Análisis histórico de estructuras.
- Apoyo a decisiones de inversión.
- Alertas regulatorias y de eventos clave.

## 8. Funcionamiento del modelo de lenguaje

El sistema emplea un modelo basado en GPT que responde en lenguaje natural a partir de información heterogénea. 

### Relación con la vectorización

- Datos estructurados y textos son vectorizados.
- Al recibir una pregunta, se vectoriza y se busca en índices semánticos.
- La información relevante se inyecta como contexto en el prompt GPT.
- El modelo genera una respuesta estructurada con referencias y trazabilidad.

## 9. Perfiles profesionales y diseño de interfaz

### Perfiles requeridos

- Ingeniero/a de datos
- Científico/a de datos NLP
- Backend y frontend developers
- Especialista en bases de datos
- Ingeniero/a MLOps
- UX/UI
- Analista de negocio

### Interfaz UX

- Búsquedas naturales, visualización clara.
- Validación de resultados y navegación por fuentes.
- Tecnologías: `Streamlit`, `Dash`, `React`.

## Conclusión

Una solución integral que transforma datos diversos en respuestas claras y contextualizadas, fortaleciendo la toma de decisiones en áreas clave del banco.
