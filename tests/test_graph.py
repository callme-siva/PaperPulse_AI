from graph.lineage_graph import CitationLineageGraph, citation_graph_engine

def test_build_lineage_graph_known_paper():
    html = citation_graph_engine.build_lineage_graph(
        seed_paper_id="2312.00752",
        seed_title="Mamba: Linear-Time Sequence Modeling"
    )
    
    # HTML checks
    assert "<!DOCTYPE html>" in html
    assert "vis-network" in html
    assert "mynetwork" in html
    
    # Check that seed paper and known ancestors (e.g., S4, HiPPO) are in the HTML graph definition
    assert "2312.00752" in html
    assert "S4" in html
    assert "HiPPO" in html
    assert "Attention Is All You Need" in html

def test_build_lineage_graph_generic_paper():
    html = citation_graph_engine.build_lineage_graph(
        seed_paper_id="9999.99999",
        seed_title="Novel Generic Architecture"
    )
    assert "<!DOCTYPE html>" in html
    assert "9999.99999" in html
    assert "Attention Is All You Need" in html
    assert "vis.Network" in html
