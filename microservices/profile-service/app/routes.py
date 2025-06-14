from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import Profiles
from app.utilities import generate_token, decode_token


routes_bp = Blueprint('routes', __name__)

"""
@routes_bp.route("/token", methods=["POST"])
def token():
    token_request = request.get_json()
    client_id = token_request.get('client_id')
    client_secret = token_request.get('client_secret')

    # Missing parameters in request
    if not all([client_id, client_secret]):
        return jsonify({
            "status": "ERROR",
            "message": "Missing fields"
        }), 400

    # Generate and return bearer token
    token = generate_token(token_request.get('client_id'))

    return jsonify({
        "status": "OK",
        "access_token": token,
        "token_type": "Bearer",
        "expires_in": 3600
    }), 200


@routes_bp.route("/register", methods=["POST"])
def register():
    register_request = request.get_json()
    first_name = register_request.get("firstName")
    last_name = register_request.get("lastName")
    email = register_request.get("email")
    password = register_request.get("password")

    # Missing parameters in request
    if not all([first_name, last_name, email, password]):
        return jsonify({
            "status": "ERROR",
            "message": "Missing fields"
        }), 400

    # User already exists in the db
    if Users.query.filter_by(email=email).first():
        return jsonify({
            "status": "ERROR",
            "message": "User already exists"
        }), 400

    # Add user to db
    user = Users(
        firstName=first_name,
        lastName=last_name,
        email=email,
        password=generate_password_hash(password)
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "status": "OK",
        "message": "User created",
    }), 201


@routes_bp.route("/login", methods=["POST"])
def login():
    login_request = request.get_json()
    email = login_request.get("email")
    password = login_request.get("password")

    # Missing parameters in request
    if not all([email, password]):
        return jsonify({
            "status": "ERROR",
            "message": "Missing fields"
        }), 400

    # User doesn't exist in the db
    user = Users.query.filter_by(email=email).first()
    if not user:
        return jsonify({
            "status": "ERROR",
            "message": "User doesn't exist"
        }), 400

    # Invalid password
    if not check_password_hash(user.password, password):
        return jsonify({
            "status": "ERROR",
            "message": "Invalid password"
        }), 400

    # Success - generate token for frontend to access protected resources
    return jsonify({
        "status": "OK",
        "message": "Successful login",
        "access_token": generate_token(user.email),
        "token_type": "Bearer",
        "expires_in": 3600
    }), 200
"""