from src.config import Settings
from src.rag import RAGService

if __name__ == "__main__":
    settings = Settings()
    settings.validate()
    RAGService(settings)
    print(f"Índice creado o cargado en: {settings.index_dir}")
