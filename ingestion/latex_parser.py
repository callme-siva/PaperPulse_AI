import re
import tarfile
import gzip
import io
from typing import Dict, List, Any, Optional

class LaTeXParser:
    """Extracts clean section hierarchy, math equations, and tables from raw LaTeX."""
    
    @staticmethod
    def extract_from_tarball(tar_bytes: bytes) -> Dict[str, Any]:
        """Extracts and merges all .tex files from an arXiv source tarball."""
        tex_contents = []
        try:
            with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode="r:*") as tar:
                for member in tar.getmembers():
                    if member.name.endswith(".tex"):
                        f = tar.extractfile(member)
                        if f:
                            try:
                                tex_contents.append(f.read().decode("utf-8", errors="ignore"))
                            except Exception:
                                pass
        except Exception:
            # Fallback if single gzipped file
            try:
                content = gzip.decompress(tar_bytes).decode("utf-8", errors="ignore")
                tex_contents.append(content)
            except Exception:
                pass

        full_latex = "\n\n".join(tex_contents)
        return LaTeXParser.parse_latex_string(full_latex)

    @staticmethod
    def parse_latex_string(latex_text: str) -> Dict[str, Any]:
        if not latex_text:
            return {"sections": {}, "equations": [], "tables": []}

        # 1. Extract Equations
        equation_patterns = [
            r"\\begin\{equation\*?\}(.*?)\\end\{equation\*?\}",
            r"\\begin\{align\*?\}(.*?)\\end\{align\*?\}",
            r"\\\[(.*?)\\\]"
        ]
        equations = []
        for pat in equation_patterns:
            matches = re.findall(pat, latex_text, re.DOTALL)
            for m in matches:
                clean_eq = m.strip()
                if clean_eq and len(clean_eq) > 3 and clean_eq not in equations:
                    equations.append(clean_eq[:300])

        # 2. Extract Sections
        sections = {}
        section_splits = re.split(r"\\section\*?\{([^}]+)\}", latex_text)
        if len(section_splits) > 1:
            for i in range(1, len(section_splits), 2):
                sec_name = section_splits[i].strip()
                sec_content = section_splits[i+1].strip() if i+1 < len(section_splits) else ""
                # Strip basic LaTeX commands
                clean_sec_text = re.sub(r"\\[a-zA-Z]+(\[[^\]]*\])?(\{[^}]*\})?", " ", sec_content)
                clean_sec_text = re.sub(r"\s+", " ", clean_sec_text).strip()
                sections[sec_name] = clean_sec_text[:2000]

        # 3. Extract Tables (rough tabular content)
        tables = []
        table_matches = re.findall(r"\\begin\{tabular\}(.*?)\\end\{tabular\}", latex_text, re.DOTALL)
        for t in table_matches[:5]:
            tables.append({"raw_table": t.strip()[:500]})

        return {
            "sections": sections,
            "equations": equations[:15],
            "tables": tables
        }

latex_parser = LaTeXParser()
