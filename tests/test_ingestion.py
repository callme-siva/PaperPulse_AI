import pytest
from unittest.mock import patch, MagicMock
from ingestion.arxiv_client import ArXivClient
from ingestion.semanticscholar_client import SemanticScholarClient
from models import RawPaper

SAMPLE_ATOM_FEED = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:arxiv="http://arxiv.org/schemas/atom">
  <entry>
    <id>http://arxiv.org/abs/2312.00752v1</id>
    <published>2023-12-01T18:00:00Z</published>
    <title>Mamba: Linear-Time Sequence Modeling</title>
    <summary>We introduce Mamba, achieving 86.4% on MMLU benchmark.</summary>
    <author><name>Albert Gu</name></author>
    <author><name>Tri Dao</name></author>
    <category term="cs.LG"/>
    <category term="cs.AI"/>
  </entry>
</feed>
"""

def test_parse_atom_feed():
    client = ArXivClient()
    papers = client._parse_atom_feed(SAMPLE_ATOM_FEED, "cs.LG")
    assert len(papers) == 1
    paper = papers[0]
    assert paper.paper_id == "2312.00752"
    assert paper.title == "Mamba: Linear-Time Sequence Modeling"
    assert paper.authors == ["Albert Gu", "Tri Dao"]
    assert "cs.LG" in paper.categories
    assert paper.primary_category == "cs.LG"
    assert paper.published_date == "2023-12-01"
    assert paper.pdf_url == "https://arxiv.org/pdf/2312.00752.pdf"

def test_extract_metrics(temp_db):
    client = ArXivClient()
    paper = RawPaper(
        paper_id="test_001",
        title="Scaling Laws with MMLU: 89.2% Accuracy",
        authors=["Author A"],
        abstract="We achieve 75.4% on GSM8K and HumanEval: 68.0%.",
        categories=["cs.AI"],
        primary_category="cs.AI",
        published_date="2024-01-01",
        arxiv_url="https://arxiv.org/abs/test_001",
        pdf_url="https://arxiv.org/pdf/test_001.pdf"
    )
    with patch("ingestion.arxiv_client.db", temp_db):
        temp_db.save_paper(paper)
        client._extract_metrics(paper)
        metrics = temp_db.get_metrics_for_paper("test_001")
        assert len(metrics) >= 1
        metric_names = [m["dataset_name"] for m in metrics]
        assert any(name in ["MMLU", "GSM8K", "HUMANEVAL"] for name in metric_names)

def test_get_fallback_seed_papers():
    client = ArXivClient()
    all_seeds = client._get_fallback_seed_papers("All")
    assert len(all_seeds) >= 3

    lg_seeds = client._get_fallback_seed_papers("cs.LG")
    assert len(lg_seeds) >= 1
    assert any(s.paper_id == "2312.00752" for s in lg_seeds)

def test_semanticscholar_client():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "citationCount": 1500,
        "influentialCitationCount": 120,
        "references": [{"title": "Attention Is All You Need", "citationCount": 100000, "year": 2017}]
    }

    with patch("requests.get", return_value=mock_response):
        result = SemanticScholarClient.get_paper_citations("2312.00752")
        assert result["citation_count"] == 1500
        assert result["influential_citations"] == 120
        assert len(result["references"]) == 1

def test_semanticscholar_fallback_on_error():
    with patch("requests.get", side_effect=Exception("Network error")):
        result = SemanticScholarClient.get_paper_citations("2312.00752")
        assert result["citation_count"] == 0
        assert result["influential_citations"] == 0
        assert result["references"] == []
