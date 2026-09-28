import requests
from typing import Dict, Any, List, Optional

class SemanticScholarClient:
    """Fetches public citation counts, reference DAGs, and influential citations."""
    BASE_URL = "https://api.semanticscholar.org/graph/v1/paper"

    @staticmethod
    def get_paper_citations(arxiv_id: str) -> Dict[str, Any]:
        url = f"{SemanticScholarClient.BASE_URL}/arXiv:{arxiv_id}"
        params = {
            "fields": "title,citationCount,influentialCitationCount,references.title,references.citationCount,references.year,references.authors"
        }
        try:
            resp = requests.get(url, params=params, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                return {
                    "citation_count": data.get("citationCount", 0),
                    "influential_citations": data.get("influentialCitationCount", 0),
                    "references": data.get("references", [])[:10]
                }
        except Exception:
            pass
        return {"citation_count": 0, "influential_citations": 0, "references": []}

semantic_scholar = SemanticScholarClient()
