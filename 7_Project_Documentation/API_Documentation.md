# API Documentation

**Project:** SmartCredit AI — Credit Card Approval Prediction
**Phase:** 7. Project Documentation

---

## Authentication
All endpoints below (except `/`, `/login`, `/register`) require an active session
(the user must be logged in). Unauthenticated requests to protected routes redirect
to `/login`, or return `401 Unauthorized` for `/api/*` JSON endpoints.

---

## `POST /api/predict`
Runs an explainable credit approval prediction for a submitted applicant.

**Auth required:** Yes

**Request Body (JSON or form):**
```json
{
  "Applicant_Name": "Riya Sharma",
  "Age": "32",
  "Gender": "Female",
  "Marital_Status": "Married",
  "Education": "Graduate",
  "Dependents": "1",
  "Employment_Status": "Salaried",
  "Years_Employed": "5.5",
  "Annual_Income": "65000",
  "Credit_Score": "720",
  "Loan_Amount": "15000",
  "Existing_Debt": "4000",
  "Housing_Status": "Owned",
  "Years_At_Residence": "3",
  "Num_Credit_Cards": "2",
  "Previous_Defaults": "0"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "result": {
    "prediction": "Approved",
    "approval_probability": 96.57,
    "rejection_probability": 3.43,
    "confidence_score": 96.57,
    "risk_category": "Low Risk",
    "top_factors": [
      { "feature": "Credit Score", "impact": "Positive", "weight": 2.03, "value": 720.0 }
    ],
    "recommendation": {
      "headline": "This application meets SmartCredit AI's underwriting criteria.",
      "next_steps": ["Digital KYC verification", "..."],
      "tips": ["Maintain your current credit utilisation below 30%..."]
    },
    "model_used": "Logistic Regression",
    "prediction_id": 1
  }
}
```

**Error Response (400/500):**
```json
{ "success": false, "errors": ["Age must be between 18 and 100."] }
```

---

## `GET /predict/result/<prediction_id>`
Renders the result page for a specific prediction owned by the logged-in user.
Returns `404`-style redirect with a flash message if the record does not belong
to the current user.

---

## `GET /history`
Renders the paginated prediction history page.

**Query Parameters:**
| Param | Description |
|---|---|
| `page` | Page number (default 1) |
| `search` | Filter by applicant name (partial match) |
| `status` | `Approved` or `Rejected` |
| `risk` | `Low Risk`, `Medium Risk`, or `High Risk` |
| `sort_by` | `date`, `name`, or `confidence` |
| `sort_dir` | `asc` or `desc` |

---

## `DELETE /api/history/<prediction_id>`
Deletes a prediction record owned by the logged-in user.

**Success Response:**
```json
{ "success": true }
```

---

## `GET /history/export`
Streams the logged-in user's full prediction history as a downloadable CSV file
(`Content-Disposition: attachment`).

---

## `GET /model-performance`
Renders the model comparison, confusion matrix, ROC curve, and feature importance
page for the currently deployed model.

---

## `GET /dashboard`
Renders the analytics dashboard (totals, approval/rejection rate, average
confidence, 14-day trend, risk distribution, recent predictions).

---

## Auth Endpoints
| Route | Method | Description |
|---|---|---|
| `/register` | GET, POST | Create a new account |
| `/login` | GET, POST | Log in |
| `/logout` | GET | Clear session and log out |
| `/forgot-password` | GET, POST | Request a password reset (placeholder flow) |
