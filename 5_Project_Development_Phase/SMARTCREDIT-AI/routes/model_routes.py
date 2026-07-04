"""SmartCredit AI - Model Performance Routes"""

import json
from flask import Blueprint, render_template
from utils.decorators import login_required
from config import Config

model_bp = Blueprint("model", __name__)


@model_bp.route("/model-performance")
@login_required
def model_performance():
    with open(Config.METRICS_PATH) as f:
        metrics = json.load(f)
    with open(Config.METADATA_PATH) as f:
        metadata = json.load(f)
    with open(Config.FEATURE_IMPORTANCE_PATH) as f:
        feature_importance = json.load(f)

    return render_template(
        "model_performance.html", metrics=metrics, metadata=metadata,
        feature_importance=feature_importance,
    )
