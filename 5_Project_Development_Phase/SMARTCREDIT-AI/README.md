# SmartCredit AI
### Enterprise Credit Card Approval & Risk Assessment Platform

SmartCredit AI is a full-stack, production-styled web application that predicts whether a
credit card application should be **Approved** or **Rejected**, using an ensemble of machine
learning models — and explains *why* on every single decision.

---

## ✨ Key Features

### Machine Learning
- Full pipeline: data cleaning → feature engineering → encoding → scaling → train/test split
- **4 models trained and compared**: Logistic Regression, Decision Tree, Random Forest, XGBoost
- Automatic **best-model selection** by ROC-AUC on a held-out test set
- Metrics tracked: Accuracy, Precision, Recall, F1 Score, ROC-AUC, Confusion Matrix, ROC Curve
- Model, scaler and encoders persisted with `joblib` (`models/model.pkl`)

### Explainable AI
- Every prediction returns: **Approval Probability**, **Rejection Probability**,
  **Confidence Score**, **Risk Category** (Low / Medium / High) and the **Top 5 Contributing
  Factors** for that specific applicant — never a bare Approved/Rejected label
- Actionable **recommendation and next-step guidance** tailored to the outcome

### Web Application
- Custom, dependency-free **glassmorphism UI** — no Bootstrap — inspired by Stripe / Linear / Notion / Apple
- **Dark & Light mode** with persistent preference
- Fully responsive, mobile-friendly layout with a collapsible sidebar
- Toast notifications, animated counters, skeleton/loading states, empty states
- **7 complete pages**: Landing, Login/Register, Dashboard, New Prediction, Result,
  Prediction History, Model Performance
- Lightweight **canvas-based charting library** (no external chart dependency) powering
  gauges, donuts, bar charts, horizontal bar charts and line/trend charts

### Backend & Data
- Flask application factory with **blueprints** (auth, dashboard, prediction, history, model, main)
- **SQLite only**, as required — three tables: `users`, `predictions`, `audit_logs`
- Secure password hashing (Werkzeug), session-based authentication, "remember me"
- Full **audit logging** of registration, login, predictions, deletions and exports
- Prediction History: **search, filter (result/risk), sort, paginate, export CSV, delete**
- Server-side + client-side form validation with clear error messaging

---

## 🗂 Project Structure

```
smartcredit-ai/
├── app.py                     # Flask application factory & entrypoint
├── config.py                  # Centralised configuration
├── requirements.txt
├── seed_demo_data.py          # Optional: seeds a demo account + sample history
│
├── ml/                        # Machine learning pipeline
│   ├── data_generator.py      # Synthetic-but-realistic dataset generator
│   ├── train.py                # Full training/comparison/selection pipeline
│   └── predict.py             # Explainable inference engine
│
├── routes/                    # Flask blueprints (HTTP layer only)
│   ├── main_routes.py
│   ├── auth_routes.py
│   ├── dashboard_routes.py
│   ├── prediction_routes.py
│   ├── history_routes.py
│   └── model_routes.py
│
├── services/                  # Business logic layer
│   ├── auth_service.py
│   ├── prediction_service.py
│   ├── history_service.py
│   └── stats_service.py
│
├── utils/                     # Cross-cutting utilities
│   ├── db.py                  # SQLite connection + schema
│   ├── validators.py
│   ├── logger.py
│   └── decorators.py
│
├── templates/                 # Jinja2 templates
│   ├── base.html               # Authenticated app shell (sidebar layout)
│   ├── landing.html
│   ├── login.html / register.html / forgot_password.html
│   ├── dashboard.html
│   ├── new_prediction.html
│   ├── result.html
│   ├── history.html
│   ├── model_performance.html
│   └── errors/ (404.html, 500.html)
│
├── static/
│   ├── css/  (main.css, landing.css, auth.css)
│   └── js/   (main.js, charts.js, prediction.js, history.js)
│
├── data/
│   └── credit_card_approval.csv   # Generated training dataset
│
├── models/                    # Generated at training time
│   ├── model.pkl
│   ├── scaler.pkl
│   ├── encoders.pkl
│   ├── model_metadata.json
│   ├── model_metrics.json
│   └── feature_importance.json
│
├── database/
│   └── smartcredit.db         # SQLite database (created on first run)
│
└── logs/
    └── application.log
```

---

## 🚀 Setup Instructions

### 1. Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```
> **Note on XGBoost:** if `xgboost` cannot be installed on your system, the training script
> automatically falls back to a `GradientBoostingClassifier` (a robust equivalent) so the
> pipeline still runs end-to-end. Install `xgboost` for the full 4-model comparison.

### 3. Generate the dataset & train the models
```bash
python ml/data_generator.py     # creates data/credit_card_approval.csv
python ml/train.py              # trains, compares, and saves the best model to /models
```

### 4. (Optional) Seed demo data
```bash
python seed_demo_data.py
```
This creates a demo account (`demo@smartcredit.ai` / `Demo1234`) with 25 sample predictions,
so the Dashboard, History and Model Performance pages have data immediately.

### 5. Run the application
```bash
python app.py
```
Visit **http://localhost:5000**

---

## 📊 About the Dataset

Public credit-approval datasets are not reachable from an offline build environment, so
`ml/data_generator.py` synthesises a realistic equivalent dataset using well-established
underwriting heuristics (credit score, debt-to-income ratio, employment stability, prior
defaults, etc.) combined with randomised noise — so the approval labels are realistic and
**not trivially separable**; models genuinely have to learn the decision boundary (achieving
~87-89% accuracy / ~93-96% ROC-AUC across the four models in testing).

To use a real dataset (e.g. the UCI "Credit Approval" or Kaggle "Credit Card Approval
Prediction" datasets), simply replace `data/credit_card_approval.csv` with your own file
using the same column schema (see `ml/train.py` → `NUMERIC_COLS` / `CATEGORICAL_COLS`) and
re-run `python ml/train.py`.

---

## 🔐 Default Login (after seeding)

| Field | Value |
|---|---|
| Email | demo@smartcredit.ai |
| Password | Demo1234 |

Or simply register a new account from the **Get Started** button on the landing page.

---

## 🧠 Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3 (custom glassmorphism design system), Vanilla JavaScript |
| Backend | Python, Flask (application-factory + blueprints) |
| ML | scikit-learn, XGBoost (with graceful fallback), Pandas, NumPy |
| Persistence | SQLite (users, predictions, audit logs) |
| Model Artefacts | joblib (`model.pkl`, `scaler.pkl`, `encoders.pkl`) |

---

## 📝 Notes

- This is a demonstration platform. It is **not** a real financial institution and should not
  be used to make real-world credit decisions without further validation, fair-lending review,
  and regulatory compliance work.
- All data — including the demo account's prediction history — is stored locally in
  `database/smartcredit.db`. Delete this file to reset the application.
