"""SmartCredit AI - Dashboard Routes"""

from flask import Blueprint, render_template, session
from utils.decorators import login_required
from services.stats_service import get_dashboard_stats

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    stats = get_dashboard_stats(session["user_id"])
    return render_template("dashboard.html", stats=stats)
