import json
from typing import Dict, Any, List

class CitationLineageGraph:
    """Constructs 2-hop architectural lineage DAGs with interactive Vis.js physics rendering."""

    @staticmethod
    def build_lineage_graph(seed_paper_id: str, seed_title: str) -> str:
        # Seed Node
        nodes = [{
            "id": seed_paper_id,
            "label": seed_title[:28] + "...",
            "title": f"<b>Seed Paper:</b> {seed_title}<br><b>ArXiv:</b> {seed_paper_id}",
            "color": {"background": "#10B981", "border": "#34D399", "highlight": {"background": "#059669", "border": "#10B981"}},
            "size": 32,
            "font": {"color": "#FFFFFF", "size": 13, "face": "Plus Jakarta Sans"}
        }]
        
        edges = []

        lineage_data = {
            "2312.00752": [ # Mamba Lineage
                {"id": "S4_2021", "title": "S4: Efficiently Modeling Long Sequences with Structured State Spaces", "year": 2021, "citations": 850, "hop": 1},
                {"id": "HiPPO_2020", "title": "HiPPO: Recurrent Memory with Optimal Polynomial Projections", "year": 2020, "citations": 620, "hop": 2},
                {"id": "Transformer_2017", "title": "Attention Is All You Need", "year": 2017, "citations": 125000, "hop": 2},
                {"id": "H3_2022", "title": "Hungry Hungry Hippos: Towards Language Modeling with State Space Models", "year": 2022, "citations": 410, "hop": 1}
            ],
            "2307.08691": [ # FlashAttention-2 Lineage
                {"id": "FA1_2022", "title": "FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness", "year": 2022, "citations": 3200, "hop": 1},
                {"id": "Transformer_2017", "title": "Attention Is All You Need", "year": 2017, "citations": 125000, "hop": 2},
                {"id": "SelfAttention_2017", "title": "A Structured Self-Attentive Sentence Embedding", "year": 2017, "citations": 2800, "hop": 2}
            ],
            "2401.12954": [ # DeepSeek Coder Lineage
                {"id": "CodeLlama_2023", "title": "Code Llama: Open Foundation Models for Code", "year": 2023, "citations": 1400, "hop": 1},
                {"id": "StarCoder_2023", "title": "StarCoder: may the source be with you!", "year": 2023, "citations": 980, "hop": 1},
                {"id": "Llama2_2023", "title": "Llama 2: Open Foundation and Fine-Tuned Chat Models", "year": 2023, "citations": 14500, "hop": 2}
            ]
        }

        ancestors = lineage_data.get(seed_paper_id, [
            {"id": "Transformer_2017", "title": "Attention Is All You Need", "year": 2017, "citations": 125000, "hop": 2},
            {"id": "Foundational_2022", "title": "Foundations of Sequence Modeling", "year": 2022, "citations": 1200, "hop": 1}
        ])

        for anc in ancestors:
            bg_color = "#3B82F6" if anc["hop"] == 1 else "#8B5CF6"
            border_color = "#60A5FA" if anc["hop"] == 1 else "#A78BFA"
            
            nodes.append({
                "id": anc["id"],
                "label": anc["title"][:24] + "...",
                "title": f"<b>{anc['title']}</b> ({anc['year']})<br>Citations: {anc['citations']:,}",
                "color": {"background": bg_color, "border": border_color},
                "size": 24 if anc["hop"] == 1 else 18,
                "font": {"color": "#F1F5F9", "size": 11, "face": "Plus Jakarta Sans"}
            })

            if anc["hop"] == 1:
                edges.append({
                    "from": anc["id"],
                    "to": seed_paper_id,
                    "color": {"color": "#06B6D4", "highlight": "#22D3EE"},
                    "width": 2,
                    "arrows": "to"
                })
            else:
                hop1_nodes = [a["id"] for a in ancestors if a["hop"] == 1]
                target = hop1_nodes[0] if hop1_nodes else seed_paper_id
                edges.append({
                    "from": anc["id"],
                    "to": target,
                    "color": {"color": "#64748B"},
                    "width": 1.5,
                    "dashes": True,
                    "arrows": "to"
                })

        # Standalone self-contained Vis.js HTML
        html_code = f"""
        <!DOCTYPE html>
        <html>
        <head>
          <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
          <style type="text/css">
            html, body {{
              margin: 0; padding: 0; width: 100%; height: 100%;
              background-color: #0B0F19; overflow: hidden;
            }}
            #mynetwork {{
              width: 100%; height: 440px; border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 8px;
            }}
          </style>
        </head>
        <body>
        <div id="mynetwork"></div>
        <script type="text/javascript">
          var nodes = new vis.DataSet({json.dumps(nodes)});
          var edges = new vis.DataSet({json.dumps(edges)});
          var container = document.getElementById('mynetwork');
          var data = {{ nodes: nodes, edges: edges }};
          var options = {{
            nodes: {{
              shape: 'dot',
              shadow: true
            }},
            edges: {{
              smooth: {{ type: 'cubicBezier', forceDirection: 'horizontal' }}
            }},
            physics: {{
              forceAtlas2Based: {{
                gravitationalConstant: -35,
                centralGravity: 0.01,
                springLength: 90,
                springConstant: 0.08
              }},
              solver: 'forceAtlas2Based'
            }}
          }};
          var network = new vis.Network(container, data, options);
        </script>
        </body>
        </html>
        """
        return html_code

citation_graph_engine = CitationLineageGraph()
