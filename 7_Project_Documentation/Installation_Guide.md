# Installation Guide

**Project:** SmartCredit AI — Credit Card Approval Prediction
**Phase:** 7. Project Documentation

---

## 1. Prerequisites
- Python 3.10 or higher
- pip
- (Optional) a virtual environment tool such as `venv`

## 2. Location of the Application
The complete Flask application lives at:
```
5_Project_Development_Phase/SMARTCREDIT-AI/
```
All commands below should be run from inside that folder.

```bash
cd 5_Project_Development_Phase/SMARTCREDIT-AI
```

## 3. Create a Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

## 4. Install Dependencies
```bash
pip install -r requirements.txt
```
> If `xgboost` fails to install on your system, the training pipeline automatically
> falls back to a `GradientBoostingClassifier` so the project still runs end-to-end.

## 5. Generate the Dataset & Train the Model
> The repository already ships with a trained model in `models/`. Re-run this step
> only if you want to regenerate the dataset or retrain from scratch.
```bash
python ml/data_generator.py
python ml/train.py
```

## 6. (Optional) Seed Demo Data
```bash
python seed_demo_data.py
```
Creates a demo account: `demo@smartcredit.ai` / `Demo1234`, with 25 sample predictions.

## 7. Run the Application
```bash
python app.py
```
Then open your browser to:
```
http://localhost:5000
```

## 8. Resetting the Application
To reset all users/predictions/audit logs, delete the SQLite database file:
```
database/smartcredit.db
```
It will be recreated automatically the next time the app starts.

## 9. Troubleshooting
| Issue | Resolution |
|---|---|
| `ModuleNotFoundError` for a package | Re-run `pip install -r requirements.txt` inside the correct virtual environment |
| Model not found error on prediction | Run `python ml/train.py` to (re)generate `models/*.pkl` |
| Port 5000 already in use | Run `app.run(port=5001)` in `app.py`, or stop the conflicting process |
