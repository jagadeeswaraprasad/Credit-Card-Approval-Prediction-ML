"""
SmartCredit AI - Model Training Pipeline
------------------------------------------
Full pipeline: load -> clean -> engineer features -> encode -> scale ->
train multiple models -> evaluate -> select best -> persist artefacts.

Run:  python ml/train.py
"""

import os
import sys
import json
import joblib
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, roc_curve,
)

try:
    from xgboost import XGBClassifier
    HAS_XGBOOST = True
except ImportError:
    HAS_XGBOOST = False

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config
from ml.data_generator import save_dataset

CATEGORICAL_COLS = [
    "Gender", "Marital_Status", "Education", "Employment_Status", "Housing_Status",
]
NUMERIC_COLS = [
    "Age", "Years_Employed", "Annual_Income", "Credit_Score", "Loan_Amount",
    "Existing_Debt", "Years_At_Residence", "Dependents", "Num_Credit_Cards",
    "Previous_Defaults", "Debt_To_Income_Ratio",
]
TARGET_COL = "Approval_Status"
FEATURE_ORDER = NUMERIC_COLS + CATEGORICAL_COLS


def load_data() -> pd.DataFrame:
    if not os.path.exists(Config.DATASET_PATH):
        print("Dataset not found - generating a fresh one ...")
        save_dataset(Config.DATASET_PATH)
    return pd.read_csv(Config.DATASET_PATH)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.drop_duplicates()

    # Missing value handling: numeric -> median, categorical -> mode
    for col in NUMERIC_COLS:
        if df[col].isna().any():
            df[col] = df[col].fillna(df[col].median())
    for col in CATEGORICAL_COLS:
        if df[col].isna().any():
            df[col] = df[col].fillna(df[col].mode()[0])

    # Guard against divide-by-zero / negative artefacts recomputation
    df["Debt_To_Income_Ratio"] = (
        (df["Existing_Debt"] + df["Loan_Amount"]) / (df["Annual_Income"] + 1)
    ).round(3)

    return df


def encode_features(df: pd.DataFrame, encoders: dict = None, fit: bool = True):
    df = df.copy()
    encoders = encoders or {}
    for col in CATEGORICAL_COLS:
        if fit:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
            encoders[col] = le
        else:
            le = encoders[col]
            df[col] = df[col].astype(str).map(
                lambda v: v if v in le.classes_ else le.classes_[0]
            )
            df[col] = le.transform(df[col])
    return df, encoders


def build_models():
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Decision Tree": DecisionTreeClassifier(max_depth=8, min_samples_leaf=10, random_state=42),
        "Random Forest": RandomForestClassifier(
            n_estimators=300, max_depth=10, min_samples_leaf=5, random_state=42, n_jobs=-1
        ),
    }
    if HAS_XGBOOST:
        models["XGBoost"] = XGBClassifier(
            n_estimators=300, max_depth=5, learning_rate=0.05,
            subsample=0.9, colsample_bytree=0.9, eval_metric="logloss",
            random_state=42, use_label_encoder=False,
        )
    else:
        # Gradient Boosting is used as a robust XGBoost-equivalent stand-in
        # when the xgboost package is unavailable in the runtime environment.
        models["XGBoost (GB fallback)"] = GradientBoostingClassifier(
            n_estimators=300, max_depth=4, learning_rate=0.05, random_state=42
        )
    return models


def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    cm = confusion_matrix(y_test, y_pred)
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    return {
        "accuracy": round(accuracy_score(y_test, y_pred), 4),
        "precision": round(precision_score(y_test, y_pred), 4),
        "recall": round(recall_score(y_test, y_pred), 4),
        "f1_score": round(f1_score(y_test, y_pred), 4),
        "roc_auc": round(roc_auc_score(y_test, y_proba), 4),
        "confusion_matrix": cm.tolist(),
        "roc_curve": {"fpr": fpr.tolist()[::max(1, len(fpr)//50)], "tpr": tpr.tolist()[::max(1, len(tpr)//50)]},
    }


def get_feature_importance(model, feature_names):
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
    elif hasattr(model, "coef_"):
        importances = np.abs(model.coef_[0])
    else:
        importances = np.ones(len(feature_names))
    importances = importances / (importances.sum() + 1e-9)
    pairs = sorted(zip(feature_names, importances.tolist()), key=lambda x: x[1], reverse=True)
    return [{"feature": f, "importance": round(v, 4)} for f, v in pairs]


def train():
    os.makedirs(Config.MODELS_DIR, exist_ok=True)

    print("Step 1/6  Loading data ...")
    df = load_data()

    print("Step 2/6  Cleaning data ...")
    df = clean_data(df)

    print("Step 3/6  Encoding categorical features ...")
    X_raw = df[FEATURE_ORDER]
    y = (df[TARGET_COL] == "Approved").astype(int)
    X_encoded, encoders = encode_features(X_raw, fit=True)

    print("Step 4/6  Splitting & scaling ...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_encoded, y, test_size=0.2, random_state=42, stratify=y
    )
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    print("Step 5/6  Training & comparing models ...")
    models = build_models()
    results = {}
    trained_models = {}
    for name, model in models.items():
        model.fit(X_train_scaled, y_train)
        metrics = evaluate_model(model, X_test_scaled, y_test)
        results[name] = metrics
        trained_models[name] = model
        print(f"    {name:28s} | Acc: {metrics['accuracy']:.4f} | F1: {metrics['f1_score']:.4f} | ROC-AUC: {metrics['roc_auc']:.4f}")

    best_name = max(results, key=lambda n: results[n]["roc_auc"])
    best_model = trained_models[best_name]
    print(f"\nBest model selected: {best_name}  (ROC-AUC = {results[best_name]['roc_auc']})")

    print("Step 6/6  Persisting artefacts ...")
    joblib.dump(best_model, Config.MODEL_PATH)
    joblib.dump(scaler, Config.SCALER_PATH)
    joblib.dump(encoders, Config.ENCODERS_PATH)

    feature_importance = get_feature_importance(best_model, FEATURE_ORDER)
    with open(Config.FEATURE_IMPORTANCE_PATH, "w") as f:
        json.dump(feature_importance, f, indent=2)

    with open(Config.METRICS_PATH, "w") as f:
        json.dump(results, f, indent=2)

    metadata = {
        "best_model": best_name,
        "feature_order": FEATURE_ORDER,
        "categorical_cols": CATEGORICAL_COLS,
        "numeric_cols": NUMERIC_COLS,
        "trained_on_rows": len(df),
        "train_rows": len(X_train),
        "test_rows": len(X_test),
        "xgboost_available": HAS_XGBOOST,
        "all_models_compared": list(results.keys()),
    }
    with open(Config.METADATA_PATH, "w") as f:
        json.dump(metadata, f, indent=2)

    print("\nTraining complete. Artefacts saved to /models")
    return metadata, results


if __name__ == "__main__":
    train()
