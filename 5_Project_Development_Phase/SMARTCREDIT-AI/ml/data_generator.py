"""
SmartCredit AI - Dataset Generator
-----------------------------------
Generates a realistic, statistically-grounded Credit Card Approval dataset.

Note: Public credit-approval datasets (e.g. UCI "Credit Approval", "Credit
Card Approval Prediction") are not reachable from this offline environment,
so this module synthesises an equivalent dataset using well-known underwriting
heuristics (income, credit score, debt-to-income ratio, employment stability,
prior defaults, etc.) combined with randomised noise so the resulting labels
are realistic and *not* trivially separable — multiple ML models genuinely
have to learn the decision boundary. Swap this file for a real CSV loader if
a licensed dataset becomes available; the rest of the pipeline is unchanged.
"""

import os
import numpy as np
import pandas as pd

RANDOM_SEED = 42


def _sigmoid(x):
    return 1 / (1 + np.exp(-x))


def generate_dataset(n_samples: int = 6000, seed: int = RANDOM_SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    age = rng.integers(21, 66, n_samples)
    gender = rng.choice(["Male", "Female"], n_samples, p=[0.54, 0.46])
    marital_status = rng.choice(
        ["Single", "Married", "Divorced", "Widowed"], n_samples, p=[0.38, 0.45, 0.12, 0.05]
    )
    education = rng.choice(
        ["High School", "Graduate", "Post Graduate", "Doctorate"],
        n_samples, p=[0.28, 0.42, 0.24, 0.06],
    )
    employment_status = rng.choice(
        ["Salaried", "Self-Employed", "Business Owner", "Unemployed", "Retired"],
        n_samples, p=[0.48, 0.22, 0.14, 0.08, 0.08],
    )
    housing_status = rng.choice(
        ["Owned", "Mortgaged", "Rented", "Living with Family"],
        n_samples, p=[0.30, 0.24, 0.32, 0.14],
    )
    dependents = rng.integers(0, 5, n_samples)
    years_employed = np.clip(rng.normal(6, 5, n_samples), 0, 40).round(1)
    years_at_residence = np.clip(rng.normal(4, 3, n_samples), 0, 30).round(1)
    num_credit_cards = rng.integers(0, 8, n_samples)
    previous_defaults = rng.choice([0, 1, 2, 3], n_samples, p=[0.78, 0.14, 0.06, 0.02])

    # Income correlated with education/employment
    edu_bonus = pd.Series(education).map(
        {"High School": 0, "Graduate": 12000, "Post Graduate": 26000, "Doctorate": 38000}
    ).values
    emp_bonus = pd.Series(employment_status).map(
        {"Salaried": 8000, "Self-Employed": 4000, "Business Owner": 15000, "Unemployed": -20000, "Retired": -5000}
    ).values
    annual_income = np.clip(
        rng.normal(45000, 18000, n_samples) + edu_bonus + emp_bonus + years_employed * 900, 8000, 400000
    ).round(0)

    credit_score = np.clip(
        rng.normal(650, 90, n_samples)
        - previous_defaults * 55
        + (years_employed > 3) * 20
        + (annual_income > 60000) * 25,
        300, 900,
    ).round(0)

    loan_amount = np.clip(rng.normal(15000, 9000, n_samples), 1000, 100000).round(0)
    existing_debt = np.clip(rng.normal(9000, 8000, n_samples) + previous_defaults * 4000, 0, 150000).round(0)

    debt_to_income = (existing_debt + loan_amount) / (annual_income + 1)

    df = pd.DataFrame({
        "Age": age,
        "Gender": gender,
        "Marital_Status": marital_status,
        "Education": education,
        "Employment_Status": employment_status,
        "Years_Employed": years_employed,
        "Annual_Income": annual_income,
        "Credit_Score": credit_score,
        "Loan_Amount": loan_amount,
        "Existing_Debt": existing_debt,
        "Housing_Status": housing_status,
        "Years_At_Residence": years_at_residence,
        "Dependents": dependents,
        "Num_Credit_Cards": num_credit_cards,
        "Previous_Defaults": previous_defaults,
    })
    df["Debt_To_Income_Ratio"] = debt_to_income.round(3)

    # ---- Underwriting score (latent) -> probability of approval ----
    z = (
        0.014 * (credit_score - 650)
        + 0.000018 * (annual_income - 45000)
        - 1.35 * debt_to_income
        - 0.55 * previous_defaults
        + 0.05 * years_employed
        - 0.09 * dependents
        + 0.10 * (housing_status != "Rented").astype(int)
        + 0.15 * np.isin(employment_status, ["Salaried", "Business Owner"]).astype(int)
        - 0.35 * (employment_status == "Unemployed").astype(int)
        + rng.normal(0, 0.65, n_samples)  # noise so it's not perfectly separable
    )
    prob_approval = _sigmoid(z)
    approved = (prob_approval > 0.5).astype(int)

    df["Approval_Status"] = np.where(approved == 1, "Approved", "Rejected")

    # introduce a small amount of missingness to exercise the cleaning pipeline
    for col in ["Years_Employed", "Years_At_Residence", "Existing_Debt"]:
        mask = rng.random(n_samples) < 0.02
        df.loc[mask, col] = np.nan

    return df


def save_dataset(path: str, n_samples: int = 6000):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df = generate_dataset(n_samples=n_samples)
    df.to_csv(path, index=False)
    return df


if __name__ == "__main__":
    out_path = os.path.join(os.path.dirname(__file__), "..", "data", "credit_card_approval.csv")
    data = save_dataset(out_path)
    print(f"Saved {len(data)} rows to {out_path}")
    print(data["Approval_Status"].value_counts(normalize=True))
