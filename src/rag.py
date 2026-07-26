from __future__ import annotations

from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

from .config import Settings
from .documents import load_documents, split_documents

SYSTEM_PROMPT = """
Eres Nexo, el asistente de la plataforma educativa NexoAula.
Responde únicamente con información respaldada por el contexto recuperado.
No inventes requisitos, plazos, porcentajes, precios ni excepciones.
Si el contexto no contiene una respuesta suficiente, responde exactamente:
"No encontré esa información en los documentos disponibles."
Usa español claro, empieza con una respuesta directa y luego explica los detalles.
Cuando existan condiciones acumulativas, enuméralas sin omitir ninguna.
No presentes el contenido como asesoría legal.
""".strip()


class RAGService:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=settings.embedding_model, google_api_key=settings.api_key
        )
        self.llm = ChatGoogleGenerativeAI(
            model=settings.chat_model, temperature=0, google_api_key=settings.api_key
        )
        self.vectorstore = self._load_or_build_index()
        self.retriever = self.vectorstore.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"score_threshold": settings.score_threshold, "k": settings.top_k},
        )

    def _load_or_build_index(self) -> FAISS:
        index_file = self.settings.index_dir / "index.faiss"
        if index_file.exists():
            return FAISS.load_local(
                str(self.settings.index_dir),
                self.embeddings,
                allow_dangerous_deserialization=True,
            )
        docs = split_documents(load_documents(self.settings.docs_dir))
        store = FAISS.from_documents(docs, self.embeddings)
        self.settings.index_dir.mkdir(parents=True, exist_ok=True)
        store.save_local(str(self.settings.index_dir))
        return store

    @staticmethod
    def _citation(doc) -> dict:
        excerpt = " ".join(doc.page_content.split())
        if len(excerpt) > 420:
            excerpt = excerpt[:417].rstrip() + "..."
        return {
            "source": doc.metadata.get("source", Path(doc.metadata.get("source_path", "documento")).name),
            "page": doc.metadata.get("page_display"),
            "section": doc.metadata.get("section"),
            "excerpt": excerpt,
        }

    def answer(self, question: str) -> dict:
        docs = self.retriever.invoke(question)
        if not docs:
            return {
                "respuesta": "No encontré esa información en los documentos disponibles.",
                "citaciones": [],
                "documentos_encontrados": False,
            }
        context_parts = []
        for i, doc in enumerate(docs, 1):
            source = doc.metadata.get("source", "documento")
            page = doc.metadata.get("page_display")
            locator = f"{source}, página {page}" if page else source
            context_parts.append(f"[FUENTE {i}: {locator}]\n{doc.page_content}")
        context = "\n\n".join(context_parts)
        response = self.llm.invoke([
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=f"CONTEXTO:\n\n{context}\n\nPREGUNTA: {question}"),
        ])
        answer = response.content.strip()
        failed = answer.startswith("No encontré esa información")
        return {
            "respuesta": answer,
            "citaciones": [] if failed else [self._citation(d) for d in docs],
            "documentos_encontrados": not failed,
        }
