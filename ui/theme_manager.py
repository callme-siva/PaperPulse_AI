import streamlit as st

THEMES = {
    "Frontier Cockpit (Dark)": {
        "bg_primary": "#030712",
        "bg_secondary": "#0A0F1D",
        "bg_card": "rgba(15, 23, 42, 0.78)",
        "border": "rgba(56, 189, 248, 0.22)",
        "border_hover": "#38BDF8",
        "accent": "#38BDF8",
        "accent_gradient": "linear-gradient(135deg, #38BDF8 0%, #818CF8 50%, #C084FC 100%)",
        "text_primary": "#F8FAFC",
        "text_secondary": "#94A3B8",
        "badge_bg": "rgba(56, 189, 248, 0.12)",
        "badge_color": "#38BDF8",
        "card_shadow": "0 10px 30px -10px rgba(0, 0, 0, 0.8), 0 0 1px 1px rgba(56, 189, 248, 0.18)"
    },
    "DeepMind Emerald (Dark)": {
        "bg_primary": "#020D08",
        "bg_secondary": "#061F14",
        "bg_card": "rgba(6, 28, 20, 0.82)",
        "border": "rgba(16, 185, 129, 0.25)",
        "border_hover": "#10B981",
        "accent": "#10B981",
        "accent_gradient": "linear-gradient(135deg, #10B981 0%, #34D399 50%, #06B6D4 100%)",
        "text_primary": "#F0FDF4",
        "text_secondary": "#86EFAC",
        "badge_bg": "rgba(16, 185, 129, 0.15)",
        "badge_color": "#34D399",
        "card_shadow": "0 10px 30px -10px rgba(0, 0, 0, 0.8), 0 0 1px 1px rgba(16, 185, 129, 0.18)"
    },
    "Silicon Titanium (Dark)": {
        "bg_primary": "#090A0F",
        "bg_secondary": "#12141C",
        "bg_card": "rgba(20, 24, 35, 0.82)",
        "border": "rgba(148, 163, 184, 0.22)",
        "border_hover": "#E2E8F0",
        "accent": "#94A3B8",
        "accent_gradient": "linear-gradient(135deg, #F8FAFC 0%, #CBD5E1 50%, #94A3B8 100%)",
        "text_primary": "#FFFFFF",
        "text_secondary": "#94A3B8",
        "badge_bg": "rgba(148, 163, 184, 0.15)",
        "badge_color": "#E2E8F0",
        "card_shadow": "0 10px 30px -10px rgba(0, 0, 0, 0.85), 0 0 1px 1px rgba(148, 163, 184, 0.18)"
    },
    "Geneva Academic (Light)": {
        "bg_primary": "#F4F6F9",
        "bg_secondary": "#E9ECEF",
        "bg_card": "#FFFFFF",
        "border": "#E2E8F0",
        "border_hover": "#2563EB",
        "accent": "#2563EB",
        "accent_gradient": "linear-gradient(135deg, #1E40AF 0%, #2563EB 50%, #3B82F6 100%)",
        "text_primary": "#0F172A",
        "text_secondary": "#64748B",
        "badge_bg": "rgba(37, 99, 235, 0.08)",
        "badge_color": "#2563EB",
        "card_shadow": "0 4px 20px -2px rgba(0, 0, 0, 0.06), 0 0 1px 1px rgba(0, 0, 0, 0.04)"
    },
    "Kyoto Porcelain (Light)": {
        "bg_primary": "#F7F5F0",
        "bg_secondary": "#EFECE4",
        "bg_card": "#FFFFFF",
        "border": "#E6E2D8",
        "border_hover": "#7C3AED",
        "accent": "#7C3AED",
        "accent_gradient": "linear-gradient(135deg, #6D28D9 0%, #7C3AED 50%, #A78BFA 100%)",
        "text_primary": "#1C1917",
        "text_secondary": "#78716C",
        "badge_bg": "rgba(124, 58, 237, 0.08)",
        "badge_color": "#7C3AED",
        "card_shadow": "0 4px 20px -2px rgba(40, 30, 20, 0.06), 0 0 1px 1px rgba(0, 0, 0, 0.04)"
    }
}

def apply_custom_theme(theme_name: str = "Frontier Cockpit (Dark)"):
    theme = THEMES.get(theme_name, THEMES["Frontier Cockpit (Dark)"])
    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    
    code, pre, .latex-code, .math-display {{
        font-family: 'JetBrains Mono', monospace !important;
    }}
    
    .stApp {{
        background-color: {theme['bg_primary']};
        color: {theme['text_primary']};
    }}

    /* Main Cockpit Container Header */
    .cockpit-header {{
        background: {theme['bg_card']};
        border: 1px solid {theme['border']};
        border-radius: 18px;
        padding: 24px 28px 18px 28px;
        margin-bottom: 16px;
        backdrop-filter: blur(20px);
        box-shadow: {theme['card_shadow']};
        position: relative;
        overflow: hidden;
    }}
    
    .cockpit-header::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; height: 3px;
        background: {theme['accent_gradient']};
    }}

    /* Live arXiv Paper Marquee Ticker */
    .ticker-wrap {{
        width: 100%;
        overflow: hidden;
        background: rgba(2, 6, 23, 0.6);
        border: 1px solid {theme['border']};
        border-radius: 10px;
        padding: 8px 14px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 12px;
    }}

    .ticker-label {{
        background: {theme['accent']};
        color: #030712;
        font-weight: 800;
        font-size: 0.72rem;
        padding: 2px 8px;
        border-radius: 4px;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        white-space: nowrap;
        display: flex;
        align-items: center;
        gap: 4px;
    }}

    .ticker-content {{
        display: flex;
        gap: 28px;
        white-space: nowrap;
        animation: marquee 28s linear infinite;
        font-size: 0.82rem;
        font-weight: 500;
        color: {theme['text_secondary']};
    }}

    .ticker-content:hover {{
        animation-play-state: paused;
    }}

    @keyframes marquee {{
        0% {{ transform: translateX(0%); }}
        100% {{ transform: translateX(-50%); }}
    }}

    /* Bento Grid Card */
    .bento-card {{
        background: {theme['bg_card']};
        border: 1px solid {theme['border']};
        border-radius: 16px;
        padding: 20px 22px;
        margin-bottom: 16px;
        backdrop-filter: blur(16px);
        box-shadow: {theme['card_shadow']};
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
        position: relative;
    }}
    
    .bento-card:hover {{
        border-color: {theme['border_hover']};
        transform: translateY(-2px);
        box-shadow: 0 16px 36px -8px rgba(0, 0, 0, 0.6), 0 0 14px 2px {theme['badge_bg']};
    }}

    .bento-active {{
        border-color: {theme['accent']} !important;
        box-shadow: 0 0 18px 2px {theme['badge_bg']} !important;
    }}
    
    .cockpit-pill {{
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: {theme['badge_bg']};
        color: {theme['badge_color']};
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 6px;
        margin-bottom: 6px;
        border: 1px solid rgba(255, 255, 255, 0.06);
    }}

    /* Split Adversarial Arena Cage */
    .arena-advocate-cage {{
        background: rgba(16, 185, 129, 0.08);
        border: 1px solid rgba(16, 185, 129, 0.35);
        border-radius: 14px;
        padding: 20px 22px;
        margin-bottom: 16px;
        box-shadow: 0 4px 20px -3px rgba(16, 185, 129, 0.12);
    }}

    .arena-critic-cage {{
        background: rgba(244, 63, 94, 0.08);
        border: 1px solid rgba(244, 63, 94, 0.35);
        border-radius: 14px;
        padding: 20px 22px;
        margin-bottom: 16px;
        box-shadow: 0 4px 20px -3px rgba(244, 63, 94, 0.12);
    }}

    .arena-verdict-deck {{
        background: rgba(139, 92, 246, 0.1);
        border: 1px solid rgba(139, 92, 246, 0.4);
        border-radius: 16px;
        padding: 22px 26px;
        margin-top: 18px;
        box-shadow: 0 8px 25px -4px rgba(139, 92, 246, 0.18);
    }}

    /* Streamlit Tab Enhancements */
    button[data-baseweb="tab"] {{
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        border-radius: 10px !important;
        padding: 10px 18px !important;
        transition: all 0.2s ease !important;
    }}

    /* Custom Scrollbars */
    ::-webkit-scrollbar {{
        width: 7px;
        height: 7px;
    }}
    ::-webkit-scrollbar-track {{
        background: {theme['bg_primary']};
    }}
    ::-webkit-scrollbar-thumb {{
        background: rgba(148, 163, 184, 0.25);
        border-radius: 4px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
        background: rgba(148, 163, 184, 0.45);
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
