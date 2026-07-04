# User Manual

**Project:** SmartCredit AI — Credit Card Approval Prediction
**Phase:** 7. Project Documentation

---

## 1. Getting Started
1. Open the application in your browser (default: `http://localhost:5000`).
2. From the landing page, click **Get Started** to create an account, or **Log In**
   if you already have one.

## 2. Creating an Account
1. Click **Get Started** on the landing page (or **Register** from the login page).
2. Enter your full name, email address, and a password (minimum 8 characters,
   including at least one uppercase letter and one number).
3. Confirm your password and submit.
4. You will be redirected to the login page.

## 3. Logging In
1. Enter your registered email and password.
2. Optionally check **Remember Me** to stay logged in longer.
3. Click **Log In** to access your dashboard.

## 4. Dashboard
The dashboard shows:
- Total predictions made
- Approval and rejection rates
- Average confidence score
- A 14-day prediction trend chart
- Risk category distribution
- Your most recent predictions

## 5. Running a New Prediction
1. Click **New Prediction** in the sidebar.
2. Fill in the applicant's personal details (name, age, gender, marital status,
   education, dependents).
3. Fill in the financial profile (employment status, years employed, annual income,
   credit score, requested loan amount, existing debt).
4. Fill in residential and credit history (housing status, years at residence,
   number of credit cards, previous defaults).
5. Click **Run AI Prediction**.
6. Wait a few seconds while the model analyses the application.

## 6. Understanding Your Result
The result page shows:
- **Decision** — Approved or Rejected.
- **Risk Category** — Low, Medium, or High Risk.
- **Confidence Meter** — how certain the model is.
- **Approval / Rejection Probability** — as percentages.
- **Top Contributing Factors** — the specific factors that most influenced the
  decision, marked as positive or negative.
- **Recommendation & Next Steps** — tailored guidance based on the outcome.

You can print or save the result as a PDF using the **Download / Print Report** button.

## 7. Prediction History
1. Click **Prediction History** in the sidebar.
2. Use the search box to find an applicant by name.
3. Use the filters to narrow by result (Approved/Rejected) or risk category.
4. Use the sort dropdown to order by date, name, or confidence.
5. Click **Export CSV** to download your full history.
6. Click **Delete** on any row to permanently remove that record.

## 8. Model Performance
Click **Model Performance** in the sidebar to view:
- A comparison table of all trained models (Accuracy, Precision, Recall, F1, ROC-AUC).
- The confusion matrix and ROC curve for the deployed model.
- A feature importance chart showing which applicant attributes matter most overall.

## 9. Switching Theme
Click the sun/moon icon in the top bar to toggle between light and dark mode.

## 10. Logging Out
Click **Logout** in the sidebar to end your session securely.
