# Test Cases

**Project:** SmartCredit AI — Credit Card Approval Prediction
**Phase:** 6. Project Testing

---

| Test ID | Module | Test Description | Steps | Expected Result | Status |
|---|---|---|---|---|---|
| TC-01 | Auth | Register with valid details | Submit registration form with valid name/email/password | Account created, redirected to login | ✅ Pass |
| TC-02 | Auth | Register with duplicate email | Submit registration with an already-registered email | Error message shown, no duplicate account created | ✅ Pass |
| TC-03 | Auth | Register with weak password | Submit password under 8 chars / missing number or uppercase | Validation error shown, form not submitted | ✅ Pass |
| TC-04 | Auth | Login with valid credentials | Submit correct email/password | Redirected to dashboard, session created | ✅ Pass |
| TC-05 | Auth | Login with incorrect password | Submit valid email, wrong password | Error message shown, no session created | ✅ Pass |
| TC-06 | Auth | Access dashboard while logged out | Navigate to `/dashboard` without logging in | Redirected to login page | ✅ Pass |
| TC-07 | Prediction | Submit valid application (strong profile) | Fill form with high income/credit score, submit | Result = Approved, Low Risk, factors shown | ✅ Pass |
| TC-08 | Prediction | Submit valid application (weak profile) | Fill form with low income/credit score, high debt, submit | Result = Rejected, High Risk, factors shown | ✅ Pass |
| TC-09 | Prediction | Submit form with missing required field | Leave a required field blank, submit | Inline validation error shown, no API call made | ✅ Pass |
| TC-10 | Prediction | Verify explainability output | Submit any valid application | Response includes probability, confidence, risk category, top factors, recommendation | ✅ Pass |
| TC-11 | Dashboard | View analytics with no predictions | Log in as new user, open dashboard | Empty states shown, no errors | ✅ Pass |
| TC-12 | Dashboard | View analytics with predictions | Log in as user with history, open dashboard | Correct totals, approval rate, charts rendered | ✅ Pass |
| TC-13 | History | Search by applicant name | Enter partial name in search box | Only matching records displayed | ✅ Pass |
| TC-14 | History | Filter by result/risk | Select "Rejected" and "High Risk" filters | Only matching records displayed | ✅ Pass |
| TC-15 | History | Sort by confidence | Select "Sort: Confidence" | Records reordered accordingly | ✅ Pass |
| TC-16 | History | Export CSV | Click "Export CSV" | CSV file downloaded with correct columns and rows | ✅ Pass |
| TC-17 | History | Delete a record | Click delete on a record, confirm | Record removed from list and database | ✅ Pass |
| TC-18 | Model Performance | View model comparison | Open Model Performance page | All trained models listed with metrics; best model marked deployed | ✅ Pass |
| TC-19 | Security | Session isolation | Log in as User A, attempt to view/delete User B's prediction by ID | Access denied / record not found | ✅ Pass |
| TC-20 | Error Handling | Navigate to invalid URL | Visit a non-existent route | Custom 404 page displayed | ✅ Pass |

> Extend this table with additional edge cases (boundary values for age/credit score,
> network failure handling, concurrent submissions, etc.) as testing progresses.
