# Use Case Document

**Project:** SmartCredit AI — Credit Card Approval Prediction
**Phase:** 3. Project Design Phase

---

## 1. Actors
- **Analyst / End User** — the primary actor who registers, logs in, and uses the platform.
- **System (ML Engine)** — supporting actor that scores applications.

## 2. Use Case Summary Table
| ID | Use Case | Primary Actor |
|---|---|---|
| UC-01 | Register Account | Analyst |
| UC-02 | Log In | Analyst |
| UC-03 | Log Out | Analyst |
| UC-04 | Submit New Credit Assessment | Analyst |
| UC-05 | View Prediction Result | Analyst |
| UC-06 | View Dashboard Analytics | Analyst |
| UC-07 | Search / Filter / Sort Prediction History | Analyst |
| UC-08 | Export Prediction History as CSV | Analyst |
| UC-09 | Delete a Prediction Record | Analyst |
| UC-10 | View Model Performance | Analyst |

## 3. Detailed Use Cases

### UC-04: Submit New Credit Assessment
- **Actor:** Analyst
- **Precondition:** Analyst is logged in.
- **Main Flow:**
  1. Analyst navigates to "New Prediction".
  2. Analyst fills in applicant personal, financial, and residential/credit details.
  3. Analyst submits the form.
  4. System validates input.
  5. System encodes/scales features and runs the deployed model.
  6. System computes explainability factors and risk category.
  7. System stores the prediction and redirects to the result page.
- **Alternate Flow:** If validation fails, the system highlights invalid fields and
  shows an error toast without submitting.
- **Postcondition:** A new record exists in the `predictions` table; an audit log
  entry is created.

### UC-07: Search / Filter / Sort Prediction History
- **Actor:** Analyst
- **Precondition:** Analyst is logged in and has at least one prediction on record.
- **Main Flow:**
  1. Analyst opens "Prediction History".
  2. Analyst enters a search term and/or selects a result/risk filter and sort order.
  3. System queries matching records and displays a paginated table.
- **Postcondition:** Filtered results are displayed; no data is modified.

### UC-09: Delete a Prediction Record
- **Actor:** Analyst
- **Precondition:** Analyst is logged in and viewing prediction history.
- **Main Flow:**
  1. Analyst clicks "Delete" on a record and confirms.
  2. System removes the record (scoped to the logged-in user).
  3. System logs the deletion to the audit trail.
- **Postcondition:** The record no longer appears in history.

## 4. Use Case Diagram (Textual Representation)
```
                +----------------------------+
                |         Analyst            |
                +----------------------------+
                 |   |   |   |   |   |   |
   Register  Log In  Log Out  Submit   View    Manage   View Model
                              Assessment Dashboard History  Performance
```
