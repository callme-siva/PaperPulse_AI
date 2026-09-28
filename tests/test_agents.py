from unittest.mock import patch
from agents.advocate_agent import advocate_agent
from agents.critic_agent import critic_agent
from agents.meta_reviewer import meta_reviewer
from agents.debate_engine import MultiAgentDebateEngine
from models import RawPaper, DebateTurn

def test_author_advocate_agent(sample_paper):
    # Opening claim
    turn1 = advocate_agent.generate_opening_claim(sample_paper)
    assert turn1.speaker == "Author Advocate"
    assert turn1.round_number == 1
    assert len(turn1.grounding_contexts) >= 1
    assert turn1.grounding_contexts[0].raw_latex_span is not None
    assert len(turn1.argument_text) > 0

    # Rebuttal
    turn2 = advocate_agent.generate_rebuttal(sample_paper, "Baseline comparisons are flawed.")
    assert turn2.speaker == "Author Advocate"
    assert turn2.round_number == 2
    assert len(turn2.grounding_contexts) >= 1
    assert len(turn2.argument_text) > 0

def test_critical_reviewer_agent(sample_paper):
    critique_turn = critic_agent.generate_critique(sample_paper, "Our architecture achieves SOTA on all tasks.")
    assert critique_turn.speaker == "Critical Reviewer"
    assert critique_turn.round_number == 1
    assert len(critique_turn.grounding_contexts) >= 1
    assert len(critique_turn.argument_text) > 0

def test_meta_reviewer_synthesizer(sample_paper):
    turn1 = advocate_agent.generate_opening_claim(sample_paper)
    turn2 = critic_agent.generate_critique(sample_paper, turn1.argument_text)
    turn3 = advocate_agent.generate_rebuttal(sample_paper, turn2.argument_text)

    verdict = meta_reviewer.synthesize_verdict(sample_paper, [turn1, turn2, turn3])
    assert verdict.paper_id == sample_paper.paper_id
    assert 1.0 <= verdict.overall_score <= 10.0
    assert 1.0 <= verdict.novelty_score <= 10.0
    assert 1.0 <= verdict.rigor_score <= 10.0
    assert 1.0 <= verdict.baseline_fairness_score <= 10.0
    assert 1.0 <= verdict.reproducibility_score <= 10.0
    assert verdict.recommendation in ["Accept (Oral)", "Accept (Poster)", "Weak Accept", "Borderline / Revise", "Reject"]
    assert len(verdict.strengths) >= 1
    assert len(verdict.weaknesses) >= 1
    assert len(verdict.open_questions) >= 1

def test_debate_engine_full_run(temp_db, sample_paper):
    engine = MultiAgentDebateEngine()
    
    with patch("agents.debate_engine.db", temp_db):
        temp_db.save_paper(sample_paper)
        
        # Initial run executes 3 debate turns and generates 1 verdict
        res = engine.run_debate(sample_paper)
        assert "turns" in res
        assert "review" in res
        assert len(res["turns"]) == 3
        assert res["review"]["overall_score"] >= 1.0
        
        # Stored in DB
        db_turns = temp_db.get_debate_turns(sample_paper.paper_id)
        db_review = temp_db.get_review(sample_paper.paper_id)
        assert len(db_turns) == 3
        assert db_review is not None

        # Second run should load from cache / DB
        cached_res = engine.run_debate(sample_paper)
        assert len(cached_res["turns"]) == 3
        assert cached_res["review"]["verdict_id"] == db_review["verdict_id"]
