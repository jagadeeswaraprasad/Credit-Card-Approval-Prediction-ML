"""SmartCredit AI - Main / Landing Routes"""

import json
from flask import Blueprint, render_template, session, redirect, url_for
from config import Config

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def landing():
    if "user_id" in session:
        return redirect(url_for("dashboard.dashboard"))

    metrics = {}
    metadata = {}
    try:
        with open(Config.METRICS_PATH) as f:
            metrics = json.load(f)
        with open(Config.METADATA_PATH) as f:
            metadata = json.load(f)
    except FileNotFoundError:
        pass

    return render_template("landing.html", metrics=metrics, metadata=metadata)
