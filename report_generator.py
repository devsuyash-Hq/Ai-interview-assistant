"""
Report Generator
================
Builds and saves the final mock-interview report: per-question scores,
strengths/improvements, and the AI coach's overall summary.
"""

import os
from datetime import datetime


def save_report(qa_records: list, overall_summary: str, output_dir: str = "reports") -> str:
    """
    Write a formatted .txt report of the full interview session.

    Returns:
        The path to the saved report file.
    """
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(output_dir, f"interview_report_{timestamp}.txt")

    scores = [r["evaluation"].get("score", 0) for r in qa_records if r.get("evaluation")]
    avg_score = round(sum(scores) / len(scores), 1) if scores else 0

    lines = [
        "=" * 60,
        "AI INTERVIEW ASSISTANT — MOCK INTERVIEW REPORT",
        "=" * 60,
        f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"Average Score: {avg_score}/10",
        "",
    ]

    for i, record in enumerate(qa_records, 1):
        e = record.get("evaluation", {})
        lines.extend([
            f"Q{i}: {record['question']}",
            f"Your Answer: {record['answer']}",
            f"Score: {e.get('score', 'N/A')}/10",
            f"Strengths: {', '.join(e.get('strengths', []))}",
            f"Improvements: {', '.join(e.get('improvements', []))}",
            f"Tip: {e.get('ideal_answer_tip', '')}",
            "-" * 60,
        ])

    lines.append("\nOVERALL FEEDBACK:")
    lines.append(overall_summary)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return filepath
