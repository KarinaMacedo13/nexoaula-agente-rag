from __future__ import annotations

import streamlit as st

from src.agent import NexoAulaAgent
from src.config import Settings

st.set_page_config(page_title="NexoAula | Asistente", page_icon="🎓", layout="wide")

CUSTOM_CSS = """
<style>
.block-container {max-width: 1050px; padding-top: 1.8rem;}
[data-testid="stSidebar"] {background: #f8fafc;}
.nexo-card {padding: 1rem 1.1rem; border: 1px solid #cbd5e1; border-radius: 14px; background: white;}
.source {font-size: .88rem; color: #475569;}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

@st.cache_resource(show_spinner="Preparando la base de conocimiento...")
def get_agent():
    return NexoAulaAgent(Settings())

with st.sidebar:
    st.image("assets/logo_nexoaula.png", use_container_width=True)
    st.markdown("**Asistente documental con RAG**")
    st.caption("Responde con base en políticas oficiales y muestra sus fuentes.")
    st.divider()
    st.markdown("Ejemplos")
    examples = [
        "¿Qué necesito para obtener el certificado?",
        "¿Cuándo puedo pedir un reembolso?",
        "¿Cuál es la comisión de afiliados?",
        "¿Puedo usar IA en mis tareas?",
    ]
    for ex in examples:
        if st.button(ex, use_container_width=True):
            st.session_state["pending_question"] = ex

st.title("Nexo, tu asistente de NexoAula")
st.write("Consulta sobre cursos, certificados, reembolsos, uso de la plataforma, becas y afiliados.")
st.info("Nexo es un agente de IA. Verifica las fuentes mostradas antes de tomar una decisión importante.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("Fuentes consultadas"):
                for c in msg["sources"]:
                    page = f", página {c['page']}" if c.get("page") else ""
                    st.markdown(f"**{c['source']}{page}**")
                    st.caption(c["excerpt"])

question = st.session_state.pop("pending_question", None) or st.chat_input("Escribe tu pregunta")
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        try:
            with st.spinner("Buscando en los documentos..."):
                result = get_agent().invoke(question)
            st.markdown(result["respuesta"])
            if result.get("citaciones"):
                with st.expander("Fuentes consultadas", expanded=True):
                    for c in result["citaciones"]:
                        page = f", página {c['page']}" if c.get("page") else ""
                        st.markdown(f"**{c['source']}{page}**")
                        st.caption(c["excerpt"])
            st.caption(f"Acción del flujo: {result.get('accion_final', 'N/D')}")
            st.session_state.messages.append({
                "role": "assistant", "content": result["respuesta"], "sources": result.get("citaciones", [])
            })
        except Exception as exc:
            st.error(str(exc))
            st.code("cp .env.example .env\n# Edita .env y agrega GEMINI_API_KEY\nstreamlit run app.py")
