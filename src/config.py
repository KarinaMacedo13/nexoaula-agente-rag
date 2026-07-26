from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    api_key: str = os.getenv("GEMINI_API_KEY", "")
    chat_model: str = os.getenv("GEMINI_CHAT_MODEL", "gemini-2.5-flash")
    embedding_model: str = os.getenv("GEMINI_EMBEDDING_MODEL", "models/gemini-embedding-001")
    docs_dir: Path = Path(os.getenv("DOCS_DIR", "docs/knowledge_base"))
    index_dir: Path = Path(os.getenv("INDEX_DIR", "data/index"))
    top_k: int = int(os.getenv("TOP_K", "5"))
    score_threshold: float = float(os.getenv("SCORE_THRESHOLD", "0.30"))
    log_file: Path = Path(os.getenv("LOG_FILE", "data/agent_logs.jsonl"))

    def validate(self) -> None:
        if not self.api_key or self.api_key == "coloca_tu_clave_aqui":
            raise ValueError("Falta GEMINI_API_KEY. Copia .env.example como .env y agrega una clave válida.")
        if not self.docs_dir.exists():
            raise FileNotFoundError(f"No existe el directorio de documentos: {self.docs_dir}")
