from functools import wraps
from flask import request, jsonify, current_app
import jwt

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get("Authorization")

        if not auth or not auth.startswith("Bearer "):
            return jsonify({"error": "Token missing or invalid"}), 401

        token = auth.split(" ", 1)[1]

        try:
            decoded = jwt.decode(
                token,
                current_app.config["SECRET_KEY"],
                algorithms=["HS256"]
            )

            # attach admin_id to request
            request.admin_id = decoded.get("admin_id")

            if not request.admin_id:
                return jsonify({"error": "Unauthorized"}), 401

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated

