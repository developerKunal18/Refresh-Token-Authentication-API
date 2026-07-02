from datetime import timedelta
from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "super-secret-key"

jwt = JWTManager(app)

users = {
    "admin": "admin123"
}

# ---------- Login ----------
@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if users.get(username) != password:
        return jsonify({
            "message": "Invalid credentials"
        }), 401

    access_token = create_access_token(
        identity=username,
        expires_delta=timedelta(minutes=15)
    )

    refresh_token = create_refresh_token(
        identity=username,
        expires_delta=timedelta(days=7)
    )

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token
    })


# ---------- Refresh ----------
@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():

    user = get_jwt_identity()

    new_access = create_access_token(
        identity=user
    )

    return jsonify({
        "access_token": new_access
    })


# ---------- Protected ----------
@app.route("/profile")
@jwt_required()
def profile():

    return jsonify({
        "user": get_jwt_identity()
    })


@app.route("/")
def home():

    return jsonify({
        "message": "Refresh Token API"
    })


if __name__ == "__main__":
    app.run(debug=True)
