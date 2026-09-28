# 🛠️ PaperPulse AI — Operations & Maintenance Runbook

### Storage Lifecycle, Offline Resilience, and Sourcing Guidelines

---

## 1. Storage Architecture & Footprint

| Storage Component | Path | Typical Size (1,000 Papers) | Maintenance Action |
| :--- | :--- | :--- | :---: |
| **SQLite Store** | `data/paperpulse.db` | $\approx 2.5\text{ MB}$ | None (Indexed auto-upserts) |
| **ChromaDB Store** | `data/chroma_db/` | $\approx 4.0\text{ MB}$ | None (Local dense collection) |
| **LaTeX Downloads** | `data/downloads/` | Ephemeral | Auto-cleaned after parsing |

---

## 2. Maintenance Cheat Sheet

### A. Storage Purge / Reset
```bash
python3 -c "from storage.db import db; from rag.vector_store import paper_vector_store; db.clear_all(); paper_vector_store.clear(); print('✓ Storage cleared successfully.')"
```

### B. Run Verification Smoke Test
```bash
python3 -c "from storage.db import db; from ingestion.arxiv_client import arxiv_client; papers = arxiv_client.fetch_recent_papers('cs.AI', 2); print('✓ Verified:', len(papers), 'papers')"
```

---

## 3. Multi-Provider API Key Fallback Chain
* **Google Gemini 2.5 Flash** (Primary Cloud LLM)
* **OpenAI GPT-4o-mini** (Secondary Cloud LLM)
* **Groq Llama 3 70B** (High-Speed Open Weights)
* **Offline Deterministic Mode** (100% Zero-Cost Local Evaluation for CI/CD)

---

*PaperPulse AI Operations Runbook.*
