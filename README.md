# Credit-Card-Approval-Prediction-ML

This repository documents the full lifecycle of **SmartCredit AI** — an enterprise-style,
explainable Credit Card Approval Prediction platform — organised into the standard
8-phase academic/SkillWallet submission structure.

The actual working application (Flask + ML pipeline) is untouched and lives in
**`5_Project_Development_Phase/SMARTCREDIT-AI/`**. Everything else in this repository
is supporting documentation for each phase of the software development lifecycle.

---

## 📁 Repository Structure

Credit-Card-Approval-Prediction-ML/
│
├── 1_Brainstorming_and_Ideation/
│   ├── Brainstorming.md
│   ├── Problem_Statement.md
│   └── Proposed_Solution.md
│
├── 2_Requirement_Analysis/
│   ├── Functional_Requirements.md
│   ├── Non_Functional_Requirements.md
│   └── SRS.md
│
├── 3_Project_Design_Phase/
│   ├── System_Architecture.md
│   ├── Database_Design.md
│   ├── Use_Case.md
│   └── ER_Diagram.md
│
├── 4_Project_Planning_Phase/
│   ├── Project_Plan.md
│   ├── Milestones.md
│   └── Timeline.md
│
├── 5_Project_Development_Phase/
│   └── SMARTCREDIT-AI/          ← The complete, working Flask application
│       ├── app.py, config.py, requirements.txt, .gitignore, README.md
│       ├── ml/                   (dataset generation, training, explainable inference)
│       ├── routes/ services/ utils/   (Flask backend)
│       ├── templates/ static/    (frontend — custom design system, no Bootstrap)
│       ├── models/               (trained model artefacts)
│       ├── data/                 (training dataset)
│       ├── database/             (SQLite database, created at runtime)
│       └── logs/                 (application logs)
│
├── 6_Project_Testing/
│   ├── Test_Cases.md
│   ├── Test_Report.md
│   └── Bug_Report.md
│
├── 7_Project_Documentation/
│   ├── User_Manual.md
│   ├── Installation_Guide.md
│   └── API_Documentation.md
│
└── 8_Project_Demonstration/
├── Demo_Guide.md
└── Presentation_Notes.md
---

## 🚀 Running the Application

```bash
cd 5_Project_Development_Phase/SMARTCREDIT-AI
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
python ml/data_generator.py       # optional — regenerate dataset
python ml/train.py                # optional — retrain model
python seed_demo_data.py          # optional — seed demo account
python app.py
```

Then open **http://localhost:5000** in your browser.

For full setup details, see
[`7_Project_Documentation/Installation_Guide.md`](7_Project_Documentation/Installation_Guide.md),
or the application's own
[`README.md`](5_Project_Development_Phase/SMARTCREDIT-AI/README.md).

---

## 📖 How to Navigate This Repository

| If you want to... | Go to... |
|---|---|
| Understand the problem and the idea behind the project | `1_Brainstorming_and_Ideation/` |
| Review functional/non-functional requirements or the SRS | `2_Requirement_Analysis/` |
| See the system architecture, database design, use cases, ER diagram | `3_Project_Design_Phase/` |
| See the project plan, milestones, and timeline | `4_Project_Planning_Phase/` |
| Run or read the actual source code | `5_Project_Development_Phase/SMARTCREDIT-AI/` |
| Review test cases, test results, and bug tracking | `6_Project_Testing/` |
| Read the user manual, installation guide, or API docs | `7_Project_Documentation/` |
| Prepare for or review the project demonstration | `8_Project_Demonstration/` |

---

## ✅ Reorganisation Notes

- The Flask project was **moved as-is** into `5_Project_Development_Phase/SMARTCREDIT-AI/`
  with no files renamed, no code modified, no routes changed, and no model retrained.
- All other phase folders contain professional placeholder documentation ready to be
  filled in / refined further as the project matures.
- Empty directories (if any) are tracked via `.gitkeep` files so the folder structure
  is preserved on GitHub.