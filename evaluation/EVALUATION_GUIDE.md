# Guía de evaluación

1. Ejecuta `python scripts/smoke_test.py` con una clave válida.
2. Comprueba que las respuestas incluyan las reglas esperadas de `questions.json`.
3. Verifica que toda respuesta informativa muestre al menos una fuente.
4. Confirma que preguntas fuera de alcance no generen datos inventados.
5. Registra latencia, errores, preguntas sin respuesta y retroalimentación negativa.

Criterio sugerido de aprobación: 90 % de respuestas con contenido correcto y 100 % de respuestas sensibles respaldadas por una fuente.
