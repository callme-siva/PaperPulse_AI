import streamlit as st
import plotly.graph_objects as go
from typing import Dict, Any, List

ACCENT = "#7C9CFF"
CELL_COLORS = {
    "novelty_score": "#7C9CFF",
    "rigor_score": "#9FB0FF",
    "baseline_fairness_score": "#E08A6F",
    "reproducibility_score": "#4ADE80",
}


def render_topbar(all_papers: List[Dict[str, Any]] = None):
    n_papers = len(all_papers) if all_papers else 0
    st.markdown(f"""
    <div class="rc-topbar">
        <div>
            <h1>PaperPulse AI</h1>
            <div class="subtitle">Multi-agent peer-review console — {n_papers} papers indexed, no account required</div>
        </div>
        <div>
            <span class="rc-chip">arXiv + Semantic Scholar, public APIs</span>
            <span class="rc-chip">Local embeddings, offline-safe</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# Backward-compatible aliases
def render_cockpit_topbar(all_papers: List[Dict[str, Any]] = None):
    render_topbar(all_papers)


def render_hero_header():
    render_topbar()


def _score_ring_gradient(score: float, max_score: float = 10.0) -> str:
    pct = max(0, min(100, int((score / max_score) * 100)))
    return f"conic-gradient({ACCENT} 0 {pct}%, #262A35 0 100%)"


def render_metric_radar_chart(review: Dict[str, Any]):
    categories = ['Novelty', 'Empirical Rigor', 'Baseline Fairness', 'Reproducibility']
    values = [
        review.get('novelty_score', 8.0),
        review.get('rigor_score', 8.0),
        review.get('baseline_fairness_score', 7.5),
        review.get('reproducibility_score', 8.5)
    ]
    categories_plot = categories + [categories[0]]
    values_plot = values + [values[0]]

    fig = go.Figure(data=go.Scatterpolar(
        r=values_plot,
        theta=categories_plot,
        fill='toself',
        fillcolor='rgba(124, 156, 255, 0.18)',
        line=dict(color=ACCENT, width=2),
        marker=dict(size=5, color=ACCENT)
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10],
                showline=False,
                tickfont=dict(size=9, color="#8B90A0"),
                gridcolor="rgba(139, 144, 160, 0.15)"
            ),
            angularaxis=dict(
                tickfont=dict(size=11, color="#E7E9EE", family="Sora"),
                gridcolor="rgba(139, 144, 160, 0.15)"
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=30, r=30, t=25, b=25),
        height=250
    )
    st.plotly_chart(fig, use_container_width=True)


def render_paper_card(paper: Dict[str, Any], is_active: bool = False):
    authors_str = ", ".join(paper.get("authors", [])) if isinstance(paper.get("authors"), list) else str(paper.get("authors"))
    abstract = (paper.get("abstract") or "")[:260]

    chips = [f'<span class="rc-chip">{paper.get("primary_category", "cs.AI")}</span>']
    if paper.get("arxiv_url"):
        chips.append(f'<a href="{paper["arxiv_url"]}" target="_blank" style="text-decoration:none;"><span class="rc-chip">arXiv:{paper.get("paper_id")} ↗</span></a>')
    chips.append(f'<span class="rc-chip">{paper.get("citation_count", 0):,} citations</span>')
    if paper.get("github_url"):
        chips.append(f'<a href="{paper["github_url"]}" target="_blank" style="text-decoration:none;"><span class="rc-chip">Code ↗</span></a>')
    if paper.get("has_latex_source"):
        chips.append('<span class="rc-chip">LaTeX source verified</span>')

    active_cls = "active" if is_active else ""

    st.markdown(f"""
    <div class="rc-card {active_cls}">
        <div>{''.join(chips)}</div>
        <h3>{paper.get('title')}</h3>
        <div class="rc-meta">{authors_str} · {paper.get('published_date', '')}</div>
        <p style="font-size: 0.85rem; color: #8B90A0; line-height: 1.55; margin: 10px 0 0 0;">
            {abstract}{'...' if len(paper.get('abstract') or '') > 260 else ''}
        </p>
    </div>
    """, unsafe_allow_html=True)


# Backward-compatible alias
def render_paper_bento_card(paper: Dict[str, Any], is_active: bool = False):
    render_paper_card(paper, is_active)


def render_rubric_cell(label: str, score: float, max_score: float = 10.0, color: str = ACCENT):
    pct = int((score / max_score) * 100)
    st.markdown(f"""
    <div class="rc-cell">
        <div class="l">{label}</div>
        <div class="v">{score:.1f}</div>
        <div class="track"><div class="fill" style="width:{pct}%; background:{color};"></div></div>
    </div>
    """, unsafe_allow_html=True)


# Backward-compatible alias — old callers pass (label, score, max_score, color)
def render_rubric_meter(label: str, score: float, max_score: float = 10.0, color: str = ACCENT):
    render_rubric_cell(label, score, max_score, color)


def render_score_ring(overall_score: float, recommendation: str, summary: str):
    gradient = _score_ring_gradient(overall_score)
    st.markdown(f"""
    <div class="rc-verdict">
        <div style="display:flex; align-items:flex-start; gap:16px;">
            <div class="rc-ring" style="background:{gradient};"><span>{overall_score:.1f}</span></div>
            <div>
                <div class="rec">{recommendation}</div>
                <div style="font-size:0.85rem; color:#8B90A0; margin-top:2px;">Multi-agent rubric assessment, not a calibrated peer-review score</div>
            </div>
        </div>
        <p style="font-size: 0.88rem; color: #E7E9EE; line-height: 1.55; margin: 14px 0 0 0;">{summary}</p>
    </div>
    """, unsafe_allow_html=True)


def render_legend_chip(color: str, label: str):
    st.markdown(f"""
    <span class="rc-chip" style="border-color:{color}66;">
        <span style="display:inline-block; width:8px; height:8px; border-radius:50%; background:{color};"></span>
        {label}
    </span>
    """, unsafe_allow_html=True)


def render_stat_tile(label: str, value: str):
    st.markdown(f"""
    <div class="rc-cell">
        <div class="l">{label}</div>
        <div class="v">{value}</div>
    </div>
    """, unsafe_allow_html=True)


def style_benchmark_table(df):
    """Pandas Styler matching the Rubric Console palette: green for positive gain, rust for negative."""
    def _delta_color(v):
        try:
            v = float(v)
        except (TypeError, ValueError):
            return ""
        if v > 0:
            return "color: #4ADE80; font-weight: 600;"
        if v < 0:
            return "color: #E08A6F; font-weight: 600;"
        return "color: #8B90A0;"

    return (
        df.style
        .hide(axis="index")
        .set_properties(**{
            "background-color": "#181B24",
            "color": "#E7E9EE",
            "border-color": "#262A35",
            "font-family": "Sora, sans-serif",
            "padding": "8px 12px",
        })
        .map(_delta_color, subset=["Gain (Δ)"])
        .set_table_styles([
            {"selector": "th", "props": [
                ("background-color", "#12141A"),
                ("color", "#8B90A0"),
                ("font-family", "IBM Plex Mono, monospace"),
                ("font-size", "0.72rem"),
                ("text-transform", "uppercase"),
                ("letter-spacing", "0.04em"),
                ("border-color", "#262A35"),
                ("padding", "8px 12px"),
                ("text-align", "left"),
            ]},
            {"selector": "table", "props": [
                ("border-collapse", "collapse"),
                ("width", "100%"),
            ]},
            {"selector": "td, th", "props": [
                ("border-bottom", "1px solid #262A35"),
            ]},
        ])
    )


def render_debate_turn(speaker: str, round_number: int, title: str, text: str):
    role_class = "critic" if "Critic" in speaker else ""
    st.markdown(f"""
    <div class="rc-turn {role_class}">
        <div class="role">{speaker} · round {round_number} · {title}</div>
        <div class="body">{text}</div>
    </div>
    """, unsafe_allow_html=True)
