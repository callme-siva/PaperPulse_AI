from ui.theme_manager import THEMES, RUBRIC_CONSOLE, apply_custom_theme
from ui.components import render_topbar, render_rubric_cell, render_paper_card
from unittest.mock import patch

def test_theme_structure():
    required_keys = ["bg_primary", "bg_card", "border", "accent", "text_primary", "text_secondary", "badge_bg", "badge_color"]
    for k in required_keys:
        assert k in RUBRIC_CONSOLE, f"Rubric Console theme is missing key '{k}'"
    assert "Rubric Console (Dark)" in THEMES

def test_apply_custom_theme():
    with patch("streamlit.markdown") as mock_markdown:
        apply_custom_theme()
        assert mock_markdown.called
        call_args = mock_markdown.call_args[0][0]
        assert "<style>" in call_args
        assert "#12141A" in call_args
