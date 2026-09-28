from ui.theme_manager import THEMES, apply_custom_theme
from ui.components import render_cockpit_topbar, render_rubric_meter, render_paper_bento_card
from unittest.mock import patch

def test_themes_structure():
    assert len(THEMES) >= 5
    required_keys = ["bg_primary", "bg_card", "border", "accent", "text_primary", "text_secondary", "badge_bg", "badge_color"]
    for theme_name, theme_data in THEMES.items():
        for k in required_keys:
            assert k in theme_data, f"Theme '{theme_name}' is missing key '{k}'"

def test_apply_custom_theme():
    with patch("streamlit.markdown") as mock_markdown:
        apply_custom_theme("Frontier Cockpit (Dark)")
        assert mock_markdown.called
        call_args = mock_markdown.call_args[0][0]
        assert "<style>" in call_args
        assert "#030712" in call_args
