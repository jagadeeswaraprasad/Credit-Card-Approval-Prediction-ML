# Project Plan

**Project:** SmartCredit AI — Credit Card Approval Prediction
**Phase:** 4. Project Planning Phase

---

## 1. Objective
Deliver a fully functional, explainable credit card approval prediction platform,
covering data preparation, model development, backend/frontend implementation,
testing, and documentation.

## 2. Scope
In scope: dataset preparation, multi-model training and comparison, explainable
inference, Flask web application (auth, dashboard, prediction, history, model
performance), SQLite persistence, and documentation.

Out of scope: production deployment/hosting, third-party KYC integration, real
banking-core integration.

## 3. Work Breakdown Structure (WBS)
1. Requirement Analysis
2. System & Database Design
3. Dataset Preparation & Cleaning
4. Model Training, Evaluation & Selection
5. Backend Development (Flask: routes, services, utils)
6. Frontend Development (templates, CSS design system, JS)
7. Integration (ML engine ↔ backend ↔ frontend)
8. Testing (unit, functional, UI)
9. Documentation
10. Demonstration Preparation

## 4. Resource Plan
| Role | Responsibility |
|---|---|
| ML Engineer | Data pipeline, model training/evaluation, explainability logic |
| Backend Developer | Flask routes, services, database layer, auth, security |
| Frontend Developer | Templates, CSS design system, JS interactivity, charts |
| QA / Tester | Test case design, functional and regression testing |
| Documentation Lead | SRS, user manual, API docs, demo materials |

## 5. Risk Register
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Public dataset unavailable in build environment | Medium | Medium | Use a statistically-grounded synthetic dataset with realistic underwriting heuristics |
| XGBoost unavailable in target environment | Low | Low | Automatic fallback to GradientBoostingClassifier |
| Scope creep on UI polish | Medium | Medium | Time-box design iterations; use a defined design system |

## 6. Assumptions
- SQLite is sufficient for the expected data volume of this project.
- A single-server Flask deployment model is acceptable for the current scope.

## 7. Dependencies
- Python 3.10+, Flask, scikit-learn, XGBoost, Pandas, NumPy, joblib.

See `Milestones.md` and `Timeline.md` for scheduling detail.
