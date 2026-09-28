import pytest
from pydantic import ValidationError
from models import (
    RetrievedContext,
    RawPaper,
    ExtractedMetric,
    DebateTurn,
    ReviewVerdict,
    CitationNode,
    PaperChunk
)

def test_retrieved_context():
    ctx = RetrievedContext(
        context_id="ctx_1",
        paper_id="2312.00752",
        section_name="Methodology",
        raw_latex_span="h_t = A h_{t-1} + B x_t",
        similarity_score=0.91,
        equations=["h_t = A h_{t-1} + B x_t"]
    )
    assert ctx.context_id == "ctx_1"
    assert ctx.similarity_score == 0.91
    assert len(ctx.equations) == 1

def test_raw_paper_defaults(sample_paper):
    assert sample_paper.paper_id == "2312.00752"
    assert len(sample_paper.authors) == 2
    assert sample_paper.has_latex_source is True
    assert sample_paper.primary_category == "cs.LG"
    assert len(sample_paper.equations) == 2
    assert sample_paper.created_at is not None

def test_extracted_metric(sample_metric):
    assert sample_metric.metric_id == "2312.00752_MMLU"
    assert sample_metric.paper_score == 86.4
    assert sample_metric.baseline_score == 83.2
    assert sample_metric.delta == 3.2

def test_debate_turn(sample_paper):
    ctx = RetrievedContext(
        context_id="ctx_1",
        paper_id=sample_paper.paper_id,
        section_name="Methodology",
        raw_latex_span="eq1"
    )
    turn = DebateTurn(
        turn_id="turn_01",
        paper_id=sample_paper.paper_id,
        round_number=1,
        speaker="Author Advocate",
        argument_title="Novelty claim",
        argument_text="We introduce selective state spaces.",
        grounding_contexts=[ctx],
        cited_context_ids=["ctx_1"]
    )
    assert turn.turn_id == "turn_01"
    assert turn.speaker == "Author Advocate"
    assert len(turn.grounding_contexts) == 1
    assert turn.cited_context_ids == ["ctx_1"]

def test_review_verdict_bounds():
    verdict = ReviewVerdict(
        verdict_id="verdict_01",
        paper_id="2312.00752",
        overall_score=8.5,
        novelty_score=9.0,
        rigor_score=8.0,
        baseline_fairness_score=8.5,
        reproducibility_score=8.5,
        recommendation="Accept (Oral)",
        executive_summary="Solid paper with strong empirical validation.",
        strengths=["Novel math", "Fast GPU scan"],
        weaknesses=["Language only"],
        open_questions=["Generalization?"]
    )
    assert verdict.overall_score == 8.5
    assert verdict.recommendation == "Accept (Oral)"
    assert len(verdict.strengths) == 2

def test_review_verdict_out_of_bounds():
    with pytest.raises(ValidationError):
        ReviewVerdict(
            verdict_id="verdict_invalid",
            paper_id="2312.00752",
            overall_score=11.5,  # Invalid: > 10.0
            novelty_score=9.0,
            rigor_score=8.0,
            baseline_fairness_score=8.5,
            reproducibility_score=8.5,
            recommendation="Accept",
            executive_summary="Invalid score test"
        )

def test_paper_chunk_to_metadata():
    chunk = PaperChunk(
        chunk_id="chk_01",
        paper_id="2312.00752",
        section_name="Introduction",
        text="State space models are promising...",
        equations=["h_t = Ax_t"],
        token_count=120
    )
    meta = chunk.to_metadata()
    assert meta["chunk_id"] == "chk_01"
    assert meta["paper_id"] == "2312.00752"
    assert meta["has_equations"] is True
    assert meta["token_count"] == 120

def test_citation_node():
    node = CitationNode(
        node_id="Transformer_2017",
        title="Attention Is All You Need",
        authors="Vaswani et al.",
        year=2017,
        citations=125000,
        is_seed=False,
        hop_distance=2
    )
    assert node.node_id == "Transformer_2017"
    assert node.year == 2017
    assert node.citations == 125000
