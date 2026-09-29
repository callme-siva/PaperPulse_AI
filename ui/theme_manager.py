import streamlit as st

# Theme palettes for PaperPulse AI
RUBRIC_CONSOLE = {
    "name": "Rubric Console (Dark)",
    "bg_primary": "#0D0F14",
    "bg_secondary": "#141721",
    "bg_card": "#161A26",
    "border": "#232838",
    "border_hover": "#3E4760",
    "accent": "#7C9CFF",
    "text_primary": "#F1F3F9",
    "text_secondary": "#8E96AB",
    "badge_bg": "#1B2238",
    "badge_color": "#A5B4FC",
    "good": "#4ADE80",
    "warn": "#F2C879",
    "critical": "#E08A6F",
    "is_dark": True,
}

NORDIC_SLATE = {
    "name": "Clean Nordic Slate (Light Minimal)",
    "bg_primary": "#F8FAFC",
    "bg_secondary": "#FFFFFF",
    "bg_card": "#FFFFFF",
    "border": "#E2E8F0",
    "border_hover": "#94A3B8",
    "accent": "#2563EB",
    "text_primary": "#0F172A",
    "text_secondary": "#475569",
    "badge_bg": "#EFF6FF",
    "badge_color": "#1D4ED8",
    "good": "#16A34A",
    "warn": "#D97706",
    "critical": "#DC2626",
    "is_dark": False,
}

COBALT_DEEP = {
    "name": "Cobalt Blue (Deep Tech)",
    "bg_primary": "#080E1A",
    "bg_secondary": "#0C1527",
    "bg_card": "#101E38",
    "border": "#1C2E52",
    "border_hover": "#38BDF8",
    "accent": "#38BDF8",
    "text_primary": "#F8FAFC",
    "text_secondary": "#94A3B8",
    "badge_bg": "#0E2548",
    "badge_color": "#7DD3FC",
    "good": "#34D399",
    "warn": "#FBBF24",
    "critical": "#F87171",
    "is_dark": True,
}

EMERALD_MATRIX = {
    "name": "Emerald Matrix (Forest Cyber)",
    "bg_primary": "#06120D",
    "bg_secondary": "#0B1E15",
    "bg_card": "#0F291D",
    "border": "#194430",
    "border_hover": "#34D399",
    "accent": "#10B981",
    "text_primary": "#ECFDF5",
    "text_secondary": "#6EE7B7",
    "badge_bg": "#0A3322",
    "badge_color": "#6EE7B7",
    "good": "#34D399",
    "warn": "#FCD34D",
    "critical": "#FB7185",
    "is_dark": True,
}

CYBERPUNK_VIOLET = {
    "name": "Cyberpunk Violet (Neon Dark)",
    "bg_primary": "#0F0619",
    "bg_secondary": "#180B27",
    "bg_card": "#200E34",
    "border": "#3B1761",
    "border_hover": "#C084FC",
    "accent": "#C084FC",
    "text_primary": "#FAF5FF",
    "text_secondary": "#D8B4FE",
    "badge_bg": "#331154",
    "badge_color": "#E9D5FF",
    "good": "#4ADE80",
    "warn": "#FDE047",
    "critical": "#F43F5E",
    "is_dark": True,
}

THEMES = {
    "Rubric Console (Dark)": RUBRIC_CONSOLE,
    "🌌 Rubric Console (Dark Obsidian)": RUBRIC_CONSOLE,
    "🌟 Clean Nordic Slate (Light Minimal)": NORDIC_SLATE,
    "💎 Cobalt Blue (Deep Tech)": COBALT_DEEP,
    "🌲 Emerald Matrix (Forest Cyber)": EMERALD_MATRIX,
    "⚡ Cyberpunk Violet (Neon Dark)": CYBERPUNK_VIOLET,
}


def apply_custom_theme(theme_name: str = "🌌 Rubric Console (Dark Obsidian)"):
    theme = THEMES.get(theme_name)
    if not theme:
        for k, v in THEMES.items():
            if theme_name in k or k in theme_name:
                theme = v
                break
    if not theme:
        theme = RUBRIC_CONSOLE

    is_dark = theme.get("is_dark", True)
    sidebar_bg = theme['bg_secondary'] if is_dark else '#FFFFFF'
    input_bg = theme['bg_secondary'] if is_dark else '#FFFFFF'
    card_shadow = '0 2px 10px rgba(0,0,0,0.3)' if is_dark else '0 1px 4px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04)'
    card_hover_shadow = '0 4px 18px rgba(0,0,0,0.4)' if is_dark else '0 4px 12px rgba(0,0,0,0.1)'
    engine_bar_bg = '#F0FDF4' if not is_dark else theme['badge_bg']
    engine_bar_border = '#86EFAC' if not is_dark else f"{theme['accent']}40"

    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

    html, body, [class*="css"], .stApp {{
        font-family: 'Sora', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }}

    code, pre {{
        font-family: 'IBM Plex Mono', monospace !important;
    }}

    .stApp {{
        background-color: {theme['bg_primary']} !important;
        color: {theme['text_primary']} !important;
    }}

    header[data-testid="stHeader"] {{
        background: transparent !important;
    }}

    /* Global Typography & Headings */
    h1, h2, h3, h4, h5, h6,
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
    .stMarkdown h4, .stMarkdown h5, .stMarkdown h6,
    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3,
    [data-testid="stMarkdownContainer"] h4,
    [data-testid="stMarkdownContainer"] h5,
    [data-testid="stMarkdownContainer"] h6 {{
        color: {theme['text_primary']} !important;
        font-family: 'Sora', sans-serif !important;
    }}

    p, span, li,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] span,
    [data-testid="stMarkdownContainer"] li {{
        color: {theme['text_primary']} !important;
    }}

    .stCaption,
    [data-testid="stCaptionContainer"] p,
    [data-testid="stCaptionContainer"] {{
        color: {theme['text_secondary']} !important;
    }}

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {{
        background-color: {sidebar_bg} !important;
        border-right: 1px solid {theme['border']} !important;
    }}

    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{
        color: {theme['text_primary']} !important;
    }}

    /* Telemetry & Metrics */
    [data-testid="stMetricValue"], [data-testid="stMetricValue"] * {{
        color: {theme['text_primary']} !important;
        font-family: 'IBM Plex Mono', monospace !important;
        font-weight: 700 !important;
    }}
    [data-testid="stMetricLabel"], [data-testid="stMetricLabel"] * {{
        color: {theme['text_secondary']} !important;
        font-weight: 500 !important;
    }}

    /* Topbar */
    .rc-topbar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 12px;
        padding: 16px 0 18px 0;
        margin-bottom: 8px;
        border-bottom: 1px solid {theme['border']};
    }}
    .rc-topbar h1 {{
        font-size: 1.55rem;
        font-weight: 700;
        margin: 0;
        color: {theme['text_primary']} !important;
        letter-spacing: -0.01em;
    }}
    .rc-topbar .subtitle {{
        font-size: 0.85rem;
        color: {theme['text_secondary']} !important;
        margin-top: 3px;
    }}

    /* Cards */
    .rc-card {{
        background: {theme['bg_card']};
        border: 1px solid {theme['border']};
        border-radius: 10px;
        padding: 16px 18px;
        margin-bottom: 12px;
        box-shadow: {card_shadow};
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }}
    .rc-card:hover {{
        border-color: {theme['border_hover']};
        box-shadow: {card_hover_shadow};
    }}
    .rc-card.active {{
        border-color: {theme['accent']};
        box-shadow: 0 0 0 2px {theme['accent']}40;
    }}

    .rc-card h3 {{
        font-size: 1.05rem;
        font-weight: 600;
        margin: 8px 0 4px 0;
        color: {theme['text_primary']} !important;
    }}
    .rc-meta {{
        font-size: 0.8rem;
        color: {theme['text_secondary']} !important;
    }}
    .rc-card-abstract {{
        font-size: 0.85rem;
        color: {theme['text_secondary']} !important;
        line-height: 1.55;
        margin: 10px 0 0 0;
    }}

    /* Chips */
    .rc-chip {{
        display: inline-flex;
        align-items: center;
        gap: 4px;
        background: {theme['badge_bg']};
        color: {theme['badge_color']} !important;
        border: 1px solid {theme['badge_color']}33;
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
        color: {theme['text_primary']} !important;
    }}
    .rc-ring span {{
        width: 44px;
        height: 44px;
        border-radius: 50%;
        background: {theme['bg_card']};
        display: flex;
        align-items: center;
        justify-content: center;
        color: {theme['text_primary']} !important;
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
        color: {theme['text_secondary']} !important;
        margin-bottom: 6px;
    }}
    .rc-cell .v {{
        font-family: 'IBM Plex Mono', monospace;
        font-weight: 600;
        font-size: 0.95rem;
        color: {theme['text_primary']} !important;
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
        background: {theme['bg_card']};
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
        color: {theme['accent']} !important;
    }}
    .rc-turn.critic .role {{
        color: {theme['critical']} !important;
    }}
    .rc-turn .body {{
        font-size: 0.88rem;
        line-height: 1.55;
        color: {theme['text_primary']} !important;
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
        font-size: 1.05rem;
        color: {theme['text_primary']} !important;
    }}
    .rc-verdict-sub {{
        font-size: 0.85rem;
        color: {theme['text_secondary']} !important;
        margin-top: 2px;
    }}
    .rc-verdict-body {{
        font-size: 0.88rem;
        color: {theme['text_primary']} !important;
        line-height: 1.55;
        margin: 14px 0 0 0;
    }}

    /* Engine pill summary bar */
    .rc-engine-bar {{
        background: {engine_bar_bg};
        border: 1px solid {engine_bar_border};
        border-radius: 10px;
        padding: 10px 16px;
        margin-bottom: 16px;
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 8px;
        font-size: 0.82rem;
    }}
    .rc-engine-chip {{
        background: {theme['bg_card']};
        border: 1px solid {theme['border']};
        padding: 3px 10px;
        border-radius: 100px;
        font-weight: 500;
        color: {theme['text_primary']} !important;
        display: inline-flex;
        align-items: center;
        gap: 4px;
    }}
    .rc-engine-sub {{
        font-size: 0.78rem;
        color: {theme['text_secondary']} !important;
        margin-top: -10px;
        margin-bottom: 14px;
    }}

    /* Selectbox, Inputs & Popovers */
    label, [data-testid="stWidgetLabel"] label, [data-testid="stWidgetLabel"] p {{
        color: {theme['text_primary']} !important;
        font-weight: 500 !important;
    }}

    div[data-baseweb="select"] > div {{
        background-color: {input_bg} !important;
        border-color: {theme['border']} !important;
        color: {theme['text_primary']} !important;
    }}

    div[data-baseweb="select"] span {{
        color: {theme['text_primary']} !important;
    }}

    div[data-baseweb="select"] svg {{
        fill: {theme['text_primary']} !important;
    }}

    div[data-baseweb="popover"],
    div[data-baseweb="popover"] ul,
    div[data-baseweb="menu"],
    ul[role="listbox"] {{
        background-color: {theme['bg_card']} !important;
        border: 1px solid {theme['border']} !important;
        box-shadow: {card_hover_shadow} !important;
    }}

    li[role="option"],
    div[data-baseweb="popover"] li,
    div[data-baseweb="popover"] span {{
        background-color: {theme['bg_card']} !important;
        color: {theme['text_primary']} !important;
    }}

    li[role="option"]:hover,
    li[role="option"][aria-selected="true"] {{
        background-color: {theme['badge_bg']} !important;
        color: {theme['badge_color']} !important;
    }}

    .stTextInput input {{
        background-color: {input_bg} !important;
        border-color: {theme['border']} !important;
        color: {theme['text_primary']} !important;
    }}

    /* Expanders */
    details[data-testid="stExpander"] {{
        background-color: {theme['bg_card']} !important;
        border: 1px solid {theme['border']} !important;
        border-radius: 8px !important;
    }}
    details[data-testid="stExpander"] summary,
    details[data-testid="stExpander"] summary p,
    details[data-testid="stExpander"] summary span {{
        color: {theme['text_primary']} !important;
        font-weight: 600 !important;
    }}
    details[data-testid="stExpander"] summary svg {{
        fill: {theme['text_primary']} !important;
    }}

    /* Pills navigation */
    [data-testid="stPills"] button {{
        background-color: {theme['bg_card']} !important;
        color: {theme['text_primary']} !important;
        border: 1px solid {theme['border']} !important;
        font-weight: 500 !important;
        border-radius: 8px !important;
        transition: all 0.15s ease-in-out !important;
    }}
    [data-testid="stPills"] button[aria-selected="true"] {{
        background-color: {theme['accent']} !important;
        color: #FFFFFF !important;
        border-color: {theme['accent']} !important;
        font-weight: 600 !important;
    }}

    /* Buttons */
    button[kind="primary"], .stButton>button[type="primary"], button[data-testid="baseButton-primary"] {{
        background-color: {theme['accent']} !important;
        color: #FFFFFF !important;
        border: 1px solid {theme['accent']} !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
    }}

    button[kind="secondary"], .stButton>button, button[data-testid="baseButton-secondary"] {{
        background-color: {theme['bg_card']} !important;
        color: {theme['text_primary']} !important;
        border: 1px solid {theme['border']} !important;
        font-weight: 500 !important;
        border-radius: 8px !important;
    }}

    button[kind="secondary"]:hover, .stButton>button:hover {{
        border-color: {theme['border_hover']} !important;
        color: {theme['accent']} !important;
    }}

    /* Code & Pre */
    pre, code, .stCode, div[data-testid="stCodeBlock"] {{
        background-color: {theme['bg_secondary']} !important;
        color: {theme['text_primary']} !important;
        border: 1px solid {theme['border']} !important;
        border-radius: 6px !important;
    }}

    div[data-testid="stLatex"] {{
        color: {theme['text_primary']} !important;
    }}

    ::-webkit-scrollbar {{
        width: 7px;
        height: 7px;
    }}
    ::-webkit-scrollbar-track {{
        background: {theme['bg_primary']};
    }}
    ::-webkit-scrollbar-thumb {{
        background: {theme['border_hover']};
        border-radius: 4px;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


