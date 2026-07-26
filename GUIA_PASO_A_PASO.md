# Guía paso a paso del proyecto

## Etapa 1. Definir el problema
El asistente responde consultas repetitivas de estudiantes usando documentos oficiales. No reemplaza a soporte humano en excepciones, pagos concretos, seguridad o correcciones.

## Etapa 2. Crear y curar los documentos
Se elaboraron cinco documentos con reglas consistentes. La matriz `docs/policy_matrix.csv` reúne los valores que no deben contradecirse.

## Etapa 3. Extraer y fragmentar
`src/documents.py` lee PDF, CSV, Markdown y texto. El contenido se divide en fragmentos de 900 caracteres con una superposición de 150 para conservar contexto.

## Etapa 4. Crear embeddings e indexar
Gemini Embedding transforma cada fragmento en un vector. FAISS guarda los vectores y permite recuperar contenido semánticamente similar.

## Etapa 5. Generar respuestas con RAG
La pregunta recupera hasta cinco fragmentos. Gemini 2.5 Flash recibe únicamente esos fragmentos y debe reconocer cuando la base no contiene la respuesta.

## Etapa 6. Orquestar con LangGraph
El grafo tiene cuatro nodos: triaje, auto-resolver, pedir información y abrir ticket. Las aristas condicionales deciden el camino.

## Etapa 7. Crear la interfaz
Streamlit muestra el chat, ejemplos, acción del flujo y fuentes con archivo, página y extracto.

## Etapa 8. Probar
Las pruebas verifican la lógica básica del triaje, la presencia de los cinco documentos y la consistencia de las reglas. El banco de evaluación incluye preguntas correctas, ambiguas y fuera de alcance.

## Etapa 9. Contenerizar
Docker empaqueta la aplicación y sus dependencias. El archivo `.env` se inyecta en tiempo de ejecución y nunca se incluye en la imagen pública.

## Etapa 10. Desplegar en OCI
OCI Compute ejecuta el contenedor. Debes habilitar el puerto, configurar la clave, capturar evidencia y añadir la URL pública al README.
