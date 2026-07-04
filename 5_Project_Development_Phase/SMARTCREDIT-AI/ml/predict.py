"""
SmartCredit AI - Explainable Prediction Engine
-------------------------------------------------
Loads the trained model bundle and produces a rich, explainable prediction:
approval probability, rejection probability, confidence, risk category and
the top contributing factors for that specific applicant.
"""

import os
import json
import joblib
import numpy as np
import pandas as pd

from config import Config
from ml.train import FEATURE_ORDER, CATEGORICAL_COLS, NUMERIC_COLS

_bundle = {}


def _load_bundle():
    """Lazy-load model artefacts once and cache them in-process."""
    if _bundle:
        return _bundle
    if not os.path.exists(Config.MODEL_PATH):
        raise FileNotFoundError(
            "No trained model found. Run `python ml/train.py` first."
        )
    _bundle["model"] = joblib.load(Config.MODEL_PATH)
    _bundle["scaler"] = joblib.load(Config.SCALER_PATH)
    _bundle["encoders"] = joblib.load(Config.ENCODERS_PATH)
    with open(Config.METADATA_PATH) as f:
        _bundle["metadata"] = json.load(f)
    with open(Config.FEATURE_IMPORTANCE_PATH) as f:
        _bundle["global_importance"] = json.load(f)
    return _bundle


def reload_bundle():
    """Force a reload after retraining."""
    _bundle.clear()
    return _load_bundle()


def _risk_category(prob_approval: float) -> str:
    if prob_approval >= 0.70:
        return "Low Risk"
    if prob_approval >= 0.40:
        return "Medium Risk"
    return "High Risk"


def _derive_engineered_fields(payload: dict) -> dict:
    payload = dict(payload)
    income = float(payload.get("Annual_Income", 0)) + 1
    debt = float(payload.get("Existing_Debt", 0))
    loan = float(payload.get("Loan_Amount", 0))
    payload["Debt_To_Income_Ratio"] = round((debt + loan) / income, 3)
    return payload


def _top_factors(model, scaled_row: np.ndarray, raw_row: dict, feature_names, top_n=5):
    """
    Contribution of each feature for THIS applicant, approximated as
    (standardised value) x (global feature weight/importance) - a fast,
    dependency-free explanation technique appropriate for linear and tree
    ensemble models alike.
    """
    if hasattr(model, "coef_"):
        weights = model.coef_[0]
    elif hasattr(model, "feature_importances_"):
        weights = model.feature_importances_
    else:
        weights = np.ones(len(feature_names))

    contributions = scaled_row.flatten() * weights
    ranked_idx = np.argsort(-np.abs(contributions))[:top_n]

    factors = []
    for idx in ranked_idx:
        fname = feature_names[idx]
        direction = "Positive" if contributions[idx] > 0 else "Negative"
        factors.append({
            "feature": fname.replace("_", " "),
            "impact": direction,
            "weight": round(float(abs(contributions[idx])), 4),
            "value": raw_row.get(fname),
        })
    return factors


def predict(applicant: dict) -> dict:
    """
    applicant: dict with raw form fields matching FEATURE_ORDER (before
    Debt_To_Income_Ratio, which is derived automatically).
    """
    bundle = _load_bundle()
    model, scaler, encoders = bundle["model"], bundle["scaler"], bundle["encoders"]

    applicant = _derive_engineered_fields(applicant)

    row = {}
    for col in NUMERIC_COLS:
        row[col] = float(applicant.get(col, 0))
    for col in CATEGORICAL_COLS:
        row[col] = str(applicant.get(col, ""))

    encoded_values = []
    for col in FEATURE_ORDER:
        if col in CATEGORICAL_COLS:
            le = encoders[col]
            val = str(row[col])
            if val not in le.classes_:
                val = le.classes_[0]
            encoded_values.append(float(le.transform([val])[0]))
        else:
            encoded_values.append(float(row[col]))

    encoded_df = pd.DataFrame([encoded_values], columns=FEATURE_ORDER)
    scaled = scaler.transform(encoded_df)

    proba = model.predict_proba(scaled)[0]
    prob_rejected, prob_approved = float(proba[0]), float(proba[1])
    prediction = "Approved" if prob_approved >= 0.5 else "Rejected"
    confidence = max(prob_approved, prob_rejected)

    factors = _top_factors(model, scaled, row, FEATURE_ORDER)

    recommendation = _build_recommendation(prediction, row, factors)

    return {
        "prediction": prediction,
        "approval_probability": round(prob_approved * 100, 2),
        "rejection_probability": round(prob_rejected * 100, 2),
        "confidence_score": round(confidence * 100, 2),
        "risk_category": _risk_category(prob_approved),
        "top_factors": factors,
        "recommendation": recommendation,
        "model_used": bundle["metadata"]["best_model"],
        "debt_to_income_ratio": applicant["Debt_To_Income_Ratio"],
    }


def _build_recommendation(prediction, row, factors):
    if prediction == "Approved":
        tips = [
            "Maintain your current credit utilisation below 30% to preserve this profile.",
            "Continue making on-time payments to further improve your credit score.",
        ]
        return {
            "headline": "This application meets SmartCredit AI's underwriting criteria.",
            "next_steps": [
                "Digital KYC verification",
                "E-sign the cardmember agreement",
                "Card dispatched within 5-7 business days",
            ],
            "tips": tips,
        }
    else:
        negative = [f for f in factors if f["impact"] == "Negative"]
        tips = []
        for f in negative[:3]:
            tips.append(f"Improve '{f['feature']}' — it is currently reducing your approval odds.")
        if not tips:
            tips.append("Reduce your debt-to-income ratio and reapply after 3-6 months.")
        return {
            "headline": "This application does not currently meet the risk threshold.",
            "next_steps": [
                "Review the contributing factors below",
                "Consider a secured credit card as an alternative",
                "Reapply after improving the highlighted factors",
            ],
            "tips": tips,
        }
