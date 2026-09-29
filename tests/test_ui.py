from ui.theme_manager import THEMES, RUBRIC_CONSOLE, NORDIC_SLATE, apply_custom_theme
from ui.components import render_topbar, render_rubric_cell, render_paper_card
from rag.llm_client import llm_client
from unittest.mock import patch

def test_theme_structure():
    required_keys = ["bg_primary", "bg_card", "border", "accent", "text_primary", "text_secondary", "badge_bg", "badge_color"]
    for k in required_keys:
        assert k in RUBRIC_CONSOLE, f"Rubric Console theme is missing key '{k}'"
        assert k in NORDIC_SLATE, f"Nordic Slate theme is missing key '{k}'"
    assert "Rubric Console (Dark)" in THEMES
    assert "🌟 Clean Nordic Slate (Light Minimal)" in THEMES
    assert "💎 Cobalt Blue (Deep Tech)" in THEMES

def test_apply_custom_theme_dark():
    with patch("streamlit.markdown") as mock_markdown:
        apply_custom_theme("🌌 Rubric Console (Dark Obsidian)")
        assert mock_markdown.called
        call_args = mock_markdown.call_args[0][0]
        assert "<style>" in call_args
        assert RUBRIC_CONSOLE["bg_primary"] in call_args

def test_apply_custom_theme_light():
    with patch("streamlit.markdown") as mock_markdown:
        apply_custom_theme("🌟 Clean Nordic Slate (Light Minimal)")
        assert mock_markdown.called
        call_args = mock_markdown.call_args[0][0]
        assert "<style>" in call_args
        assert NORDIC_SLATE["bg_primary"] in call_args

def test_llm_client_rag_config_update():
    llm_client.update_config(
        provider="OpenAI",
        model="gpt-4o-mini",
        temperature=0.45,
        top_k=8,
        hybrid_dense_weight=0.7,
        similarity_threshold=0.4,
        citation_hops=3,
        preset="🚀 Deep Exploratory & Creative",
        response_style="🔬 Detailed Analytical Proof"
    )
    assert llm_client.provider == "openai"
    assert llm_client.model == "gpt-4o-mini"
    assert llm_client.temperature == 0.45
    assert llm_client.top_k == 8
    assert llm_client.hybrid_dense_weight == 0.7
    assert llm_client.preset == "🚀 Deep Exploratory & Creative"
    assert llm_client.response_style == "🔬 Detailed Analytical Proof"

