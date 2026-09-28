from models import RawPaper, DebateTurn
from rag.llm_client import llm_client

class CriticalReviewerAgent:
    """Challenges baseline fairness, compute requirements, overfitting, and missing ablations."""
    
    def generate_critique(self, paper: RawPaper, advocate_claim: str) -> DebateTurn:
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
            cited_section="Experimental Baselines & Limitations",
            key_quote="Need verification of equal FLOPs and parameter-matched comparisons."
        )

critic_agent = CriticalReviewerAgent()
