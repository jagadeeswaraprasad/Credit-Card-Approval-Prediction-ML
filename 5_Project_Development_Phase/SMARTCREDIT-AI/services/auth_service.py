"""SmartCredit AI - Authentication Service"""

from werkzeug.security import generate_password_hash, check_password_hash
from utils.db import get_connection
from utils.logger import get_logger

logger = get_logger("auth_service")


def create_user(full_name: str, email: str, password: str):
    conn = get_connection()
    try:
        existing = conn.execute("SELECT id FROM users WHERE email = ?", (email.lower(),)).fetchone()
        if existing:
            return None, "An account with this email already exists."
        password_hash = generate_password_hash(password)
        cur = conn.execute(
            "INSERT INTO users (full_name, email, password_hash) VALUES (?, ?, ?)",
            (full_name.strip(), email.lower().strip(), password_hash),
        )
        conn.commit()
        user_id = cur.lastrowid
        log_action(user_id, "REGISTER", f"New account created for {email}")
        return user_id, None
    finally:
        conn.close()


def authenticate_user(email: str, password: str):
    conn = get_connection()
    try:
        user = conn.execute("SELECT * FROM users WHERE email = ?", (email.lower().strip(),)).fetchone()
        if not user:
            return None, "No account found with this email."
        if not check_password_hash(user["password_hash"], password):
            log_action(user["id"], "LOGIN_FAILED", "Incorrect password")
            return None, "Incorrect password."
        conn.execute("UPDATE users SET last_login = datetime('now') WHERE id = ?", (user["id"],))
        conn.commit()
        log_action(user["id"], "LOGIN_SUCCESS", "User logged in")
        return dict(user), None
    finally:
        conn.close()


def get_user_by_id(user_id: int):
    conn = get_connection()
    try:
        user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return dict(user) if user else None
    finally:
        conn.close()


def log_action(user_id, action, details, ip_address=None):
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO audit_logs (user_id, action, details, ip_address) VALUES (?, ?, ?, ?)",
            (user_id, action, details, ip_address),
        )
        conn.commit()
        logger.info(f"AUDIT | user_id={user_id} | {action} | {details}")
    finally:
        conn.close()
