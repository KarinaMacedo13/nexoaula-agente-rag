from src.agent import NexoAulaAgent

QUESTIONS = [
    "¿Qué necesito para obtener el certificado?",
    "¿Puedo pedir un reembolso después de tres días si avancé 10 %?",
    "¿Cuál es la comisión de afiliados?",
    "¿Quién fue Napoleón?",
]

if __name__ == "__main__":
    agent = NexoAulaAgent()
    for question in QUESTIONS:
        result = agent.invoke(question)
        print("\nPREGUNTA:", question)
        print("ACCIÓN:", result.get("accion_final"))
        print("RESPUESTA:", result.get("respuesta"))
        print("FUENTES:", [x.get("source") for x in result.get("citaciones", [])])
