from __future__ import annotations

from .config import Settings
from .schemas import TriageOutput

TRIAGE_PROMPT = """
Eres responsable del triaje de soporte de NexoAula. Devuelve una salida estructurada.

AUTO_RESOLVER: pregunta clara sobre reglamento, cursos, acceso, reembolsos, certificados, plataforma, becas o afiliados que pueda responderse con documentos.
PEDIR_INFO: mensaje ambiguo, incompleto o que no identifica el curso, pago, certificado o problema necesario.
ABRIR_TICKET: solicitud de excepción, corrección de datos, devolución concreta, cobro, acceso bloqueado, certificado errado, denuncia de conducta o petición explícita de soporte humano.

Urgencia ALTA: posible fraude, seguridad, acoso, cobro no reconocido o pérdida de acceso durante una evaluación en curso.
Urgencia MEDIA: pagos, certificados, acceso o fechas próximas.
Urgencia BAJA: consultas informativas.
""".strip()


class TriageService:
    def __init__(self, settings: Settings):
        from langchain_google_genai import ChatGoogleGenerativeAI

        llm = ChatGoogleGenerativeAI(
            model=settings.chat_model, temperature=0, google_api_key=settings.api_key
        )
        self.chain = llm.with_structured_output(TriageOutput)

    def classify(self, message: str) -> dict:
        try:
            from langchain_core.messages import HumanMessage, SystemMessage

            result = self.chain.invoke([
                SystemMessage(content=TRIAGE_PROMPT),
                HumanMessage(content=message),
            ])
            return result.model_dump()
        except Exception:
            return heuristic_triage(message)


def heuristic_triage(message: str) -> dict:
    text = message.lower().strip()
    critical = ["fraude", "hack", "hackeo", "acos", "cobro no reconocido", "robaron mi cuenta"]
    ticket = ["excepción", "autorizar", "corregir mi nombre", "reembolso de mi", "devolver mi dinero", "abrir ticket", "no puedo entrar", "certificado equivocado"]
    vague = ["ayuda", "tengo un problema", "no funciona", "consulta"]
    if any(k in text for k in critical):
        return {"decision": "ABRIR_TICKET", "urgencia": "ALTA", "campos_faltantes": []}
    if any(k in text for k in ticket):
        return {"decision": "ABRIR_TICKET", "urgencia": "MEDIA", "campos_faltantes": []}
    if len(text.split()) < 4 or text in vague:
        return {"decision": "PEDIR_INFO", "urgencia": "BAJA", "campos_faltantes": ["curso o servicio", "descripción del caso"]}
    return {"decision": "AUTO_RESOLVER", "urgencia": "BAJA", "campos_faltantes": []}
