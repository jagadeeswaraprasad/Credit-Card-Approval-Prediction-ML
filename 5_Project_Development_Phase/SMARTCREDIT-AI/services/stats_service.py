"""SmartCredit AI - Dashboard Statistics Service"""

from utils.db import get_connection


def get_dashboard_stats(user_id: int) -> dict:
    conn = get_connection()
    try:
        total = conn.execute(
            "SELECT COUNT(*) c FROM predictions WHERE user_id = ?", (user_id,)
        ).fetchone()["c"]

        approved = conn.execute(
            "SELECT COUNT(*) c FROM predictions WHERE user_id = ? AND prediction = 'Approved'", (user_id,)
        ).fetchone()["c"]

        rejected = total - approved

        avg_confidence = conn.execute(
            "SELECT AVG(confidence_score) a FROM predictions WHERE user_id = ?", (user_id,)
        ).fetchone()["a"] or 0

        approval_rate = round((approved / total) * 100, 1) if total else 0
        rejection_rate = round((rejected / total) * 100, 1) if total else 0

        recent = conn.execute(
            """SELECT id, applicant_name, prediction, confidence_score, risk_category, created_at
               FROM predictions WHERE user_id = ? ORDER BY created_at DESC LIMIT 6""",
            (user_id,),
        ).fetchall()

        risk_breakdown = conn.execute(
            """SELECT risk_category, COUNT(*) c FROM predictions
               WHERE user_id = ? GROUP BY risk_category""",
            (user_id,),
        ).fetchall()

        trend = conn.execute(
            """SELECT date(created_at) d, COUNT(*) c,
                      SUM(CASE WHEN prediction = 'Approved' THEN 1 ELSE 0 END) approved
               FROM predictions WHERE user_id = ?
               GROUP BY date(created_at) ORDER BY d DESC LIMIT 14""",
            (user_id,),
        ).fetchall()

        return {
            "total_predictions": total,
            "approved": approved,
            "rejected": rejected,
            "approval_rate": approval_rate,
            "rejection_rate": rejection_rate,
            "avg_confidence": round(avg_confidence, 1),
            "recent_predictions": [dict(r) for r in recent],
            "risk_breakdown": {r["risk_category"]: r["c"] for r in risk_breakdown},
            "trend": [dict(r) for r in reversed(trend)],
        }
    finally:
        conn.close()
