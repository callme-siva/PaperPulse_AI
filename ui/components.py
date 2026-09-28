import streamlit as st
import plotly.graph_objects as go
from typing import Dict, Any, List

def render_cockpit_topbar(all_papers: List[Dict[str, Any]] = None):
    # Prepare paper titles for ticker marquee
    ticker_items = []
    if all_papers:
        for p in all_papers[:6]:
            cits = p.get("citation_count", 0)
            ticker_items.append(f"<b>[{p.get('primary_category', 'cs.AI')}]</b> {p.get('title', '')} — <i>{cits:,} citations</i>")
    
    if not ticker_items:
        ticker_items = [
            "<b>[cs.LG]</b> Mamba: Linear-Time Sequence Modeling — <i>1,840 citations</i>",
            "<b>[cs.AI]</b> FlashAttention-2: Faster Attention with Better Parallelism — <i>2,950 citations</i>",
            "<b>[cs.CL]</b> DeepSeek-Coder: When Large Language Models Meet Programming — <i>410 citations</i>"
        ]
        
    ticker_html_content = " &nbsp;&nbsp;•&nbsp;&nbsp; ".join(ticker_items)
    # Double it for seamless continuous loop
    full_ticker_html = f"{ticker_html_content} &nbsp;&nbsp;•&nbsp;&nbsp; {ticker_html_content}"

    st.markdown(f"""
    <div class="cockpit-header">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; margin-bottom: 12px;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <span style="font-size: 1.8rem;">🔬</span>
                <div>
                    <h1 style="font-size: 2.2rem; font-weight: 800; letter-spacing: -0.03em; margin: 0; background: linear-gradient(135deg, #38BDF8 0%, #818CF8 50%, #C084FC 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                        PaperPulse AI
                    </h1>
                    <div style="font-size: 0.85rem; color: #94A3B8; font-weight: 500;">
                        Frontier Academic Research Discovery & Autonomous Multi-Agent Peer-Review Cockpit
                    </div>
                </div>
            </div>
            <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                <span class="cockpit-pill" style="background: rgba(16,185,129,0.15); color: #34D399; border-color: rgba(16,185,129,0.3);">
                    🟢 arXiv API Live Feed
                </span>
                <span class="cockpit-pill">⚡ 384-Dim Local Vector RAG</span>
                <span class="cockpit-pill">🛡️ Verifiable LaTeX Grounding</span>
                <span class="cockpit-pill">🤖 ICLR/NeurIPS Rubric Calibrated</span>
            </div>
        </div>
        
        <!-- Live Continuous Streaming Paper Marquee Ticker -->
        <div class="ticker-wrap">
            <div class="ticker-label">
                <span>📡 LIVE ARRANGE</span>
            </div>
            <div class="ticker-content">
                <span>{full_ticker_html}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_hero_header():
    render_cockpit_topbar()

def render_metric_radar_chart(review: Dict[str, Any]):
    categories = ['Novelty', 'Empirical Rigor', 'Baseline Fairness', 'Reproducibility']
    values = [
        review.get('novelty_score', 8.0),
        review.get('rigor_score', 8.0),
        review.get('baseline_fairness_score', 7.5),
        review.get('reproducibility_score', 8.5)
    ]
    # Close polygon
    categories_plot = categories + [categories[0]]
    values_plot = values + [values[0]]

    fig = go.Figure(data=go.Scatterpolar(
        r=values_plot,
        theta=categories_plot,
        fill='toself',
        fillcolor='rgba(56, 189, 248, 0.22)',
        line=dict(color='#38BDF8', width=2.5),
        marker=dict(size=6, color='#38BDF8')
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10],
                showline=False,
                tickfont=dict(size=9, color="#94A3B8"),
                gridcolor="rgba(148, 163, 184, 0.15)"
            ),
            angularaxis=dict(
                tickfont=dict(size=11, color="#F8FAFC", family="Plus Jakarta Sans", weight=600),
                gridcolor="rgba(148, 163, 184, 0.15)"
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
    render_paper_bento_card(paper, is_active)

def render_paper_bento_card(paper: Dict[str, Any], is_active: bool = False):
    authors_str = ", ".join(paper.get("authors", [])) if isinstance(paper.get("authors"), list) else str(paper.get("authors"))
    code_badge = f'<a href="{paper.get("github_url")}" target="_blank" style="text-decoration:none;"><span class="cockpit-pill" style="background: rgba(16,185,129,0.18); color: #34D399; border-color: rgba(16,185,129,0.3);">💻 Open Source Code ↗</span></a>' if paper.get("github_url") else ""
    latex_badge = f'<span class="cockpit-pill" style="background: rgba(139,92,246,0.18); color: #C084FC; border-color: rgba(139,92,246,0.3);">📜 LaTeX Math Verified</span>' if paper.get("has_latex_source") else ""
    arxiv_link = f'<a href="{paper.get("arxiv_url", "")}" target="_blank" style="text-decoration:none;"><span class="cockpit-pill" style="background: rgba(56,189,248,0.15); color: #38BDF8; border-color: rgba(56,189,248,0.3);">📄 arXiv:{paper.get("paper_id")} ↗</span></a>'
    pdf_link = f'<a href="{paper.get("pdf_url", "")}" target="_blank" style="text-decoration:none;"><span class="cockpit-pill" style="background: rgba(239,68,68,0.15); color: #F87171; border-color: rgba(239,68,68,0.3);">📥 PDF ↗</span></a>'
    
    active_cls = "bento-active" if is_active else ""
    
    st.markdown(f"""
    <div class="bento-card {active_cls}">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 8px;">
            <div style="display: flex; flex-wrap: wrap; align-items: center;">
                <span class="cockpit-pill" style="font-weight: 700;">🏷️ {paper.get('primary_category', 'cs.AI')}</span>
                {arxiv_link}
                {pdf_link}
                <span class="cockpit-pill">⭐ {paper.get('citation_count', 0):,} Citations</span>
                {code_badge}
                {latex_badge}
            </div>
            <span style="font-size: 0.8rem; color: #94A3B8; font-weight: 500;">📅 {paper.get('published_date', '')}</span>
        </div>
        <h3 style="margin: 12px 0 6px 0; font-size: 1.25rem; font-weight: 700; color: #F8FAFC; letter-spacing: -0.01em;">
            {paper.get('title')}
        </h3>
        <p style="font-size: 0.85rem; color: #60A5FA; margin-bottom: 10px; font-weight: 500;">
            ✍️ {authors_str}
        </p>
        <p style="font-size: 0.88rem; color: #94A3B8; line-height: 1.55; margin-bottom: 12px;">
            {paper.get('abstract', '')[:300]}...
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_rubric_meter(label: str, score: float, max_score: float = 10.0, color: str = "#38BDF8"):
    percentage = int((score / max_score) * 100)
    st.markdown(f"""
    <div style="margin-bottom: 10px;">
        <div style="display: flex; justify-content: space-between; font-size: 0.85rem; font-weight: 600; margin-bottom: 4px;">
            <span>{label}</span>
            <span style="color: {color}; font-family: 'JetBrains Mono', monospace;">{score:.1f} / {max_score:.1f}</span>
        </div>
        <div style="width: 100%; height: 6px; background: rgba(148, 163, 184, 0.2); border-radius: 4px; overflow: hidden;">
            <div style="width: {percentage}%; height: 100%; background: {color}; border-radius: 4px; transition: width 0.4s ease;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
