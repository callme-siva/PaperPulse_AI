from typing import List
import numpy as np

class LocalEmbeddingModel:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._model = None
        self._init_model()

    def _init_model(self):
        try:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(self.model_name)
        except Exception as e:
            print(f"[Embeddings] SentenceTransformer failed to load: {e}. Using deterministic fallback.")
            self._model = None

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        if self._model:
            try:
                embeddings = self._model.encode(texts, show_progress_bar=False, normalize_embeddings=True)
                return embeddings.tolist()
            except Exception:
                pass
        
        # Deterministic offline fallback (384-dim normalized vector)
        dim = 384
        result = []
        for t in texts:
            seed = sum(ord(c) for c in t) % 100000
            rng = np.random.RandomState(seed)
            vec = rng.randn(dim)
            vec = vec / np.linalg.norm(vec)
            result.append(vec.tolist())
        return result

    def embed_query(self, text: str) -> List[float]:
        return self.embed_documents([text])[0]

_embedding_instance = None

def get_embeddings_model() -> LocalEmbeddingModel:
    global _embedding_instance
    if _embedding_instance is None:
        _embedding_instance = LocalEmbeddingModel()
    return _embedding_instance
