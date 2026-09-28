import streamlit as st
import plotly.graph_objects as go
from typing import Dict, Any, List

def render_hero_header():
    st.markdown("""
    <div style="text-align: center; padding: 24px 0 16px 0;">
        <h1 style="font-size: 2.5rem; font-weight: 800; margin-bottom: 4px; background: linear-gradient(135deg, #38BDF8 0%, #818CF8 50%, #C084FC 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            🔬 PaperPulse AI
        </h1>
        <p style="font-size: 1.05rem; color: #94A3B8; margin-bottom: 12px; font-weight: 500;">
            Autonomous Multi-Agent Academic Discovery • Adversarial Peer-Review Arena • Citation Lineage DAG
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_metric_radar_chart(review: Dict[str, Any]):
    categories = ['Novelty', 'Empirical Rigor', 'Baseline Fairness', 'Reproducibility']
    values = [
        review.get('novelty_score', 8.0),
        review.get('rigor_score', 8.0),
        review.get('baseline_fairness_score', 7.5),
        review.get('reproducibility_score', 8.5)
    ]
    # Close polygon
    categories.append(categories[0])
    values.append(values[0])

    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(56, 189, 248, 0.25)',
        line=dict(color='#38BDF8', width=2),
        marker=dict(size=6, color='#38BDF8')
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 10], showline=False, tickfont=dict(size=10, color="#94A3B8")),
            angularaxis=dict(tickfont=dict(size=12, color="#F8FAFC", family="Plus Jakarta Sans"))
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=40, t=30, b=30),
        height=280
    )
    st.plotly_chart(fig, use_container_width=True)

def render_paper_card(paper: Dict[str, Any]):
    authors_str = ", ".join(paper.get("authors", [])) if isinstance(paper.get("authors"), list) else str(paper.get("authors"))
    code_badge = f'<span class="paper-badge" style="background: rgba(16,185,129,0.2); color: #34D399;">💻 GitHub Code</span>' if paper.get("github_url") else ""
    latex_badge = f'<span class="paper-badge" style="background: rgba(139,92,246,0.2); color: #A78BFA;">📜 LaTeX Source</span>' if paper.get("has_latex_source") else ""
    
    st.markdown(f"""
    <div class="paper-card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
                <span class="paper-badge">🏷️ {paper.get('primary_category', 'cs.AI')}</span>
                <span class="paper-badge">📄 arXiv:{paper.get('paper_id')}</span>
                <span class="paper-badge">⭐ {paper.get('citation_count', 0):,} Citations</span>
                {code_badge}
                {latex_badge}
            </div>
            <span style="font-size: 0.8rem; color: #94A3B8;">📅 {paper.get('published_date', '')}</span>
        </div>
        <h3 style="margin: 10px 0 6px 0; font-size: 1.25rem; font-weight: 700; color: #F8FAFC;">
            {paper.get('title')}
        </h3>
        <p style="font-size: 0.85rem; color: #60A5FA; margin-bottom: 8px;">
            ✍️ {authors_str}
        </p>
        <p style="font-size: 0.9rem; color: #94A3B8; line-height: 1.5; margin-bottom: 12px;">
            {paper.get('abstract', '')[:280]}...
        </p>
    </div>
    """, unsafe_allow_html=True)
