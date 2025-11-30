"""
Reporting router for exporting grading data.
Generates formatted Markdown tables with summary stats or JSONL for programmatic analysis.
"""
import json
from typing import List, Literal
from fastapi import APIRouter, Query, Response
from arcade_app.session_state import session_store, SessionState

router = APIRouter()


def _format_markdown_table(sessions: List[SessionState]) -> str:
    """Generates a GitHub-flavored Markdown table with summary stats."""
    
    # Filter for graded sessions
    graded_sessions = [s for s in sessions if s.last_grade]
    
    if not graded_sessions:
        return "> **No graded sessions found.** Submit some code to generate data."

    # Calculate Stats
    count = len(graded_sessions)
    avg_score = sum(s.last_grade.weighted_score for s in graded_sessions) / count
    
    # 1. Summary Header
    md = [
        "## 📊 EvalForge Grading Report",
        f"- **Total Submissions:** {count}",
        f"- **Average Weighted Score:** {avg_score:.1f}%",
        "",
        "### Detail View",
        "| Session | Track | Score | Cov | Corr | Clar | Feedback |",
        "|---|---|---|---|---|---|---|"
    ]

    # 2. Data Rows
    for sid, state in session_store._store.items():
        if state.last_grade:
            g = state.last_grade
            # Truncate session ID and comment for table readability
            sid_short = sid[:8] if len(sid) > 8 else sid
            comment_short = (g.comment[:50] + "...") if len(g.comment) > 50 else g.comment
            track = state.track or "default"
            
            row = (
                f"| `{sid_short}` | `{track}` | **{g.weighted_score:.1f}** | "
                f"{g.coverage} | {g.correctness} | {g.clarity} | {comment_short} |"
            )
            md.append(row)
    
    return "\n".join(md)


def _format_jsonl(sessions: List[SessionState]) -> str:
    """Generates NDJSON (Newline Delimited JSON) for piping to tools."""
    lines = []
    for sid, state in session_store._store.items():
        if state.last_grade:
            g = state.last_grade
            record = {
                "session_id": sid,
                "track": state.track or "default",
                "weighted_score": g.weighted_score,
                "components": {
                    "coverage": g.coverage,
                    "correctness": g.correctness,
                    "clarity": g.clarity
                },
                "comment": g.comment,
                "input_hash": state.last_graded_input_hash
            }
            lines.append(json.dumps(record))
    return "\n".join(lines)


@router.get("/dev/grades/export")
async def export_grades(
    format: Literal["md", "jsonl"] = Query("md", description="Output format: md (Markdown) or jsonl"),
):
    """
    Export all grades from the current session store.
    
    - **md**: GitHub-flavored Markdown table with summary statistics
    - **jsonl**: Newline-delimited JSON for programmatic processing
    
    Note: In production, this would query a database. Currently uses in-memory session store.
    """
    # Get all sessions from the store
    sessions = list(session_store._store.values())

    if format == "md":
        content = _format_markdown_table(sessions)
        return Response(content=content, media_type="text/markdown")
    
    elif format == "jsonl":
        content = _format_jsonl(sessions)
        return Response(content=content, media_type="application/x-ndjson")
