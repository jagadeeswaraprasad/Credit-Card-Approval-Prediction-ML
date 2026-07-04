"""SmartCredit AI - Prediction History Service"""

import csv
import io
import json
from utils.db import get_connection
from config import Config

SORTABLE_COLUMNS = {
    "date": "created_at",
    "name": "applicant_name",
    "prediction": "prediction",
    "confidence": "confidence_score",
    "risk": "risk_category",
}


def get_history(user_id: int, page: int = 1, search: str = "", status_filter: str = "",
                 risk_filter: str = "", sort_by: str = "date", sort_dir: str = "desc"):
    conn = get_connection()
    try:
        clauses = ["user_id = ?"]
        params = [user_id]

        if search:
            clauses.append("applicant_name LIKE ?")
            params.append(f"%{search}%")
        if status_filter:
            clauses.append("prediction = ?")
            params.append(status_filter)
        if risk_filter:
            clauses.append("risk_category = ?")
            params.append(risk_filter)

        where_clause = " AND ".join(clauses)
        sort_col = SORTABLE_COLUMNS.get(sort_by, "created_at")
        sort_dir = "DESC" if sort_dir.lower() != "asc" else "ASC"

        total = conn.execute(
            f"SELECT COUNT(*) as c FROM predictions WHERE {where_clause}", params
        ).fetchone()["c"]

        page_size = Config.HISTORY_PAGE_SIZE
        offset = (page - 1) * page_size

        rows = conn.execute(
            f"""SELECT * FROM predictions WHERE {where_clause}
                ORDER BY {sort_col} {sort_dir} LIMIT ? OFFSET ?""",
            params + [page_size, offset],
        ).fetchall()

        records = [dict(r) for r in rows]
        total_pages = max(1, (total + page_size - 1) // page_size)

        return {
            "records": records,
            "total": total,
            "page": page,
            "total_pages": total_pages,
            "page_size": page_size,
        }
    finally:
        conn.close()


def delete_prediction(user_id: int, prediction_id: int) -> bool:
    conn = get_connection()
    try:
        cur = conn.execute(
            "DELETE FROM predictions WHERE id = ? AND user_id = ?", (prediction_id, user_id)
        )
        conn.commit()
        return cur.rowcount > 0
    finally:
        conn.close()


def export_csv(user_id: int) -> str:
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM predictions WHERE user_id = ? ORDER BY created_at DESC", (user_id,)
        ).fetchall()
    finally:
        conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "ID", "Applicant Name", "Prediction", "Approval Probability (%)",
        "Rejection Probability (%)", "Confidence Score (%)", "Risk Category",
        "Model Used", "Date",
    ])
    for r in rows:
        writer.writerow([
            r["id"], r["applicant_name"], r["prediction"], r["approval_probability"],
            r["rejection_probability"], r["confidence_score"], r["risk_category"],
            r["model_used"], r["created_at"],
        ])
    return output.getvalue()
