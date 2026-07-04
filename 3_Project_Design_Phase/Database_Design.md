# Database Design

**Project:** SmartCredit AI — Credit Card Approval Prediction
**Phase:** 3. Project Design Phase
**Engine:** SQLite (see `5_Project_Development_Phase/SMARTCREDIT-AI/utils/db.py`)

---

## 1. Tables

### 1.1 `users`
| Column | Type | Constraints |
|---|---|---|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| full_name | TEXT | NOT NULL |
| email | TEXT | UNIQUE, NOT NULL |
| password_hash | TEXT | NOT NULL |
| created_at | TEXT | DEFAULT (datetime('now')) |
| last_login | TEXT | nullable |

### 1.2 `predictions`
| Column | Type | Constraints |
|---|---|---|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| user_id | INTEGER | NOT NULL, FK → users(id) ON DELETE CASCADE |
| applicant_name | TEXT | |
| input_json | TEXT | NOT NULL — raw form submission |
| prediction | TEXT | NOT NULL — "Approved" / "Rejected" |
| approval_probability | REAL | NOT NULL |
| rejection_probability | REAL | NOT NULL |
| confidence_score | REAL | NOT NULL |
| risk_category | TEXT | NOT NULL — Low / Medium / High Risk |
| top_factors_json | TEXT | NOT NULL — top contributing factors |
| recommendation_json | TEXT | NOT NULL DEFAULT '{}' — next-step guidance |
| model_used | TEXT | NOT NULL |
| created_at | TEXT | DEFAULT (datetime('now')) |

### 1.3 `audit_logs`
| Column | Type | Constraints |
|---|---|---|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| user_id | INTEGER | FK → users(id) ON DELETE SET NULL |
| action | TEXT | NOT NULL |
| details | TEXT | |
| ip_address | TEXT | |
| created_at | TEXT | DEFAULT (datetime('now')) |

## 2. Indexes
- `idx_predictions_user` on `predictions(user_id)`
- `idx_audit_user` on `audit_logs(user_id)`

## 3. Relationships
- One `user` → many `predictions` (1:N, cascade delete)
- One `user` → many `audit_logs` (1:N, set null on delete)

## 4. Design Notes
- JSON columns (`input_json`, `top_factors_json`, `recommendation_json`) store
  semi-structured, prediction-specific data without requiring additional tables —
  appropriate for SQLite and the read patterns of this application.
- All timestamps default to the database server's local `datetime('now')` for
  consistency.
