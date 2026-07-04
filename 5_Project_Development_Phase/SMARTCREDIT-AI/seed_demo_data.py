"""
SmartCredit AI - Demo Data Seeder
------------------------------------
Creates a demo user and a batch of realistic historical predictions so the
Dashboard / History / Model Performance pages have data to show immediately
after setup. Optional — run with:  python seed_demo_data.py
"""

import random
import numpy as np

from app import create_app
from utils.db import get_connection
from services.auth_service import create_user
from services.prediction_service import make_prediction

DEMO_EMAIL = "demo@smartcredit.ai"
DEMO_PASSWORD = "Demo1234"

FIRST_NAMES = ["Aarav", "Priya", "Rohan", "Sneha", "Vikram", "Ananya", "Karan", "Ishita", "Arjun", "Meera"]
LAST_NAMES = ["Sharma", "Verma", "Patel", "Nair", "Iyer", "Gupta", "Khan", "Reddy", "Das", "Chopra"]


def random_applicant(rng):
    name = f"{rng.choice(FIRST_NAMES)} {rng.choice(LAST_NAMES)}"
    return {
        "Applicant_Name": name,
        "Age": str(rng.integers(21, 65)),
        "Gender": rng.choice(["Male", "Female"]),
        "Marital_Status": rng.choice(["Single", "Married", "Divorced", "Widowed"]),
        "Education": rng.choice(["High School", "Graduate", "Post Graduate", "Doctorate"]),
        "Dependents": str(rng.integers(0, 4)),
        "Employment_Status": rng.choice(["Salaried", "Self-Employed", "Business Owner", "Unemployed", "Retired"]),
        "Years_Employed": str(round(float(rng.uniform(0, 20)), 1)),
        "Annual_Income": str(int(rng.uniform(15000, 150000))),
        "Credit_Score": str(int(rng.uniform(350, 850))),
        "Loan_Amount": str(int(rng.uniform(2000, 40000))),
        "Existing_Debt": str(int(rng.uniform(0, 40000))),
        "Housing_Status": rng.choice(["Owned", "Mortgaged", "Rented", "Living with Family"]),
        "Years_At_Residence": str(round(float(rng.uniform(0, 15)), 1)),
        "Num_Credit_Cards": str(rng.integers(0, 6)),
        "Previous_Defaults": str(rng.choice([0, 0, 0, 1, 2])),
    }


def seed(n=25):
    app = create_app()
    with app.app_context():
        pass  # app context not strictly required, kept for clarity/extension

    conn = get_connection()
    existing = conn.execute("SELECT id FROM users WHERE email = ?", (DEMO_EMAIL,)).fetchone()
    conn.close()

    if existing:
        user_id = existing["id"]
        print(f"Demo user already exists (id={user_id}).")
    else:
        user_id, error = create_user("Demo Analyst", DEMO_EMAIL, DEMO_PASSWORD)
        if error:
            print(f"Could not create demo user: {error}")
            return
        print(f"Created demo user: {DEMO_EMAIL} / {DEMO_PASSWORD}")

    rng = np.random.default_rng(7)
    for _ in range(n):
        applicant = random_applicant(rng)
        try:
            make_prediction(user_id, applicant)
        except FileNotFoundError:
            print("Model not trained yet. Run `python ml/train.py` first.")
            return
    print(f"Seeded {n} demo predictions for user_id={user_id}.")


if __name__ == "__main__":
    seed()
