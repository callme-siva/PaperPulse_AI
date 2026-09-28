from models import RawPaper, DebateTurn, RetrievedContext
from rag.llm_client import llm_client

class CriticalReviewerAgent:
    """Challenges baseline fairness, compute requirements, overfitting, and missing ablations."""
    
    def generate_critique(self, paper: RawPaper, advocate_claim: str) -> DebateTurn:
        grounding = [
            RetrievedContext(
                context_id=f"{paper.paper_id}#sec_limitations",
                paper_id=paper.paper_id,
                section_name="Baselines & Discussion",
                raw_latex_span="Comparative baseline selection across parameter-matched models",
                similarity_score=0.85,
                equations=[]
            )
        ]

        prompt = (
            f"You are the Critical Reviewer Agent reviewing '{paper.title}'.\n"
            f"The Author Advocate claimed:\n'{advocate_claim}'\n\n"
            f"Task: Present Round 1 Critique probing: 1. Baseline fairness; 2. Compute/GPU budget; 3. Overfitting or dataset contamination risks."
        )
        sys_prompt = "You are an expert ICLR/NeurIPS reviewer ensuring rigorous evaluation standards."
        arg_text = llm_client.generate(prompt, sys_prompt)
        
        return DebateTurn(
            turn_id=f"{paper.paper_id}_R1_CRI",
            paper_id=paper.paper_id,
            round_number=1,
            speaker="Critical Reviewer",
            argument_title="Baseline Fairness, Compute Overhead & Ablation Scrutiny",
            argument_text=arg_text,
            cited_section="Baselines & Discussion (Section 5)",
            key_quote="Need verification of equal FLOPs and parameter-matched comparisons.",
            grounding_contexts=grounding,
            cited_context_ids=[g.context_id for g in grounding]
        )

critic_agent = CriticalReviewerAgent()
