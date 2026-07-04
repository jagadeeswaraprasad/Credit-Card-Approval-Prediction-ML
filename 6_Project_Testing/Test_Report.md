# Test Report

**Project:** SmartCredit AI — Credit Card Approval Prediction
**Phase:** 6. Project Testing

---

## 1. Summary
| Metric | Value |
|---|---|
| Total Test Cases | 20 (see `Test_Cases.md`) |
| Passed | 20 |
| Failed | 0 |
| Blocked | 0 |
| Test Coverage Areas | Authentication, Prediction Engine, Dashboard, History, Model Performance, Security, Error Handling |

## 2. Test Environment
| Item | Detail |
|---|---|
| OS | Linux (containerised) |
| Python Version | 3.12 |
| Framework | Flask 3.x |
| Database | SQLite (local file) |
| ML Libraries | scikit-learn, XGBoost (with GradientBoosting fallback) |
| Test Method | Flask test client (functional/integration testing) |

## 3. Functional Verification Highlights
- End-to-end flow verified: registration → login → new prediction → result →
  history → export → delete → logout.
- Both **Approved** and **Rejected** prediction paths verified with distinct
  applicant profiles, confirming the model responds sensibly to input changes
  (credit score, income, debt-to-income ratio, prior defaults).
- Confirmed prediction responses always include probability, confidence, risk
  category, and top contributing factors — never a bare label.
- Confirmed session-based access control blocks unauthenticated access to
  protected routes.

## 4. Known Limitations
- XGBoost may not be installed in every environment; a GradientBoostingClassifier
  fallback is used automatically and is functionally equivalent for this project's
  purposes, though its exact accuracy profile may differ slightly from true XGBoost.
- The dataset is synthetically generated (see project README) rather than sourced
  from a live public dataset, due to offline build constraints. This does not affect
  the validity of the pipeline or the platform's functional testing.

## 5. Conclusion
All planned test cases passed in the current build. The application is functionally
stable for demonstration purposes. See `Bug_Report.md` for any issues logged during
testing and their resolution status.
