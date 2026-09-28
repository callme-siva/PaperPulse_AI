from typing import List, Dict, Any
from models import RawPaper, DebateTurn, ReviewVerdict
from storage.db import db
from agents.advocate_agent import advocate_agent
from agents.critic_agent import critic_agent
from agents.meta_reviewer import meta_reviewer

class MultiAgentDebateEngine:
    """Orchestrates the 2-round cyclic debate loop between Advocate, Critic, and Meta-Reviewer."""
    
    def run_debate(self, paper: RawPaper) -> Dict[str, Any]:
        existing_turns = db.get_debate_turns(paper.paper_id)
        existing_review = db.get_review(paper.paper_id)
        
        if existing_turns and existing_review:
            return {
                "turns": existing_turns,
                "review": existing_review
            }

        turns: List[DebateTurn] = []

        # Round 1: Opening Claim (Advocate) -> Opening Critique (Critic)
        turn1 = advocate_agent.generate_opening_claim(paper)
        turns.append(turn1)
        db.save_debate_turn(turn1)

        turn2 = critic_agent.generate_critique(paper, turn1.argument_text)
        turns.append(turn2)
        db.save_debate_turn(turn2)

        # Round 2: Rebuttal (Advocate)
        turn3 = advocate_agent.generate_rebuttal(paper, turn2.argument_text)
        turns.append(turn3)
        db.save_debate_turn(turn3)

        # Meta-Review Verdict
        verdict = meta_reviewer.synthesize_verdict(paper, turns)
        db.save_review(verdict)

        return {
            "turns": [t.model_dump() if hasattr(t, "model_dump") else t.dict() for t in turns],
            "review": verdict.model_dump() if hasattr(verdict, "model_dump") else verdict.dict()
        }

debate_engine = MultiAgentDebateEngine()
