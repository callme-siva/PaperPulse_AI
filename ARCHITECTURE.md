# 🏗️ PaperPulse AI — System Architecture & Engineering Specifications

### Autonomous Multi-Agent Academic Paper Discovery, Adversarial Peer-Review & Lineage Graph

---

## 1. Executive Summary & Problem Formulation

Academic research in machine learning has reached a throughput exceeding 2,500 arXiv papers weekly. Standard LLM-based paper summarizers fail due to three fundamental limitations:
1. **Lossy PDF Parsing**: Multi-column PDF extractors scramble tables, math notations, and equations.
2. **Uncalibrated Hallucinations**: Standard chat models accept paper claims uncritically without probing baseline fairness or compute FLOPs.
3. **Missing Architectural Lineage**: Failure to trace conceptual ancestry across foundational precursors.

**PaperPulse AI** resolves this via a multi-agent peer-review architecture powered by **raw LaTeX extraction**, **cyclic adversarial debate**, and **interactive 2-hop citation DAGs**.

---

## 2. End-to-End System Architecture

```mermaid
flowchart TB
    subgraph Ingestion["1. Continuous Paper Sourcing"]
        ARX["📡 ArXiv API (cs.AI, cs.LG, cs.CL, cs.CV)"]
        TAR["📦 Raw LaTeX Tarball Extractor (.tar.gz)"]
        SEM["📚 Semantic Scholar API (Citation DAGs)"]
        ARX --> TAR
    end

    subgraph Parsing["2. Academic Parsing Core"]
        EQ_EXTRACT["Lossless Math Environment Extractor"]
        TABLE_EXTRACT["LaTeX Tabular Matrix Extractor"]
        METRIC_EXTRACT["Structured SOTA Benchmark Extractor"]
        TAR --> EQ_EXTRACT
        TAR --> TABLE_EXTRACT
        TAR --> METRIC_EXTRACT
    end

    subgraph Grounding["3. Verifiable Grounding & Retrieval Layer"]
        CTX["RetrievedContext Engine (chunk_id, span, LaTeX, score)"]
        EQ_EXTRACT --> CTX
        TABLE_EXTRACT --> CTX
    end

    subgraph Debate["4. Multi-Agent Peer-Review Arena"]
        ADV["🧑‍🔬 Author Advocate Agent (Novelty & Scaling)"]
        CRI["🕵️ Critical Reviewer Agent (Baselines & Compute)"]
        META["⚖️ Area Chair Meta-Reviewer (4-Axis Rubric)"]
        
        CTX --> ADV
        CTX --> CRI
        ADV <--> CRI
        ADV --> META
        CRI --> META
    end

    subgraph Storage["5. Dual-Store Persistence"]
        VDB[("ChromaDB Vector Store (Chunks + Math)")]
        SQL[("SQLite Database (Papers, Metrics, Debates, Reviews)")]
        DAG_STORE[("NetworkX Citation DAG (2-Hop Radius)")]
    end

    subgraph UI["6. Streamlit Research Studio"]
        STUDIO["🖥️ Interactive UI (Radar Charts, Debate Player, Lineage Graph)"]
    end

    Debate --> Storage
    Storage --> UI
```

---

## 3. Mathematical Formulations & Multi-Agent State Machine

### A. Provenance Grounding Scoring
For each argument $A_t$ generated at round $t$, a set of verifiable grounding contexts $C = \{c_1, c_2, \dots, c_k\}$ is retrieved such that:

$$\text{Sim}(A_t, c_i) = \frac{\mathbf{e}(A_t) \cdot \mathbf{e}(c_i)}{\|\mathbf{e}(A_t)\| \|\mathbf{e}(c_i)\|} \ge \tau_{\text{sim}}$$

Where $\mathbf{e}(\cdot)$ represents the 384-dimensional dense embedding space (`sentence-transformers/all-MiniLM-L6-v2`) and $\tau_{\text{sim}} = 0.35$ represents the minimum factual relevance threshold.

### B. Calibrated 4-Axis Rubric Formulation
The Area Chair Meta-Reviewer computes the final verdict using a weighted multi-axis rubric:

$$\text{Overall Score} = \frac{1}{4} \left( S_{\text{novelty}} + S_{\text{rigor}} + S_{\text{fairness}} + S_{\text{reproducibility}} \right)$$

* $S_{\text{novelty}} \in [1.0, 10.0]$: Mathematical originality and theoretical framing.
* $S_{\text{rigor}} \in [1.0, 10.0]$: Empirical dataset coverage and statistical confidence.
* $S_{\text{fairness}} \in [1.0, 10.0]$: Baseline parity across parameter and FLOP budgets.
* $S_{\text{reproducibility}} \in [1.0, 10.0]$: Open-source code availability, weights, and hyperparameter disclosure.

---

*PaperPulse AI — System Architecture Specification.*
