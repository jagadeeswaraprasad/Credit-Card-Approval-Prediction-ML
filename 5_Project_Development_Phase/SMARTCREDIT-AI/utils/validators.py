"""SmartCredit AI - Validation Helpers"""

import re

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate_email(email: str) -> bool:
    return bool(email) and bool(EMAIL_RE.match(email.strip()))


def validate_password(password: str) -> tuple[bool, str]:
    if not password or len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one number."
    return True, ""


def validate_registration(form: dict) -> list[str]:
    errors = []
    if not form.get("full_name", "").strip():
        errors.append("Full name is required.")
    if not validate_email(form.get("email", "")):
        errors.append("A valid email address is required.")
    ok, msg = validate_password(form.get("password", ""))
    if not ok:
        errors.append(msg)
    if form.get("password") != form.get("confirm_password"):
        errors.append("Passwords do not match.")
    return errors


def validate_prediction_form(form: dict) -> list[str]:
    errors = []
    required_numeric = {
        "Age": (18, 100),
        "Annual_Income": (0, 10_000_000),
        "Credit_Score": (300, 900),
        "Loan_Amount": (0, 10_000_000),
        "Existing_Debt": (0, 10_000_000),
        "Years_Employed": (0, 60),
        "Years_At_Residence": (0, 60),
        "Dependents": (0, 20),
        "Num_Credit_Cards": (0, 30),
        "Previous_Defaults": (0, 20),
    }
    for field, (lo, hi) in required_numeric.items():
        raw = form.get(field, "")
        try:
            val = float(raw)
        except (TypeError, ValueError):
            errors.append(f"{field.replace('_', ' ')} must be a number.")
            continue
        if not (lo <= val <= hi):
            errors.append(f"{field.replace('_', ' ')} must be between {lo} and {hi}.")

    required_text = ["Gender", "Marital_Status", "Education", "Employment_Status", "Housing_Status"]
    for field in required_text:
        if not form.get(field, "").strip():
            errors.append(f"{field.replace('_', ' ')} is required.")

    if not form.get("Applicant_Name", "").strip():
        errors.append("Applicant name is required.")

    return errors
