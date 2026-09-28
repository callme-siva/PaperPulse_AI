import streamlit as st

# Single, deliberate visual system: dark SaaS console with a rubric-first
# card as the hero unit. Replaces the old multi-theme glassmorphism "cockpit".
RUBRIC_CONSOLE = {
    "bg_primary": "#12141A",
    "bg_secondary": "#181B24",
    "bg_card": "#181B24",
    "border": "#262A35",
    "border_hover": "#333A4A",
    "accent": "#7C9CFF",
    "text_primary": "#E7E9EE",
    "text_secondary": "#8B90A0",
    "badge_bg": "#1A2030",
    "badge_color": "#9FB0FF",
    "good": "#4ADE80",
    "warn": "#F2C879",
    "critical": "#E08A6F",
}

# Kept for backward compatibility with call sites that iterate a theme registry.
THEMES = {"Rubric Console (Dark)": RUBRIC_CONSOLE}


def apply_custom_theme(theme_name: str = "Rubric Console (Dark)"):
    theme = THEMES.get(theme_name, RUBRIC_CONSOLE)
    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Sora', -apple-system, BlinkMacSystemFont, sans-serif;
    }}

    code, pre {{
        font-family: 'IBM Plex Mono', monospace !important;
    }}

    .stApp {{
        background-color: {theme['bg_primary']};
        color: {theme['text_primary']};
    }}

    /* Topbar */
    .rc-topbar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 12px;
        padding: 18px 0 20px 0;
        margin-bottom: 6px;
        border-bottom: 1px solid {theme['border']};
    }}
    .rc-topbar h1 {{
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0;
        color: {theme['text_primary']};
        letter-spacing: -0.01em;
    }}
    .rc-topbar .subtitle {{
        font-size: 0.85rem;
        color: {theme['text_secondary']};
        margin-top: 2px;
    }}

    /* Card (paper / verdict / debate turn) */
    .rc-card {{
        background: {theme['bg_card']};
        border: 1px solid {theme['border']};
        border-radius: 10px;
        padding: 16px 18px;
        margin-bottom: 14px;
    }}
    .rc-card:hover {{
        border-color: {theme['border_hover']};
    }}
    .rc-card.active {{
        border-color: {theme['accent']};
    }}

    .rc-card h3 {{
        font-size: 1.05rem;
        font-weight: 600;
        margin: 8px 0 4px 0;
        color: {theme['text_primary']};
    }}
    .rc-meta {{
        font-size: 0.8rem;
        color: {theme['text_secondary']};
    }}

    /* Chips */
    .rc-chip {{
        display: inline-flex;
        align-items: center;
        gap: 4px;
        background: {theme['badge_bg']};
        color: {theme['badge_color']};
        border: 1px solid #262F45;
        padding: 3px 9px;
        border-radius: 100px;
        font-size: 0.72rem;
        font-weight: 500;
        margin-right: 6px;
        margin-bottom: 6px;
    }}

    /* Score ring */
    .rc-ring {{
        width: 56px;
        height: 56px;
        border-radius: 50%;
        flex-shrink: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 1.05rem;
        color: {theme['text_primary']};
    }}
    .rc-ring span {{
        width: 44px;
        height: 44px;
        border-radius: 50%;
        background: {theme['bg_card']};
        display: flex;
        align-items: center;
        justify-content: center;
    }}

    /* Rubric grid cells */
    .rc-cell {{
        background: {theme['bg_secondary']};
        border: 1px solid {theme['border']};
        border-radius: 8px;
        padding: 10px 12px;
        margin-bottom: 10px;
    }}
    .rc-cell .l {{
        font-size: 0.72rem;
        color: {theme['text_secondary']};
        margin-bottom: 6px;
    }}
    .rc-cell .v {{
        font-family: 'IBM Plex Mono', monospace;
        font-weight: 600;
        font-size: 0.95rem;
        color: {theme['text_primary']};
    }}
    .rc-cell .track {{
        height: 4px;
        background: {theme['border']};
        border-radius: 2px;
        margin-top: 8px;
        overflow: hidden;
    }}
    .rc-cell .fill {{
        height: 100%;
        background: {theme['accent']};
    }}

    /* Debate transcript */
    .rc-turn {{
        border: 1px solid {theme['border']};
        border-left: 3px solid {theme['accent']};
        border-radius: 8px;
        padding: 14px 16px;
        margin-bottom: 12px;
        background: {theme['bg_secondary']};
    }}
    .rc-turn.critic {{
        border-left-color: {theme['critical']};
    }}
    .rc-turn .role {{
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        margin-bottom: 6px;
        color: {theme['accent']};
    }}
    .rc-turn.critic .role {{
        color: {theme['critical']};
    }}
    .rc-turn .body {{
        font-size: 0.88rem;
        line-height: 1.55;
        color: {theme['text_primary']};
    }}

    .rc-verdict {{
        background: {theme['bg_card']};
        border: 1px solid {theme['border']};
        border-radius: 10px;
        padding: 18px 20px;
        margin-top: 4px;
    }}
    .rc-verdict .rec {{
        font-weight: 700;
        font-size: 1rem;
        color: {theme['text_primary']};
    }}
    .rc-verdict .score {{
        font-family: 'IBM Plex Mono', monospace;
        font-weight: 700;
        color: {theme['accent']};
    }}

    /* Streamlit tab styling */
    button[data-baseweb="tab"] {{
        font-family: 'Sora', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
    }}

    ::-webkit-scrollbar {{
        width: 7px;
        height: 7px;
    }}
    ::-webkit-scrollbar-track {{
        background: {theme['bg_primary']};
    }}
    ::-webkit-scrollbar-thumb {{
        background: #333A4A;
        border-radius: 4px;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
