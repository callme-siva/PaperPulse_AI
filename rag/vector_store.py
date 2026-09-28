import chromadb
from typing import List, Dict, Any, Optional
from config import CHROMA_DIR
from models import PaperChunk
from rag.embeddings import get_embeddings_model

class PaperVectorStore:
    def __init__(self, persist_dir=CHROMA_DIR, collection_name="paperpulse_chunks"):
        self.persist_dir = str(persist_dir)
        self.collection_name = collection_name
        self.embeddings_model = get_embeddings_model()
        self.client = chromadb.PersistentClient(path=self.persist_dir)
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def add_paper_chunks(self, chunks: List[PaperChunk]) -> int:
        if not chunks:
            return 0
        ids = [c.chunk_id for c in chunks]
        documents = [c.text for c in chunks]
        metadatas = [c.to_metadata() for c in chunks]
        try:
            embeddings = self.embeddings_model.embed_documents(documents)
            self.collection.upsert(
                ids=ids,
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas
            )
            return len(ids)
        except Exception as e:
            print(f"[VectorStore Error] add_paper_chunks failed: {e}")
            return 0

    def query_similar_sections(self, query_text: str, n_results: int = 5, paper_id: Optional[str] = None) -> List[Dict[str, Any]]:
        where_clause = {"paper_id": paper_id} if paper_id else None
        try:
            query_emb = self.embeddings_model.embed_query(query_text)
            results = self.collection.query(
                query_embeddings=[query_emb],
                n_results=n_results,
                where=where_clause,
                include=["documents", "metadatas", "distances"]
            )
            retrieved = []
            if results and results.get("ids") and results["ids"][0]:
                for i in range(len(results["ids"][0])):
                    dist = results["distances"][0][i] if results.get("distances") else 0.5
                    sim = max(0.0, min(1.0, 1.0 - dist))
                    retrieved.append({
                        "id": results["ids"][0][i],
                        "text": results["documents"][0][i],
                        "metadata": results["metadatas"][0][i],
                        "similarity": sim
                    })
            return retrieved
        except Exception as e:
            print(f"[VectorStore Error] query failed: {e}")
            return []

    def get_total_chunks(self) -> int:
        return self.collection.count()

    def clear(self):
        try:
            self.client.delete_collection(self.collection_name)
        except Exception:
            pass
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )

paper_vector_store = PaperVectorStore()
