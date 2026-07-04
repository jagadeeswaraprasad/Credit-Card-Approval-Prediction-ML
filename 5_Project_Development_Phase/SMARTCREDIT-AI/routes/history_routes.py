"""SmartCredit AI - Prediction History Routes"""

from flask import Blueprint, render_template, request, session, jsonify, Response
from utils.decorators import login_required
from services.history_service import get_history, delete_prediction, export_csv
from services.auth_service import log_action

history_bp = Blueprint("history", __name__)


@history_bp.route("/history")
@login_required
def history():
    page = request.args.get("page", 1, type=int)
    search = request.args.get("search", "")
    status_filter = request.args.get("status", "")
    risk_filter = request.args.get("risk", "")
    sort_by = request.args.get("sort_by", "date")
    sort_dir = request.args.get("sort_dir", "desc")

    data = get_history(session["user_id"], page, search, status_filter, risk_filter, sort_by, sort_dir)
    return render_template(
        "history.html", data=data, search=search, status_filter=status_filter,
        risk_filter=risk_filter, sort_by=sort_by, sort_dir=sort_dir,
    )


@history_bp.route("/api/history/<int:prediction_id>", methods=["DELETE"])
@login_required
def api_delete(prediction_id):
    ok = delete_prediction(session["user_id"], prediction_id)
    if ok:
        log_action(session["user_id"], "PREDICTION_DELETED", f"Prediction #{prediction_id} deleted")
    return jsonify({"success": ok})


@history_bp.route("/history/export")
@login_required
def export():
    csv_data = export_csv(session["user_id"])
    log_action(session["user_id"], "HISTORY_EXPORTED", "Prediction history exported as CSV")
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=smartcredit_prediction_history.csv"},
    )
