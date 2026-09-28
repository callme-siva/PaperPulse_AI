from models import RawPaper, DebateTurn
from rag.llm_client import llm_client

class AuthorAdvocateAgent:
    """Argues in favor of the paper's novelty, mathematical rigor, and empirical breakthroughs."""
    
    def generate_opening_claim(self, paper: RawPaper) -> DebateTurn:
        prompt = (
            f"You are the Author Advocate Agent representing the paper '{paper.title}'.\n"
            f"Authors: {', '.join(paper.authors)}\n"
            f"Abstract: {paper.abstract}\n"
            f"Equations: {paper.equations}\n\n"
            f"Task: Present Round 1 Opening Argument highlighting the core architectural innovation, "
            f"mathematical contributions, and benchmark superiority."
        )
        sys_prompt = "You are a top-tier machine learning researcher advocating for a groundbreaking conference submission."
        arg_text = llm_client.generate(prompt, sys_prompt)
        
        return DebateTurn(
            turn_id=f"{paper.paper_id}_R1_ADV",
            paper_id=paper.paper_id,
            round_number=1,
            speaker="Author Advocate",
            argument_title="Core Architectural Innovation & Empirical Superiority",
            argument_text=arg_text,
            cited_section="Abstract & Methodology",
            key_quote=f"Linear-time scaling with superior throughput over baselines."
        )

    def generate_rebuttal(self, paper: RawPaper, critic_argument: str) -> DebateTurn:
        prompt = (
            f"You are the Author Advocate Agent for '{paper.title}'.\n"
            f"The Critical Reviewer raised the following concerns:\n'{critic_argument}'\n\n"
            f"Task: Present Round 2 Rebuttal directly defending the methodology, compute efficiency, and reproducibility."
        )
        sys_prompt = "Defend the paper vigorously with sound technical and empirical reasoning."
        arg_text = llm_client.generate(prompt, sys_prompt)
        
        return DebateTurn(
            turn_id=f"{paper.paper_id}_R2_ADV",
            paper_id=paper.paper_id,
            round_number=2,
            speaker="Author Advocate",
            argument_title="Rebuttal on Compute Efficiency & Baseline Rigor",
            argument_text=arg_text,
            cited_section="Experiments & Discussion"
        )

advocate_agent = AuthorAdvocateAgent()
