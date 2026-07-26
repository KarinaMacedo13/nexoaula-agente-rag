from __future__ import annotations

from pathlib import Path

from langchain_community.document_loaders import CSVLoader, PyMuPDFLoader, TextLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

SUPPORTED = {".pdf", ".csv", ".md", ".txt"}


def load_documents(directory: Path) -> list[Document]:
    documents: list[Document] = []
    for path in sorted(directory.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED:
            continue
        try:
            if path.suffix.lower() == ".pdf":
                loaded = PyMuPDFLoader(str(path)).load()
            elif path.suffix.lower() == ".csv":
                loaded = CSVLoader(str(path), encoding="utf-8").load()
            else:
                loaded = TextLoader(str(path), encoding="utf-8").load()
            for doc in loaded:
                doc.metadata["source"] = path.name
                doc.metadata["source_path"] = str(path)
                if "page" in doc.metadata:
                    doc.metadata["page_display"] = int(doc.metadata["page"]) + 1
            documents.extend(loaded)
        except Exception as exc:
            raise RuntimeError(f"No se pudo cargar {path.name}: {exc}") from exc
    if not documents:
        raise ValueError(f"No se encontraron documentos compatibles en {directory}")
    return documents


def split_documents(documents: list[Document]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=150,
        separators=["\n## ", "\n# ", "\n\n", "\n", ". ", " "],
    )
    return splitter.split_documents(documents)
