from typing import Dict, Any, Optional
from config import GEMINI_API_KEY, OPENAI_API_KEY, GROQ_API_KEY, DEFAULT_LLM_PROVIDER, DEFAULT_LLM_MODEL

class LLMClient:
    def __init__(self):
        self.provider = DEFAULT_LLM_PROVIDER
        self.model = DEFAULT_LLM_MODEL
        self.temperature = 0.2
        self.top_k = 5
        self.hybrid_dense_weight = 0.5
        self.similarity_threshold = 0.35
        self.citation_hops = 2
        self.preset = "Strict Grounding & Precision"
        self.response_style = "Executive Bullet Points"
        self.custom_api_keys: Dict[str, str] = {}

    def update_config(
        self,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        top_k: Optional[int] = None,
        hybrid_dense_weight: Optional[float] = None,
        similarity_threshold: Optional[float] = None,
        citation_hops: Optional[int] = None,
        preset: Optional[str] = None,
        response_style: Optional[str] = None,
        api_keys: Optional[Dict[str, str]] = None,
    ):
        if provider is not None:
            self.provider = provider.lower().strip()
        if model is not None:
            self.model = model.strip()
        if temperature is not None:
            self.temperature = float(temperature)
        if top_k is not None:
            self.top_k = int(top_k)
        if hybrid_dense_weight is not None:
            self.hybrid_dense_weight = float(hybrid_dense_weight)
        if similarity_threshold is not None:
            self.similarity_threshold = float(similarity_threshold)
        if citation_hops is not None:
            self.citation_hops = int(citation_hops)
        if preset is not None:
            self.preset = preset
        if response_style is not None:
            self.response_style = response_style
        if api_keys is not None:
            self.custom_api_keys.update(api_keys)

    def _get_api_key(self, provider_key: str, default_env: str) -> str:
        return self.custom_api_keys.get(provider_key) or default_env

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        prov = self.provider or "gemini"
        
        # Inject style & preset into system instruction if specified
        enhanced_sys = system_prompt
        if self.response_style:
            enhanced_sys += f"\nFormat all output according to style: {self.response_style}."
        if self.preset:
            enhanced_sys += f"\nReasoning & grounding mode: {self.preset}."

        # 1. Google Gemini
        gemini_key = self._get_api_key("gemini", GEMINI_API_KEY)
        if (prov in ["gemini", "google gemini"]) and gemini_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=gemini_key)
                model_name = self.model if "gemini" in (self.model or "") else "gemini-2.5-flash"
                gen_config = genai.types.GenerationConfig(temperature=self.temperature)
                model = genai.GenerativeModel(model_name, generation_config=gen_config)
                full_prompt = f"{enhanced_sys}\n\n{prompt}" if enhanced_sys else prompt
                resp = model.generate_content(full_prompt)
                if resp and resp.text:
                    return resp.text.strip()
            except Exception as e:
                print(f"[LLM Gemini Error] {e}")

        # 2. OpenAI GPT-4o
        openai_key = self._get_api_key("openai", OPENAI_API_KEY)
        if (prov in ["openai", "gpt"]) and openai_key:
            try:
                from openai import OpenAI
                client = OpenAI(api_key=openai_key)
                messages = []
                if enhanced_sys:
                    messages.append({"role": "system", "content": enhanced_sys})
                messages.append({"role": "user", "content": prompt})
                model_name = self.model if self.model and "gpt" in self.model else "gpt-4o-mini"
                resp = client.chat.completions.create(
                    model=model_name,
                    messages=messages,
                    temperature=self.temperature
                )
                return resp.choices[0].message.content.strip()
            except Exception as e:
                print(f"[LLM OpenAI Error] {e}")

        # 3. Groq Llama 3
        groq_key = self._get_api_key("groq", GROQ_API_KEY)
        if (prov in ["groq", "llama"]) and groq_key:
            try:
                from groq import Groq
                client = Groq(api_key=groq_key)
                messages = []
                if enhanced_sys:
                    messages.append({"role": "system", "content": enhanced_sys})
                messages.append({"role": "user", "content": prompt})
                model_name = self.model if self.model and "llama" in self.model else "llama3-70b-8192"
                resp = client.chat.completions.create(
                    model=model_name,
                    messages=messages,
                    temperature=self.temperature
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
