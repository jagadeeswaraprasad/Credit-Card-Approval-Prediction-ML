# Non-Functional Requirements

**Project:** SmartCredit AI — Credit Card Approval Prediction
**Phase:** 2. Requirement Analysis

---

## 1. Performance
| ID | Requirement |
|---|---|
| NFR-01 | A prediction request shall return a result in under 1 second under normal load. |
| NFR-02 | The dashboard shall load within 2 seconds for a user with typical prediction history volume. |

## 2. Security
| ID | Requirement |
|---|---|
| NFR-03 | Passwords shall be stored using a secure one-way hash (never in plaintext). |
| NFR-04 | Sessions shall be protected with HTTP-only, same-site cookies. |
| NFR-05 | All authenticated routes shall be inaccessible without a valid session. |
| NFR-06 | All user-modifying actions shall be recorded in an audit log with timestamp. |

## 3. Usability
| ID | Requirement |
|---|---|
| NFR-07 | The UI shall be responsive across desktop, tablet, and mobile viewports. |
| NFR-08 | The UI shall support both dark mode and light mode. |
| NFR-09 | Form validation errors shall be clearly displayed inline and via toast notifications. |
| NFR-10 | Every prediction result shall be explainable in plain language, not just numeric output. |

## 4. Reliability & Availability
| ID | Requirement |
|---|---|
| NFR-11 | The application shall handle invalid or missing input gracefully without crashing. |
| NFR-12 | The application shall log unexpected errors for later diagnosis (500 error handling). |

## 5. Maintainability
| ID | Requirement |
|---|---|
| NFR-13 | The codebase shall follow a modular structure separating routes, services, ML logic, and utilities. |
| NFR-14 | The codebase shall follow PEP8 style conventions. |
| NFR-15 | The ML pipeline shall be re-runnable independently of the web application (`ml/train.py`). |

## 6. Portability
| ID | Requirement |
|---|---|
| NFR-16 | The application shall run on any platform supporting Python 3.10+ and Flask. |
| NFR-17 | The application shall use SQLite to avoid external database server dependencies. |

## 7. Scalability (Design Intent)
| ID | Requirement |
|---|---|
| NFR-18 | The architecture shall allow the SQLite layer to be swapped for a production RDBMS with minimal code change (service layer abstraction). |
