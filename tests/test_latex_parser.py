import io
import tarfile
import gzip
from ingestion.latex_parser import LaTeXParser, latex_parser

SAMPLE_LATEX = r"""
\documentclass{article}
\begin{document}
\title{Sample Academic Paper}
\author{Researcher One \and Researcher Two}
\maketitle

\section{Introduction}
Deep learning has revolutionized artificial intelligence.
We propose a novel recurrence relation.

\begin{equation}
h_t = \mathbf{A} h_{t-1} + \mathbf{B} x_t
\end{equation}

\section{Methodology}
Our approach relies on the following optimization:

\begin{align}
\mathcal{L}(\theta) = \sum_{i=1}^N \ell(f(x_i; \theta), y_i)
\end{align}

Also consider the display math:
\[
y_t = \mathbf{C} h_t + \mathbf{D} x_t
\]

\begin{tabular}{|c|c|}
\hline
Model & Accuracy \\
\hline
Baseline & 82.4 \\
Ours & 88.6 \\
\hline
\end{tabular}

\end{document}
"""

def test_parse_latex_string_equations():
    parsed = latex_parser.parse_latex_string(SAMPLE_LATEX)
    assert len(parsed["equations"]) >= 3
    eq_texts = " ".join(parsed["equations"])
    assert r"h_t = \mathbf{A} h_{t-1}" in eq_texts
    assert r"\mathcal{L}(\theta)" in eq_texts
    assert r"y_t = \mathbf{C} h_t" in eq_texts

def test_parse_latex_string_sections():
    parsed = latex_parser.parse_latex_string(SAMPLE_LATEX)
    sections = parsed["sections"]
    assert "Introduction" in sections
    assert "Methodology" in sections
    assert "Deep learning has revolutionized" in sections["Introduction"]

def test_parse_latex_string_tables():
    parsed = latex_parser.parse_latex_string(SAMPLE_LATEX)
    assert len(parsed["tables"]) >= 1
    assert "Accuracy" in parsed["tables"][0]["raw_table"]

def test_parse_latex_string_empty():
    parsed = latex_parser.parse_latex_string("")
    assert parsed == {"sections": {}, "equations": [], "tables": []}

def test_extract_from_tarball():
    # Create an in-memory tarball containing a .tex file
    tar_stream = io.BytesIO()
    with tarfile.open(fileobj=tar_stream, mode="w:gz") as tar:
        tex_bytes = SAMPLE_LATEX.encode("utf-8")
        tarinfo = tarfile.TarInfo(name="main.tex")
        tarinfo.size = len(tex_bytes)
        tar.addfile(tarinfo, io.BytesIO(tex_bytes))
    
    tar_data = tar_stream.getvalue()
    parsed = LaTeXParser.extract_from_tarball(tar_data)
    assert len(parsed["equations"]) >= 3
    assert "Introduction" in parsed["sections"]

def test_extract_from_gzip_fallback():
    # Create an in-memory gzipped single file
    gz_data = gzip.compress(SAMPLE_LATEX.encode("utf-8"))
    parsed = LaTeXParser.extract_from_tarball(gz_data)
    assert len(parsed["equations"]) >= 3
    assert "Introduction" in parsed["sections"]
