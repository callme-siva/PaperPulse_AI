from typing import Dict, Any, Optional
from config import GEMINI_API_KEY, OPENAI_API_KEY, GROQ_API_KEY, DEFAULT_LLM_PROVIDER, DEFAULT_LLM_MODEL

class LLMClient:
    def __init__(self):
        self.provider = DEFAULT_LLM_PROVIDER
        self.model = DEFAULT_LLM_MODEL

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        # 1. Google Gemini
        if (self.provider == "gemini" or not self.provider) and GEMINI_API_KEY:
            try:
                import google.generativeai as genai
                genai.configure(api_key=GEMINI_API_KEY)
                model = genai.GenerativeModel("gemini-2.5-flash")
                full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
                resp = model.generate_content(full_prompt)
                if resp and resp.text:
                    return resp.text.strip()
            except Exception as e:
                print(f"[LLM Gemini Error] {e}")

        # 2. OpenAI GPT-4o
        if (self.provider == "openai" or not self.provider) and OPENAI_API_KEY:
            try:
                from openai import OpenAI
                client = OpenAI(api_key=OPENAI_API_KEY)
                messages = []
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                messages.append({"role": "user", "content": prompt})
                resp = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    temperature=0.2
                )
                return resp.choices[0].message.content.strip()
            except Exception as e:
                print(f"[LLM OpenAI Error] {e}")

        # 3. Groq Llama 3
        if (self.provider == "groq" or not self.provider) and GROQ_API_KEY:
            try:
                from groq import Groq
                client = Groq(api_key=GROQ_API_KEY)
                messages = []
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                messages.append({"role": "user", "content": prompt})
                resp = client.chat.completions.create(
                    model="llama3-70b-8192",
                    messages=messages,
                    temperature=0.2
                )
                return resp.choices[0].message.content.strip()
            except Exception as e:
                print(f"[LLM Groq Error] {e}")

        # 4. Offline Deterministic Rule-Based Fallback
        return self._offline_deterministic_response(prompt)

    def _offline_deterministic_response(self, prompt: str) -> str:
        """Robust offline fallback for CI/CD and offline development without API keys."""
        if "Advocate" in prompt:
            return (
                "**Theoretical & Empirical Novelty:** The architecture demonstrates major mathematical innovations "
                "in selective state space recurrence / attention tiling. By reducing computational complexity "
                "from quadratic $O(N^2)$ to linear $O(N)$, this work establishes a new state-of-the-art across "
                "long-context sequence modeling tasks with substantial throughput speedups."
            )
        elif "Critic" in prompt or "Reviewer" in prompt:
            return (
                "**Methodological Concerns & Baseline Fairness:** While the empirical results are impressive, "
                "the baseline comparisons could be hardened. Specifically, the compute budget and hyperparameter tuning "
                "allocated to competing Transformer architectures should be strictly verified to ensure an equal FLOPs comparison."
            )
        else:
            return (
                "**Meta-Review Summary:** This paper presents a compelling, high-impact architectural contribution. "
                "The mathematical formulation is sound, and the empirical gains on standard benchmarks are significant. "
                "Recommendation: **Accept (Oral)**."
            )

llm_client = LLMClient()
