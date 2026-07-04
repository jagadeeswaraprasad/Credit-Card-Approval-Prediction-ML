# Software Requirements Specification (SRS)

**Project:** SmartCredit AI — Credit Card Approval Prediction
**Phase:** 2. Requirement Analysis
**Version:** 1.0

---

## 1. Introduction

### 1.1 Purpose
This document specifies the software requirements for SmartCredit AI, a web-based
platform that predicts credit card approval outcomes using machine learning and
presents explainable, auditable decisions to end users.

### 1.2 Scope
SmartCredit AI covers: user authentication, applicant data intake, ML-based prediction,
explainability reporting, prediction history management, and model performance
reporting. It does not cover core banking integration, physical card issuance, or
KYC document verification.

### 1.3 Intended Audience
Project reviewers, evaluators, and developers extending the SmartCredit AI codebase.

### 1.4 References
- `1_Brainstorming_and_Ideation/Problem_Statement.md`
- `2_Requirement_Analysis/Functional_Requirements.md`
- `2_Requirement_Analysis/Non_Functional_Requirements.md`
- `5_Project_Development_Phase/SMARTCREDIT-AI/README.md`

---

## 2. Overall Description

### 2.1 Product Perspective
SmartCredit AI is a standalone Flask web application backed by a SQLite database and
a locally-trained scikit-learn/XGBoost model pipeline. It is not dependent on any
external banking system.

### 2.2 Product Functions
See `Functional_Requirements.md` for the complete functional requirement list
(authentication, prediction engine, dashboard, history, model performance, audit log).

### 2.3 User Classes
- **Analyst / End User** — registers, logs in, submits applications, reviews results
  and history.

### 2.4 Operating Environment
- Python 3.10+
- Flask 3.x
- SQLite (bundled, no separate server required)
- Modern web browser (Chrome, Firefox, Edge, Safari)

### 2.5 Design & Implementation Constraints
- Must use SQLite only (no MySQL/MongoDB) per project constraints.
- Must not use Bootstrap or third-party UI frameworks — custom CSS design system only.
- ML pipeline must compare multiple models and automatically select the best one.

---

## 3. Specific Requirements
See:
- `Functional_Requirements.md` for functional requirements (FR-01 to FR-29).
- `Non_Functional_Requirements.md` for non-functional requirements (NFR-01 to NFR-18).

---

## 4. External Interface Requirements

### 4.1 User Interfaces
Landing page, authentication pages, dashboard, new prediction form, result page,
prediction history, and model performance page (see
`3_Project_Design_Phase/System_Architecture.md`).

### 4.2 Software Interfaces
- scikit-learn / XGBoost for model training and inference.
- joblib for model artefact persistence.
- SQLite3 (Python standard library) for data persistence.

---

## 5. Appendix
Dataset details and generation methodology are documented in the project README
at `5_Project_Development_Phase/SMARTCREDIT-AI/README.md`.
