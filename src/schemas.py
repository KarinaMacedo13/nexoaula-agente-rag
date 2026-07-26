from __future__ import annotations

from typing import Literal, TypedDict

from pydantic import BaseModel, Field


class TriageOutput(BaseModel):
    decision: Literal["AUTO_RESOLVER", "PEDIR_INFO", "ABRIR_TICKET"]
    urgencia: Literal["BAJA", "MEDIA", "ALTA"]
    campos_faltantes: list[str] = Field(default_factory=list)


class Citation(BaseModel):
    source: str
    page: int | None = None
    section: str | None = None
    excerpt: str


class AgentState(TypedDict, total=False):
    pregunta: str
    triaje: dict
    respuesta: str
    citaciones: list[dict]
    rag_exito: bool
    accion_final: str
    ticket_id: str
