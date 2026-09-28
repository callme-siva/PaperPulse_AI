from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class RetrievedContext(BaseModel):
    """Verifiable grounding context retrieved from the paper's LaTeX/PDF source."""
    context_id: str
    paper_id: str
    section_name: str
    raw_latex_span: str
    similarity_score: float = 0.0
    equations: List[str] = Field(default_factory=list)

class RawPaper(BaseModel):
    """Represents an academic paper ingested from arXiv / Semantic Scholar."""
    paper_id: str
    title: str
    authors: List[str] = Field(default_factory=list)
    abstract: str
    categories: List[str] = Field(default_factory=list)
    primary_category: str = "cs.AI"
    published_date: str
    arxiv_url: str
    pdf_url: str
    latex_source_url: Optional[str] = None
    github_url: Optional[str] = None
    citation_count: int = 0
    has_latex_source: bool = False
    latex_content: Optional[str] = None
    equations: List[str] = Field(default_factory=list)
    tables: List[Dict[str, Any]] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())

class ExtractedMetric(BaseModel):
    """Structured SOTA benchmark or empirical result extracted from the paper."""
    metric_id: str
    paper_id: str
    dataset_name: str
    metric_name: str = "Accuracy"
    paper_score: float
    baseline_name: Optional[str] = None
    baseline_score: Optional[float] = None
    delta: Optional[float] = None
    compute_claim: Optional[str] = None
    source_context_id: Optional[str] = None
    source_latex_span: Optional[str] = None

class DebateTurn(BaseModel):
    """Single argument turn in the multi-agent peer-review debate with provable grounding."""
    turn_id: str
    paper_id: str
    round_number: int
    speaker: str  # "Author Advocate" | "Critical Reviewer"
    argument_title: str
    argument_text: str
    cited_section: Optional[str] = None
    key_quote: Optional[str] = None
    grounding_contexts: List[RetrievedContext] = Field(default_factory=list)
    cited_context_ids: List[str] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

class ReviewVerdict(BaseModel):
    """Calibrated multi-axis rubric verdict issued by the Meta-Reviewer Synthesizer."""
    verdict_id: str
    paper_id: str
    overall_score: float = Field(ge=1.0, le=10.0)
    novelty_score: float = Field(ge=1.0, le=10.0)
    rigor_score: float = Field(ge=1.0, le=10.0)
    baseline_fairness_score: float = Field(ge=1.0, le=10.0)
    reproducibility_score: float = Field(ge=1.0, le=10.0)
    recommendation: str  # "Accept (Oral)", "Accept (Poster)", "Weak Accept", "Borderline / Revise", "Reject"
    executive_summary: str
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    open_questions: List[str] = Field(default_factory=list)
    generated_at: str = Field(default_factory=lambda: datetime.now().isoformat())

class CitationNode(BaseModel):
    """Node in the citation and concept evolution DAG."""
    node_id: str
    title: str
    authors: str
    year: int
    citations: int = 0
    is_seed: bool = False
    hop_distance: int = 0
    group: str = "ai_architecture"

class PaperChunk(BaseModel):
    """Hierarchical document chunk for equation-preserving RAG."""
    chunk_id: str
    paper_id: str
    section_name: str
    text: str
    equations: List[str] = Field(default_factory=list)
    token_count: int = 0
    
    def to_metadata(self) -> Dict[str, Any]:
        return {
            "chunk_id": self.chunk_id,
            "paper_id": self.paper_id,
            "section_name": self.section_name,
            "has_equations": len(self.equations) > 0,
            "token_count": self.token_count
        }
