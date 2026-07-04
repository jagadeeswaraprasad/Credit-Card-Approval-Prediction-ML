# Functional Requirements

**Project:** SmartCredit AI — Credit Card Approval Prediction
**Phase:** 2. Requirement Analysis

---

## 1. Authentication & User Management
| ID | Requirement |
|---|---|
| FR-01 | The system shall allow a new user to register with full name, email, and password. |
| FR-02 | The system shall validate email format and password strength during registration. |
| FR-03 | The system shall allow a registered user to log in with email and password. |
| FR-04 | The system shall support a "Remember Me" option that extends session duration. |
| FR-05 | The system shall provide a "Forgot Password" flow. |
| FR-06 | The system shall allow a logged-in user to log out, clearing their session. |

## 2. Prediction Engine
| ID | Requirement |
|---|---|
| FR-07 | The system shall accept applicant details through a structured form (personal, financial, residential/credit history). |
| FR-08 | The system shall validate all required fields before submission. |
| FR-09 | The system shall return a prediction of "Approved" or "Rejected" for a submitted application. |
| FR-10 | The system shall return an approval probability and rejection probability for every prediction. |
| FR-11 | The system shall return a confidence score for every prediction. |
| FR-12 | The system shall classify every prediction into Low / Medium / High risk. |
| FR-13 | The system shall return the top contributing factors behind each prediction. |
| FR-14 | The system shall provide a recommendation and next-step guidance based on the outcome. |

## 3. Dashboard & Analytics
| ID | Requirement |
|---|---|
| FR-15 | The system shall display total predictions, approval rate, rejection rate, and average confidence for the logged-in user. |
| FR-16 | The system shall display a prediction trend chart over the last 14 days. |
| FR-17 | The system shall display a risk category distribution chart. |
| FR-18 | The system shall display the most recent predictions on the dashboard. |

## 4. Prediction History
| ID | Requirement |
|---|---|
| FR-19 | The system shall list all past predictions for the logged-in user, paginated. |
| FR-20 | The system shall allow searching predictions by applicant name. |
| FR-21 | The system shall allow filtering predictions by result and risk category. |
| FR-22 | The system shall allow sorting predictions by date, name, or confidence. |
| FR-23 | The system shall allow exporting prediction history as a CSV file. |
| FR-24 | The system shall allow deleting an individual prediction record. |

## 5. Model Performance
| ID | Requirement |
|---|---|
| FR-25 | The system shall display accuracy, precision, recall, F1 score, and ROC-AUC for all trained models. |
| FR-26 | The system shall display a confusion matrix for the deployed model. |
| FR-27 | The system shall display an ROC curve for the deployed model. |
| FR-28 | The system shall display global feature importance for the deployed model. |

## 6. Auditability
| ID | Requirement |
|---|---|
| FR-29 | The system shall log every registration, login, prediction, deletion, and export action to an audit log. |
