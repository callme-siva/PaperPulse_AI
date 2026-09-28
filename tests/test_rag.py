import numpy as np
from rag.embeddings import LocalEmbeddingModel, get_embeddings_model
from rag.llm_client import LLMClient
from models import PaperChunk

def test_local_embedding_model():
    model = LocalEmbeddingModel()
    texts = ["Attention is all you need.", "State space models are fast."]
    embeddings = model.embed_documents(texts)
    
    assert len(embeddings) == 2
    assert len(embeddings[0]) == 384
    assert len(embeddings[1]) == 384
    
    # Verify vectors are normalized (L2 norm ≈ 1.0)
    norm0 = np.linalg.norm(embeddings[0])
    norm1 = np.linalg.norm(embeddings[1])
    assert abs(norm0 - 1.0) < 1e-4
    assert abs(norm1 - 1.0) < 1e-4

def test_embed_query():
    model = LocalEmbeddingModel()
    emb = model.embed_query("Transformer architecture")
    assert len(emb) == 384
    assert abs(np.linalg.norm(emb) - 1.0) < 1e-4

def test_vector_store_operations(temp_chroma_store):
    chunks = [
        PaperChunk(
            chunk_id="chunk_1",
            paper_id="paper_a",
            section_name="Methodology",
            text="We propose linear attention with sub-quadratic memory.",
            equations=["eq1"],
            token_count=10
        ),
        PaperChunk(
            chunk_id="chunk_2",
            paper_id="paper_b",
            section_name="Experiments",
            text="Image classification results on ImageNet dataset.",
            token_count=8
        )
    ]
    
    added_count = temp_chroma_store.add_paper_chunks(chunks)
    assert added_count == 2
    assert temp_chroma_store.get_total_chunks() == 2

    # Query without filter
    results = temp_chroma_store.query_similar_sections("linear attention sub-quadratic", n_results=2)
    assert len(results) >= 1
    assert "text" in results[0]
    assert "similarity" in results[0]

    # Query with paper_id filter
    filtered_results = temp_chroma_store.query_similar_sections(
        "results",
        n_results=2,
        paper_id="paper_b"
    )
    assert len(filtered_results) >= 1
    assert all(r["metadata"]["paper_id"] == "paper_b" for r in filtered_results)

    # Clear vector store
    temp_chroma_store.clear()
    assert temp_chroma_store.get_total_chunks() == 0

def test_llm_client_offline_deterministic():
    client = LLMClient()
    
    # Advocate prompt
    adv_resp = client._offline_deterministic_response("Advocate claim for paper")
    assert "Theoretical & Empirical Novelty" in adv_resp
    assert "quadratic" in adv_resp
    
    # Critic prompt
    cri_resp = client._offline_deterministic_response("Critic review for paper")
    assert "Methodological Concerns & Baseline Fairness" in cri_resp
    assert "compute budget" in cri_resp
    
    # Meta-Review prompt
    meta_resp = client._offline_deterministic_response("Synthesize meta-review")
    assert "Meta-Review Summary" in meta_resp
    assert "Accept (Oral)" in meta_resp

def test_llm_generate_without_keys():
    client = LLMClient()
    # When no external API keys are configured or mock fails, fallback is used
    res = client.generate("Advocate round 1 argument")
    assert len(res) > 0
