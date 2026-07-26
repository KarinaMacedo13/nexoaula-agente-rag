# Entrega final del proyecto NexoAula

## Alcance implementado

NexoAula es una prueba de concepto de una escuela online con un agente de inteligencia artificial que responde consultas utilizando recuperación aumentada por generación (RAG). La solución se apoya en cinco documentos institucionales coherentes y citables.

## Entregables incluidos

- Código fuente del agente y la interfaz.
- Cinco documentos institucionales en Markdown, DOCX y PDF.
- Manual institucional consolidado en DOCX y PDF.
- Matriz de reglas maestras para evitar contradicciones.
- Notebook didáctico para Google Colab.
- Banco de preguntas y guía de evaluación.
- Pruebas unitarias y verificador de consistencia.
- Dockerfile y Docker Compose.
- Guía de despliegue en OCI Compute.
- README, guía paso a paso y tablero sugerido para Trello.
- Plantilla de evidencia para el despliegue.

## Validaciones realizadas

- Compilación sintáctica de todos los archivos Python.
- Cinco pruebas automatizadas aprobadas.
- Verificación de consistencia de reglas aprobada.
- Renderizado y revisión visual de todos los DOCX.
- Preflight de los seis PDF: abiertos correctamente, no cifrados y con texto seleccionable.

## Acciones que requieren las credenciales del propietario

1. Crear el repositorio público en GitHub y subir el contenido.
2. Configurar una clave válida de Gemini en el archivo `.env` o en un gestor de secretos.
3. Ejecutar las pruebas funcionales que consumen la API.
4. Crear la instancia de OCI y desplegar el contenedor.
5. Añadir al README la URL pública y una captura o video del agente en OCI.

## Advertencia de uso

Las políticas y direcciones de correo son material ficticio para un proyecto académico. Antes de utilizar la solución comercialmente deben sustituirse los datos de ejemplo y realizarse una revisión legal, de privacidad, accesibilidad y protección al consumidor.
