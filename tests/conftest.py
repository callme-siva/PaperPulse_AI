import sys
import os
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
import tempfile
from models import RawPaper, ExtractedMetric, RetrievedContext, DebateTurn, ReviewVerdict, PaperChunk
from storage.db import AcademicDatabase
from rag.vector_store import PaperVectorStore

@pytest.fixture
def temp_db():
    """Provides an isolated temporary SQLite database for testing."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        temp_path = f.name
    
    db_instance = AcademicDatabase(db_path=temp_path)
    yield db_instance
    
    # Cleanup
    if os.path.exists(temp_path):
        try:
            os.remove(temp_path)
        except Exception:
            pass

@pytest.fixture
def temp_chroma_store():
    """Provides an isolated Chroma vector store in a temporary directory."""
    temp_dir = tempfile.mkdtemp()
    store = PaperVectorStore(persist_dir=temp_dir, collection_name="test_collection")
    yield store
    # Cleanup
    import shutil
    try:
        shutil.rmtree(temp_dir)
    except Exception:
        pass

@pytest.fixture
def sample_paper():
    """Sample RawPaper instance for tests."""
    return RawPaper(
        paper_id="2312.00752",
        title="Mamba: Linear-Time Sequence Modeling with Selective State Spaces",
        authors=["Albert Gu", "Tri Dao"],
        abstract="Foundation models are now powering most of the exciting applications in deep learning. We introduce Mamba, a selective state space model.",
        categories=["cs.LG", "cs.AI"],
        primary_category="cs.LG",
        published_date="2023-12-01",
        arxiv_url="https://arxiv.org/abs/2312.00752",
        pdf_url="https://arxiv.org/pdf/2312.00752.pdf",
        github_url="https://github.com/state-spaces/mamba",
        citation_count=1840,
        has_latex_source=True,
        equations=[
            r"h_t = \bar{A} h_{t-1} + \bar{B} x_t",
            r"y_t = C h_t + D x_t"
        ]
    )

@pytest.fixture
def sample_metric():
    """Sample ExtractedMetric instance for tests."""
    return ExtractedMetric(
        metric_id="2312.00752_MMLU",
        paper_id="2312.00752",
        dataset_name="MMLU",
        metric_name="Accuracy / Score",
        paper_score=86.4,
        baseline_name="Previous SOTA",
        baseline_score=83.2,
        delta=3.2,
        compute_claim="Extracted from Abstract / Results"
    )
