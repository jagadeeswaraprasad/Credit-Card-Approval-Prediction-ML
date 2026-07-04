# System Architecture

**Project:** SmartCredit AI — Credit Card Approval Prediction
**Phase:** 3. Project Design Phase

---

## 1. Architectural Style
SmartCredit AI follows a **layered, modular monolith** architecture within a single
Flask application, cleanly separating concerns into distinct packages:

```
Client (Browser)
      │
      ▼
Flask Routes (routes/)         ── HTTP layer: request/response, session handling
      │
      ▼
Services (services/)           ── Business logic: auth, predictions, history, stats
      │
      ▼
ML Engine (ml/)                ── train.py / predict.py — model inference & explainability
      │
      ▼
Data Layer (utils/db.py)       ── SQLite persistence (users, predictions, audit_logs)
```

## 2. Component Overview

| Component | Responsibility |
|---|---|
| `app.py` | Application factory; registers blueprints, error handlers, context processors |
| `config.py` | Centralised configuration (paths, session settings) |
| `routes/` | Thin HTTP-facing blueprints: `main`, `auth`, `dashboard`, `prediction`, `history`, `model` |
| `services/` | Business logic layer, isolated from Flask request objects where possible |
| `ml/` | Data generation, training pipeline, and explainable inference engine |
| `utils/` | Cross-cutting concerns: database connection/schema, validators, logging, decorators |
| `templates/` + `static/` | Server-rendered Jinja2 views with a custom vanilla CSS/JS design system |

## 3. Request Lifecycle (Example: New Prediction)
1. User submits the "New Prediction" form → `POST /api/predict` (`routes/prediction_routes.py`).
2. Route validates input (`utils/validators.py`) and delegates to
   `services/prediction_service.py`.
3. Service calls `ml/predict.py`, which loads the persisted model bundle
   (`models/model.pkl`, `scaler.pkl`, `encoders.pkl`) and returns an explainable result.
4. Service persists the prediction to SQLite (`predictions` table) and logs the action
   to `audit_logs`.
5. Route returns JSON; the frontend redirects to the result page.

## 4. Deployment View
Single-process Flask application (development server via `python app.py`, or a WSGI
server such as Gunicorn in production), with a local SQLite file and locally-stored
model artefacts — no external services required.

## 5. Key Design Decisions
- **Application factory + blueprints** for testability and clean route registration.
- **Service layer** to keep business logic independent of Flask specifics.
- **Model artefacts persisted to disk** (`joblib`) so inference does not require
  retraining at request time.
- **SQLite only**, per project constraints, with a schema designed so the service
  layer could be pointed at another RDBMS with minimal change.

## 6. Diagram References
See `Database_Design.md`, `Use_Case.md`, and `ER_Diagram.md` in this same folder for
complementary design artefacts.
