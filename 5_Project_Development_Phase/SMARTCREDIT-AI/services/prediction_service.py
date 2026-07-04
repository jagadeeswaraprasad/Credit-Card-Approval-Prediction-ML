"""SmartCredit AI - Prediction Service"""

import json
from utils.db import get_connection
from ml.predict import predict as run_prediction


def make_prediction(user_id: int, form_data: dict) -> dict:
    result = run_prediction(form_data)

    conn = get_connection()
    try:
        cur = conn.execute(
            """INSERT INTO predictions
               (user_id, applicant_name, input_json, prediction, approval_probability,
                rejection_probability, confidence_score, risk_category, top_factors_json,
                recommendation_json, model_used)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                user_id,
                form_data.get("Applicant_Name", "Applicant"),
                json.dumps(form_data),
                result["prediction"],
                result["approval_probability"],
                result["rejection_probability"],
                result["confidence_score"],
                result["risk_category"],
                json.dumps(result["top_factors"]),
                json.dumps(result["recommendation"]),
                result["model_used"],
            ),
        )
        conn.commit()
        result["prediction_id"] = cur.lastrowid
    finally:
        conn.close()

    result["applicant_name"] = form_data.get("Applicant_Name", "Applicant")
    return result


def get_prediction(prediction_id: int, user_id: int):
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM predictions WHERE id = ? AND user_id = ?", (prediction_id, user_id)
        ).fetchone()
        if not row:
            return None
        record = dict(row)
        record["input_json"] = json.loads(record["input_json"])
        record["top_factors_json"] = json.loads(record["top_factors_json"])
        record["recommendation"] = json.loads(record.get("recommendation_json") or "{}")
        return record
    finally:
        conn.close()
