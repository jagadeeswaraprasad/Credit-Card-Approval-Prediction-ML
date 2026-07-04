# Entity-Relationship (ER) Diagram

**Project:** SmartCredit AI — Credit Card Approval Prediction
**Phase:** 3. Project Design Phase

---

## 1. Entities & Attributes

**USERS**
- id (PK)
- full_name
- email (unique)
- password_hash
- created_at
- last_login

**PREDICTIONS**
- id (PK)
- user_id (FK → USERS.id)
- applicant_name
- input_json
- prediction
- approval_probability
- rejection_probability
- confidence_score
- risk_category
- top_factors_json
- recommendation_json
- model_used
- created_at

**AUDIT_LOGS**
- id (PK)
- user_id (FK → USERS.id, nullable)
- action
- details
- ip_address
- created_at

## 2. Relationships
- `USERS (1) ──── (N) PREDICTIONS` — a user can have many predictions; each
  prediction belongs to exactly one user. Cascade delete: removing a user removes
  their predictions.
- `USERS (1) ──── (N) AUDIT_LOGS` — a user can generate many audit log entries;
  each entry references at most one user. On user deletion, `user_id` is set to NULL.

## 3. Textual ER Diagram

```
┌───────────────────┐        1        N ┌───────────────────────┐
│       USERS        │───────────────────│      PREDICTIONS        │
├───────────────────┤                    ├───────────────────────┤
│ PK id               │                    │ PK id                    │
│    full_name        │                    │ FK user_id               │
│    email (unique)   │                    │    applicant_name        │
│    password_hash    │                    │    input_json            │
│    created_at       │                    │    prediction             │
│    last_login       │                    │    approval_probability  │
└───────────────────┘                    │    rejection_probability │
          │ 1                              │    confidence_score      │
          │                                │    risk_category         │
          │ N                              │    top_factors_json      │
┌───────────────────┐                    │    recommendation_json   │
│    AUDIT_LOGS       │                    │    model_used             │
├───────────────────┤                    │    created_at             │
│ PK id               │                    └───────────────────────┘
│ FK user_id (nullable)│
│    action            │
│    details           │
│    ip_address        │
│    created_at        │
└───────────────────┘
```

## 4. Notes
- All primary keys are auto-incrementing integers, consistent with SQLite conventions.
- JSON columns are used to store variable-shape data (form inputs, explainability
  factors, recommendations) without normalising into additional tables, which is an
  appropriate trade-off for this application's read/write patterns.
