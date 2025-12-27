from flask_jwt_extended import jwt_required, get_jwt_identity

def admin_only(fn):
    @jwt_required()
    def wrapper(*args, **kwargs):
        admin_id = get_jwt_identity()
        if not admin_id:
            return jsonify({"error": "Admins only"}), 403
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper
