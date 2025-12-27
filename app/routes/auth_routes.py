# app/routes/auth_routes.py
from flask import Blueprint, request, jsonify
from app.models import Admin
from app import db
import jwt
from datetime import datetime,timedelta
from functools import wraps
from flask import current_app
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# ---------------------------
# Generate JWT
# ---------------------------
def generate_token(admin):
    payload = {
        "admin_id": admin.id,  # <-- key now matches middleware
        "username": admin.username,
        "exp": datetime.utcnow() + timedelta(hours=24),
    }

    return jwt.encode(
        payload,
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )


# ---------------------------
# Admin Login
# ---------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    username = data.get("username")
    password = data.get("password")

    admin = Admin.query.filter_by(username=username).first()

    if not admin or not admin.check_password(password):
        return jsonify({"error": "Invalid username or password"}), 401

    token = generate_token(admin)

    return jsonify({
        "message": "Login successful",
        "token": token,
        "admin": {
            "id": admin.id,
            "username": admin.username
        }
    })


# ---------------------------
# Token Required Decorator
# ---------------------------
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()  # ensures token is valid
        admin_id = get_jwt_identity()  # automatically reads identity from token
        admin = Admin.query.get(admin_id)
        if not admin:
            return jsonify({"error": "Admin not found"}), 401
        return fn(admin, *args, **kwargs)
    return wrapper


# ---------------------------
# Verify Token
# ---------------------------
@auth_bp.route("/me", methods=["GET"])
@admin_required
def get_me(admin):
    return jsonify({
        "id": admin.id,
        "username": admin.username
    })
