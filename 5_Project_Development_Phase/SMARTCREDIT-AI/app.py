"""
SmartCredit AI - Enterprise Credit Card Approval & Risk Assessment Platform
=============================================================================
Application entrypoint. Run with:  python app.py
"""

import os
from flask import Flask, render_template
from config import config_map
from utils.db import init_db
from utils.logger import get_logger

logger = get_logger("app")


def create_app(env: str = None):
    env = env or os.environ.get("FLASK_ENV", "default")
    app = Flask(__name__)
    app.config.from_object(config_map.get(env, config_map["default"]))

    # ---- Database ----
    init_db()

    # ---- Blueprints ----
    from routes.main_routes import main_bp
    from routes.auth_routes import auth_bp
    from routes.dashboard_routes import dashboard_bp
    from routes.prediction_routes import prediction_bp
    from routes.history_routes import history_bp
    from routes.model_routes import model_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(prediction_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(model_bp)

    # ---- Context processors ----
    @app.context_processor
    def inject_globals():
        from flask import session
        return {"current_user_name": session.get("full_name"), "is_authenticated": "user_id" in session}

    # ---- Error handlers ----
    @app.errorhandler(404)
    def not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        logger.exception("Internal server error")
        return render_template("errors/500.html"), 500

    logger.info("SmartCredit AI application initialised.")
    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
