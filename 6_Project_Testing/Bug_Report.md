# Bug Report

**Project:** SmartCredit AI — Credit Card Approval Prediction
**Phase:** 6. Project Testing

---

## Bug Tracking Table

| Bug ID | Module | Description | Severity | Status | Resolution |
|---|---|---|---|---|---|
| BUG-01 | ML Inference | Prediction endpoint raised a dtype error when encoding categorical fields on newer pandas versions | High | ✅ Fixed | Rewrote row encoding to build feature values explicitly instead of in-place DataFrame cell assignment |
| BUG-02 | ML Inference | scikit-learn emitted a "feature names" warning when scaling a raw NumPy array | Low | ✅ Fixed | Passed a named DataFrame (matching training feature order) into `scaler.transform()` |
| BUG-03 | — | _(template row — no further defects logged as of this build)_ | — | — | — |

## Severity Legend
- **Critical** — Application crash or data loss.
- **High** — Core feature broken or incorrect result produced.
- **Medium** — Feature partially broken, workaround exists.
- **Low** — Cosmetic issue, warning, or minor inconsistency.

## Status Legend
- ✅ Fixed
- 🔄 In Progress
- ⬜ Open
- ❌ Won't Fix (with justification)

> Log new defects here as they are discovered during further testing or review,
> following the same format.
