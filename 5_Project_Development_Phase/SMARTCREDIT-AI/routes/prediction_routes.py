"""SmartCredit AI - Prediction Routes"""

from flask import Blueprint, render_template, request, session, jsonify, redirect, url_for, flash
from utils.decorators import login_required
from utils.validators import validate_prediction_form
from services.prediction_service import make_prediction, get_prediction
from services.auth_service import log_action

prediction_bp = Blueprint("prediction", __name__)


@prediction_bp.route("/predict/new")
@login_required
def new_prediction():
    return render_template("new_prediction.html")


@prediction_bp.route("/api/predict", methods=["POST"])
@login_required
def api_predict():
    form = request.get_json(silent=True) or request.form.to_dict()
    errors = validate_prediction_form(form)
    if errors:
        return jsonify({"success": False, "errors": errors}), 400

    try:
        result = make_prediction(session["user_id"], form)
        log_action(session["user_id"], "PREDICTION_MADE",
                   f"{result['prediction']} for {result['applicant_name']} "
                   f"(confidence {result['confidence_score']}%)")
        return jsonify({"success": True, "result": result})
    except FileNotFoundError:
        return jsonify({"success": False, "errors": ["Model not trained yet. Run ml/train.py."]}), 500
    except Exception as exc:  # noqa: BLE001
        return jsonify({"success": False, "errors": [str(exc)]}), 500


@prediction_bp.route("/predict/result/<int:prediction_id>")
@login_required
def result(prediction_id):
    record = get_prediction(prediction_id, session["user_id"])
    if not record:
        flash("Prediction not found.", "danger")
        return redirect(url_for("dashboard.dashboard"))
    return render_template("result.html", record=record)
