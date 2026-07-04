# Problem Statement

**Project:** SmartCredit AI — Credit Card Approval Prediction
**Phase:** 1. Brainstorming & Ideation

---

## 1. Background
Credit card issuers receive a high volume of applications daily. Traditional approval
workflows rely on manual underwriting or simple rule-based checks, which are:

- **Slow** — applicants wait days for a decision.
- **Inconsistent** — different underwriters may reach different conclusions on similar profiles.
- **Opaque** — applicants and internal auditors are rarely told *why* a decision was made.
- **Difficult to scale** — manual review does not scale with application volume.

## 2. Problem Statement
> Financial institutions need an accurate, fast, and explainable system that can predict
> whether a credit card application should be approved or rejected, while clearly
> communicating the risk factors behind every decision — without functioning as an
> opaque black box.

## 3. Who Is Affected
- **Underwriting teams** — need a consistent, auditable decisioning tool.
- **Applicants** — deserve clarity on why their application was approved or declined.
- **Compliance / risk teams** — need an audit trail and explainability for regulatory review.
- **Engineering teams** — need a maintainable, modular codebase to extend over time.

## 4. Impact of Not Solving This Problem
- Continued inconsistent approval decisions and applicant dissatisfaction.
- Higher operational cost from manual review.
- Regulatory exposure from undocumented, unexplainable decisioning.

## 5. Scope of the Problem (for this project)
This project addresses the **decisioning and explainability layer** of the credit card
approval workflow — collecting applicant data, generating a risk-based prediction, and
presenting it through a secure, auditable web platform. It does not cover downstream
processes such as card manufacturing, physical KYC verification, or core banking
integration (these are noted as future extensions).

## 6. Success Criteria
- A trained model achieving strong discriminative performance (ROC-AUC > 0.90 on
  held-out data).
- Every prediction accompanied by probability, confidence, risk category, and
  top contributing factors.
- A secure, role-appropriate web application usable by an underwriting analyst
  end-to-end (login → new assessment → result → history).
