# Demo Guide

**Project:** SmartCredit AI — Credit Card Approval Prediction
**Phase:** 8. Project Demonstration

---

## 1. Pre-Demo Checklist
- [ ] Application dependencies installed (`pip install -r requirements.txt`)
- [ ] Model artefacts present in `models/` (or re-run `python ml/train.py`)
- [ ] Demo data seeded (`python seed_demo_data.py`) so dashboard/history aren't empty
- [ ] Application running (`python app.py`) and reachable at `http://localhost:5000`
- [ ] Browser zoom/resolution set for clear screen sharing

## 2. Suggested Demo Flow (≈8-10 minutes)

### Step 1 — Landing Page (1 min)
- Show the hero section, live risk-assessment preview card, and model benchmark table.
- Point out the "How AI Works" section explaining the 4-stage explainability pipeline.

### Step 2 — Account & Login (1 min)
- Register a new account live, or log in with the demo account
  (`demo@smartcredit.ai` / `Demo1234`).

### Step 3 — Dashboard (1-2 min)
- Walk through total predictions, approval/rejection rate, average confidence.
- Highlight the 14-day trend chart and risk distribution donut chart.

### Step 4 — New Prediction: Approval Case (2 min)
- Submit an application with a strong profile (high income, high credit score, low
  debt) and show the animated loading sequence.
- On the result page, explain: decision, confidence meter, probability bars, top
  contributing factors, and recommendation/next steps.

### Step 5 — New Prediction: Rejection Case (2 min)
- Submit a weaker profile (low credit score, high existing debt, prior defaults).
- Show how the top contributing factors and recommendation change accordingly —
  emphasise this is never a "black box" decision.

### Step 6 — Prediction History (1-2 min)
- Demonstrate search, filter by risk/result, sort, CSV export, and record deletion.

### Step 7 — Model Performance (1 min)
- Show the model comparison table, confusion matrix, ROC curve, and feature
  importance chart for the deployed model.

### Step 8 — Theme Toggle & Responsiveness (30 sec)
- Toggle dark/light mode.
- Resize the browser (or use device toolbar) to show the responsive sidebar.

## 3. Anticipated Questions & Answers
| Question | Suggested Answer |
|---|---|
| "Why not use a real public dataset?" | The build environment had no internet access, so a statistically-grounded synthetic dataset was generated using real underwriting heuristics; the pipeline works unchanged with a real CSV (see README). |
| "Why is XGBoost sometimes a fallback model?" | If `xgboost` isn't installable in a given environment, the pipeline automatically substitutes a `GradientBoostingClassifier` so training never breaks. |
| "How is explainability computed?" | Per-applicant feature contributions are derived from the model's learned weights/importances combined with the applicant's standardised feature values — see `ml/predict.py`. |
| "Is this production-ready?" | It's a reference-grade platform demonstrating the full ML + web lifecycle; production use would need further compliance, fair-lending review, and infrastructure hardening. |

See `Presentation_Notes.md` for slide-level talking points.
