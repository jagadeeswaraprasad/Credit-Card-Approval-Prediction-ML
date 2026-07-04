"""
SmartCredit AI - Application Configuration
Centralised configuration for all environments.
"""

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration shared across environments."""

    SECRET_KEY = os.environ.get("SMARTCREDIT_SECRET_KEY", "smartcredit-ai-dev-secret-2026")

    # Database
    DATABASE_PATH = os.path.join(BASE_DIR, "database", "smartcredit.db")

    # Model artefacts
    MODELS_DIR = os.path.join(BASE_DIR, "models")
    MODEL_PATH = os.path.join(MODELS_DIR, "model.pkl")
    SCALER_PATH = os.path.join(MODELS_DIR, "scaler.pkl")
    ENCODERS_PATH = os.path.join(MODELS_DIR, "encoders.pkl")
    METADATA_PATH = os.path.join(MODELS_DIR, "model_metadata.json")
    FEATURE_IMPORTANCE_PATH = os.path.join(MODELS_DIR, "feature_importance.json")
    METRICS_PATH = os.path.join(MODELS_DIR, "model_metrics.json")

    # Dataset
    DATA_DIR = os.path.join(BASE_DIR, "data")
    DATASET_PATH = os.path.join(DATA_DIR, "credit_card_approval.csv")

    # Logging
    LOG_DIR = os.path.join(BASE_DIR, "logs")
    APP_LOG_PATH = os.path.join(LOG_DIR, "application.log")

    # Session
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    PERMANENT_SESSION_LIFETIME = 60 * 60 * 24 * 7  # 7 days for "remember me"

    # Pagination
    HISTORY_PAGE_SIZE = 10


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config_map = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
