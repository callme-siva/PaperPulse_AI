import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from config import SQLITE_DB_PATH
from models import RawPaper, ExtractedMetric, DebateTurn, ReviewVerdict, RetrievedContext

class AcademicDatabase:
    def __init__(self, db_path=SQLITE_DB_PATH):
        self.db_path = str(db_path)
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Papers table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS papers (
                    paper_id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    authors TEXT NOT NULL,
                    abstract TEXT NOT NULL,
                    categories TEXT NOT NULL,
                    primary_category TEXT NOT NULL,
                    published_date TEXT NOT NULL,
                    arxiv_url TEXT NOT NULL,
                    pdf_url TEXT NOT NULL,
                    github_url TEXT,
                    citation_count INTEGER DEFAULT 0,
                    has_latex_source INTEGER DEFAULT 0,
                    equations TEXT,
                    created_at TEXT NOT NULL
                )
            """)

            # Extracted SOTA Metrics table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS metrics (
                    metric_id TEXT PRIMARY KEY,
                    paper_id TEXT NOT NULL,
                    dataset_name TEXT NOT NULL,
                    metric_name TEXT NOT NULL,
                    paper_score REAL NOT NULL,
                    baseline_name TEXT,
                    baseline_score REAL,
                    delta REAL,
                    compute_claim TEXT,
                    source_context_id TEXT,
                    source_latex_span TEXT,
                    FOREIGN KEY(paper_id) REFERENCES papers(paper_id)
                )
            """)

            # Multi-Agent Debate Turns table (with provable grounding context)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS debate_turns (
                    turn_id TEXT PRIMARY KEY,
                    paper_id TEXT NOT NULL,
                    round_number INTEGER NOT NULL,
                    speaker TEXT NOT NULL,
                    argument_title TEXT NOT NULL,
                    argument_text TEXT NOT NULL,
                    cited_section TEXT,
                    key_quote TEXT,
                    grounding_contexts TEXT,
                    cited_context_ids TEXT,
                    timestamp TEXT NOT NULL,
                    FOREIGN KEY(paper_id) REFERENCES papers(paper_id)
                )
            """)

            # Peer Review Verdicts table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reviews (
                    verdict_id TEXT PRIMARY KEY,
                    paper_id TEXT UNIQUE NOT NULL,
                    overall_score REAL NOT NULL,
                    novelty_score REAL NOT NULL,
                    rigor_score REAL NOT NULL,
                    baseline_fairness_score REAL NOT NULL,
                    reproducibility_score REAL NOT NULL,
                    recommendation TEXT NOT NULL,
                    executive_summary TEXT NOT NULL,
                    strengths TEXT NOT NULL,
                    weaknesses TEXT NOT NULL,
                    open_questions TEXT NOT NULL,
                    generated_at TEXT NOT NULL,
                    FOREIGN KEY(paper_id) REFERENCES papers(paper_id)
                )
            """)

            # Watchlist Topics
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS watchlist_topics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic TEXT UNIQUE NOT NULL,
                    category TEXT NOT NULL,
                    added_at TEXT NOT NULL
                )
            """)
            conn.commit()

    # ------------------ PAPER OPERATIONS ------------------
    def save_paper(self, paper: RawPaper) -> bool:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO papers (
                        paper_id, title, authors, abstract, categories, primary_category,
                        published_date, arxiv_url, pdf_url, github_url, citation_count,
                        has_latex_source, equations, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(paper_id) DO UPDATE SET
                        citation_count = excluded.citation_count,
                        github_url = excluded.github_url
                """, (
                    paper.paper_id, paper.title, json.dumps(paper.authors), paper.abstract,
                    json.dumps(paper.categories), paper.primary_category, paper.published_date,
                    paper.arxiv_url, paper.pdf_url, paper.github_url, paper.citation_count,
                    1 if paper.has_latex_source else 0, json.dumps(paper.equations), paper.created_at
                ))
                conn.commit()
                return True
        except Exception as e:
            print(f"[DB Error] save_paper failed: {e}")
            return False

    def get_paper(self, paper_id: str) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM papers WHERE paper_id = ?", (paper_id,))
            row = cursor.fetchone()
            if not row:
                return None
            data = dict(row)
            data["authors"] = json.loads(data["authors"]) if data["authors"] else []
            data["categories"] = json.loads(data["categories"]) if data["categories"] else []
            data["equations"] = json.loads(data["equations"]) if data["equations"] else []
            return data

    def get_all_papers(self, category: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if category and category != "All":
                cursor.execute("SELECT * FROM papers WHERE primary_category = ? ORDER BY published_date DESC LIMIT ?", (category, limit))
            else:
                cursor.execute("SELECT * FROM papers ORDER BY published_date DESC LIMIT ?", (limit,))
            rows = cursor.fetchall()
            papers = []
            for r in rows:
                p = dict(r)
                p["authors"] = json.loads(p["authors"]) if p["authors"] else []
                p["categories"] = json.loads(p["categories"]) if p["categories"] else []
                p["equations"] = json.loads(p["equations"]) if p["equations"] else []
                papers.append(p)
            return papers

    # ------------------ SOTA METRICS ------------------
    def save_metric(self, metric: ExtractedMetric) -> bool:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO metrics (
                        metric_id, paper_id, dataset_name, metric_name, paper_score,
                        baseline_name, baseline_score, delta, compute_claim,
                        source_context_id, source_latex_span
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    metric.metric_id, metric.paper_id, metric.dataset_name, metric.metric_name,
                    metric.paper_score, metric.baseline_name, metric.baseline_score,
                    metric.delta, metric.compute_claim, metric.source_context_id, metric.source_latex_span
                ))
                conn.commit()
                return True
        except Exception as e:
            print(f"[DB Error] save_metric failed: {e}")
            return False

    def get_metrics_for_paper(self, paper_id: str) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM metrics WHERE paper_id = ?", (paper_id,))
            return [dict(r) for r in cursor.fetchall()]

    def get_all_metrics(self) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT m.*, p.title as paper_title, p.arxiv_url
                FROM metrics m
                JOIN papers p ON m.paper_id = p.paper_id
                ORDER BY m.dataset_name, m.paper_score DESC
            """)
            return [dict(r) for r in cursor.fetchall()]

    # ------------------ DEBATE TURNS ------------------
    def save_debate_turn(self, turn: DebateTurn) -> bool:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                g_contexts = [c.dict() if hasattr(c, "dict") else c for c in turn.grounding_contexts]
                cursor.execute("""
                    INSERT OR REPLACE INTO debate_turns (
                        turn_id, paper_id, round_number, speaker, argument_title,
                        argument_text, cited_section, key_quote, grounding_contexts,
                        cited_context_ids, timestamp
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    turn.turn_id, turn.paper_id, turn.round_number, turn.speaker,
                    turn.argument_title, turn.argument_text, turn.cited_section,
                    turn.key_quote, json.dumps(g_contexts), json.dumps(turn.cited_context_ids),
                    turn.timestamp
                ))
                conn.commit()
                return True
        except Exception as e:
            print(f"[DB Error] save_debate_turn failed: {e}")
            return False

    def get_debate_turns(self, paper_id: str) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM debate_turns WHERE paper_id = ? ORDER BY round_number ASC, turn_id ASC", (paper_id,))
            rows = cursor.fetchall()
            turns = []
            for r in rows:
                t = dict(r)
                t["grounding_contexts"] = json.loads(t["grounding_contexts"]) if t["grounding_contexts"] else []
                t["cited_context_ids"] = json.loads(t["cited_context_ids"]) if t["cited_context_ids"] else []
                turns.append(t)
            return turns

    # ------------------ REVIEW VERDICTS ------------------
    def save_review(self, review: ReviewVerdict) -> bool:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO reviews (
                        verdict_id, paper_id, overall_score, novelty_score, rigor_score,
                        baseline_fairness_score, reproducibility_score, recommendation,
                        executive_summary, strengths, weaknesses, open_questions, generated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    review.verdict_id, review.paper_id, review.overall_score, review.novelty_score,
                    review.rigor_score, review.baseline_fairness_score, review.reproducibility_score,
                    review.recommendation, review.executive_summary, json.dumps(review.strengths),
                    json.dumps(review.weaknesses), json.dumps(review.open_questions), review.generated_at
                ))
                conn.commit()
                return True
        except Exception as e:
            print(f"[DB Error] save_review failed: {e}")
            return False

    def get_review(self, paper_id: str) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM reviews WHERE paper_id = ?", (paper_id,))
            row = cursor.fetchone()
            if not row:
                return None
            data = dict(row)
            data["strengths"] = json.loads(data["strengths"]) if data["strengths"] else []
            data["weaknesses"] = json.loads(data["weaknesses"]) if data["weaknesses"] else []
            data["open_questions"] = json.loads(data["open_questions"]) if data["open_questions"] else []
            return data

    def clear_all(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM papers")
            cursor.execute("DELETE FROM metrics")
            cursor.execute("DELETE FROM debate_turns")
            cursor.execute("DELETE FROM reviews")
            conn.commit()

db = AcademicDatabase()
