from __future__ import annotations

import uuid

from langgraph.graph import END, START, StateGraph

from .config import Settings
from .logging_utils import append_log
from .rag import RAGService
from .schemas import AgentState
from .triage import TriageService


class NexoAulaAgent:
    def __init__(self, settings: Settings | None = None):
        self.settings = settings or Settings()
        self.settings.validate()
        self.triage = TriageService(self.settings)
        self.rag = RAGService(self.settings)
        self.graph = self._build_graph()

    def _build_graph(self):
        workflow = StateGraph(AgentState)
        workflow.add_node("triaje", self._node_triage)
        workflow.add_node("auto_resolver", self._node_rag)
        workflow.add_node("pedir_info", self._node_ask_info)
        workflow.add_node("abrir_ticket", self._node_ticket)
        workflow.add_edge(START, "triaje")
        workflow.add_conditional_edges("triaje", self._route_triage, {
            "rag": "auto_resolver", "info": "pedir_info", "ticket": "abrir_ticket"
        })
        workflow.add_conditional_edges("auto_resolver", self._route_rag, {
            "ok": END, "info": "pedir_info", "ticket": "abrir_ticket"
        })
        workflow.add_edge("pedir_info", END)
        workflow.add_edge("abrir_ticket", END)
        return workflow.compile()

    def _node_triage(self, state: AgentState) -> AgentState:
        return {"triaje": self.triage.classify(state["pregunta"])}

    def _node_rag(self, state: AgentState) -> AgentState:
        result = self.rag.answer(state["pregunta"])
        update: AgentState = {
            "respuesta": result["respuesta"],
            "citaciones": result["citaciones"],
            "rag_exito": result["documentos_encontrados"],
        }
        if result["documentos_encontrados"]:
            update["accion_final"] = "AUTO_RESOLVER"
        return update

    @staticmethod
    def _node_ask_info(state: AgentState) -> AgentState:
        missing = state.get("triaje", {}).get("campos_faltantes") or ["curso o servicio", "descripción concreta"]
        return {
            "respuesta": "Necesito un poco más de información: " + ", ".join(missing) + ". No incluyas contraseñas ni datos bancarios completos.",
            "citaciones": [],
            "accion_final": "PEDIR_INFO",
        }

    @staticmethod
    def _node_ticket(state: AgentState) -> AgentState:
        ticket_id = "NX-" + uuid.uuid4().hex[:8].upper()
        urgency = state.get("triaje", {}).get("urgencia", "MEDIA")
        return {
            "respuesta": f"Tu caso requiere revisión humana. Se generó la referencia {ticket_id} con urgencia {urgency}. Envía el detalle y evidencia a soporte@nexoaula.example.",
            "citaciones": [],
            "accion_final": "ABRIR_TICKET",
            "ticket_id": ticket_id,
        }

    @staticmethod
    def _route_triage(state: AgentState) -> str:
        decision = state["triaje"]["decision"]
        return {"AUTO_RESOLVER": "rag", "PEDIR_INFO": "info", "ABRIR_TICKET": "ticket"}[decision]

    @staticmethod
    def _route_rag(state: AgentState) -> str:
        if state.get("rag_exito"):
            return "ok"
        text = state["pregunta"].lower()
        human_keywords = ["reembolso", "cobro", "certificado", "cuenta", "acceso", "denuncia", "excepción"]
        return "ticket" if any(k in text for k in human_keywords) else "info"

    def invoke(self, question: str) -> dict:
        result = self.graph.invoke({"pregunta": question})
        append_log(self.settings.log_file, {
            "question": question,
            "action": result.get("accion_final"),
            "answer": result.get("respuesta"),
            "sources": [c.get("source") for c in result.get("citaciones", [])],
        })
        return result
