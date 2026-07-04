# Brainstorming

**Project:** SmartCredit AI — Credit Card Approval Prediction
**Phase:** 1. Brainstorming & Ideation

---

## 1. Purpose of This Document
This document captures the initial ideation session for the SmartCredit AI project —
the problem space, candidate approaches, and the reasoning that led to the chosen direction.

## 2. Team / Contributors
| Name | Role |
|---|---|
| _TBD_ | Project Lead |
| _TBD_ | ML Engineer |
| _TBD_ | Full-Stack Developer |
| _TBD_ | UI/UX Designer |

## 3. Problem Space Exploration
- Manual credit card approval review is slow, inconsistent, and prone to human bias.
- Financial institutions need a fast, data-driven, and **explainable** way to assess
  applicant risk instead of a rules-only checklist.
- Applicants receiving a plain "Rejected" with no reasoning creates a poor experience
  and compliance risk (regulators increasingly expect explainability in credit decisions).

## 4. Ideas Considered
| Idea | Description | Verdict |
|---|---|---|
| Rule-based approval engine | Hard-coded thresholds (income, credit score) | ❌ Too rigid, doesn't generalise |
| Single ML classifier (Logistic Regression only) | Fast but limited accuracy ceiling | ⚠️ Used as a baseline, not final |
| Ensemble of multiple ML models with automatic best-model selection | Compare Logistic Regression, Decision Tree, Random Forest, XGBoost and deploy the best performer | ✅ **Selected** |
| Black-box deep learning model | Higher complexity, harder to explain to regulators/applicants | ❌ Rejected — explainability is a core requirement |

## 5. Chosen Direction
Build **SmartCredit AI**: a full-stack web platform that trains and compares multiple
ML models, automatically selects the best one by ROC-AUC, and serves explainable,
real-time credit card approval predictions through a premium banking-grade UI.

## 6. Key Differentiators
- Never returns a bare Approved/Rejected — always ships probability, confidence,
  risk category, and top contributing factors.
- Full audit trail for every prediction and account action.
- Enterprise-style UI (glassmorphism, dark/light mode) instead of a typical
  student-project Bootstrap template.

## 7. Next Steps
Proceed to `2_Requirement_Analysis` to formalise functional and non-functional
requirements based on the ideas above.
