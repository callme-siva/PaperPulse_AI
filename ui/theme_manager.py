import streamlit as st

THEMES = {
    "Cyber Academic (Dark)": {
        "bg_primary": "#0B0F19",
        "bg_card": "rgba(18, 24, 38, 0.75)",
        "border": "rgba(56, 189, 248, 0.25)",
        "accent": "#38BDF8",
        "text_primary": "#F8FAFC",
        "text_secondary": "#94A3B8",
        "badge_bg": "rgba(56, 189, 248, 0.15)",
        "badge_color": "#38BDF8"
    },
    "Deep Quantum Obsidian (Dark)": {
        "bg_primary": "#05070B",
        "bg_card": "rgba(15, 23, 42, 0.8)",
        "border": "rgba(139, 92, 246, 0.3)",
        "accent": "#8B5CF6",
        "text_primary": "#F8FAFC",
        "text_secondary": "#A1A1AA",
        "badge_bg": "rgba(139, 92, 246, 0.15)",
        "badge_color": "#A78BFA"
    },
    "Emerald Scholar (Dark)": {
        "bg_primary": "#06100C",
        "bg_card": "rgba(11, 28, 22, 0.8)",
        "border": "rgba(16, 185, 129, 0.3)",
        "accent": "#10B981",
        "text_primary": "#F0FDF4",
        "text_secondary": "#86EFAC",
        "badge_bg": "rgba(16, 185, 129, 0.15)",
        "badge_color": "#34D399"
    },
    "Nordic Research Slate (Light)": {
        "bg_primary": "#F8FAFC",
        "bg_card": "#FFFFFF",
        "border": "#E2E8F0",
        "accent": "#2563EB",
        "text_primary": "#0F172A",
        "text_secondary": "#64748B",
        "badge_bg": "#EFF6FF",
        "badge_color": "#2563EB"
    },
    "Royal LaTeX Porcelain (Light)": {
        "bg_primary": "#F5F3EF",
        "bg_card": "#FFFFFF",
        "border": "#E5E0D8",
        "accent": "#9333EA",
        "text_primary": "#1C1917",
        "text_secondary": "#78716C",
        "badge_bg": "#FAF5FF",
        "badge_color": "#9333EA"
    }
}

def apply_custom_theme(theme_name: str = "Cyber Academic (Dark)"):
    theme = THEMES.get(theme_name, THEMES["Cyber Academic (Dark)"])
    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Plus Jakarta Sans', sans-serif;
    }}
    
    .stApp {{
        background-color: {theme['bg_primary']};
        color: {theme['text_primary']};
    }}
    
    .paper-card {{
        background: {theme['bg_card']};
        border: 1px solid {theme['border']};
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        backdrop-filter: blur(12px);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }}
    
    .paper-card:hover {{
        border-color: {theme['accent']};
        transform: translateY(-2px);
    }}
    
    .paper-badge {{
        display: inline-block;
        background: {theme['badge_bg']};
        color: {theme['badge_color']};
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 6px;
        margin-bottom: 8px;
    }}
    
    .debate-advocate {{
        background: rgba(16, 185, 129, 0.08);
        border-left: 4px solid #10B981;
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 12px;
    }}
    
    .debate-critic {{
        background: rgba(239, 68, 68, 0.08);
        border-left: 4px solid #EF4444;
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 12px;
    }}
    
    .debate-meta {{
        background: rgba(139, 92, 246, 0.1);
        border-left: 4px solid #8B5CF6;
        border-radius: 8px;
        padding: 16px 20px;
        margin-top: 16px;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
