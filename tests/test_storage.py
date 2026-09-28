import pytest
from models import RawPaper, ExtractedMetric, DebateTurn, ReviewVerdict, RetrievedContext

def test_paper_crud(temp_db, sample_paper):
    # Save paper
    success = temp_db.save_paper(sample_paper)
    assert success is True

    # Retrieve paper
    retrieved = temp_db.get_paper(sample_paper.paper_id)
    assert retrieved is not None
    assert retrieved["paper_id"] == sample_paper.paper_id
    assert retrieved["title"] == sample_paper.title
    assert retrieved["authors"] == sample_paper.authors
    assert retrieved["categories"] == sample_paper.categories
    assert retrieved["equations"] == sample_paper.equations
    assert retrieved["has_latex_source"] == 1

    # Non-existent paper
    assert temp_db.get_paper("non_existent_id") is None

    # Get all papers with and without category filter
    all_papers = temp_db.get_all_papers()
    assert len(all_papers) == 1

    cs_lg_papers = temp_db.get_all_papers(category="cs.LG")
    assert len(cs_lg_papers) == 1

    cs_cv_papers = temp_db.get_all_papers(category="cs.CV")
    assert len(cs_cv_papers) == 0

def test_metric_crud(temp_db, sample_paper, sample_metric):
    temp_db.save_paper(sample_paper)
    success = temp_db.save_metric(sample_metric)
    assert success is True

    paper_metrics = temp_db.get_metrics_for_paper(sample_paper.paper_id)
    assert len(paper_metrics) == 1
    assert paper_metrics[0]["dataset_name"] == "MMLU"
    assert paper_metrics[0]["paper_score"] == 86.4

    all_metrics = temp_db.get_all_metrics()
    assert len(all_metrics) == 1
    assert all_metrics[0]["paper_title"] == sample_paper.title

def test_debate_turn_crud(temp_db, sample_paper):
    temp_db.save_paper(sample_paper)
    ctx = RetrievedContext(
        context_id="ctx_methodology",
        paper_id=sample_paper.paper_id,
        section_name="Methodology",
        raw_latex_span="h_t = A h_{t-1} + B x_t",
        similarity_score=0.92,
        equations=["eq1"]
    )
    turn = DebateTurn(
        turn_id="turn_r1_adv",
        paper_id=sample_paper.paper_id,
        round_number=1,
        speaker="Author Advocate",
        argument_title="Opening Claim",
        argument_text="Selective SSMs provide linear scaling.",
        cited_section="Methodology (Sec 3)",
        key_quote="Linear-time scaling",
        grounding_contexts=[ctx],
        cited_context_ids=["ctx_methodology"]
    )
    success = temp_db.save_debate_turn(turn)
    assert success is True

    turns = temp_db.get_debate_turns(sample_paper.paper_id)
    assert len(turns) == 1
    assert turns[0]["turn_id"] == "turn_r1_adv"
    assert turns[0]["speaker"] == "Author Advocate"
    assert len(turns[0]["grounding_contexts"]) == 1
    assert turns[0]["grounding_contexts"][0]["context_id"] == "ctx_methodology"
    assert turns[0]["cited_context_ids"] == ["ctx_methodology"]

def test_review_verdict_crud(temp_db, sample_paper):
    temp_db.save_paper(sample_paper)
    verdict = ReviewVerdict(
        verdict_id="verdict_01",
        paper_id=sample_paper.paper_id,
        overall_score=8.8,
        novelty_score=9.2,
        rigor_score=8.5,
        baseline_fairness_score=8.7,
        reproducibility_score=8.8,
        recommendation="Accept (Oral)",
        executive_summary="Excellent algorithmic speedup and mathematical formulation.",
        strengths=["Linear scaling", "Kernel fusion"],
        weaknesses=["Requires custom CUDA scan"],
        open_questions=["Non-causal generalization?"]
    )
    success = temp_db.save_review(verdict)
    assert success is True

    retrieved_verdict = temp_db.get_review(sample_paper.paper_id)
    assert retrieved_verdict is not None
    assert retrieved_verdict["overall_score"] == 8.8
    assert retrieved_verdict["recommendation"] == "Accept (Oral)"
    assert len(retrieved_verdict["strengths"]) == 2
    assert "Linear scaling" in retrieved_verdict["strengths"]
    assert len(retrieved_verdict["weaknesses"]) == 1
    assert len(retrieved_verdict["open_questions"]) == 1

def test_clear_all(temp_db, sample_paper, sample_metric):
    temp_db.save_paper(sample_paper)
    temp_db.save_metric(sample_metric)
    assert len(temp_db.get_all_papers()) == 1
    assert len(temp_db.get_all_metrics()) == 1

    temp_db.clear_all()
    assert len(temp_db.get_all_papers()) == 0
    assert len(temp_db.get_all_metrics()) == 0
