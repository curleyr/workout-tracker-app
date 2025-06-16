from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import Users
from app.utilities import generate_token, decode_token
import requests


routes_bp = Blueprint('routes', __name__)
# Docker sets up internal DNS so containers can be reached by name
PROFILE_SERVICE_URL = "http://profile-service:8001/profile/create"


@routes_bp.route("/token", methods=["POST"])
def token():
    token_request = request.get_json()
    client_id = token_request.get('client_id')
    client_secret = token_request.get('client_secret')

    try:
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
    
    except Exception as e:
        return jsonify({
            "status": "ERROR",
            "message": "Internal server error"
        }), 500


@routes_bp.route("/register", methods=["POST"])
def register():
    register_request = request.get_json()
    username = register_request.get("username")
    first_name = register_request.get("firstName")
    last_name = register_request.get("lastName")
    email = register_request.get("email")
    password = register_request.get("password")

    # Missing parameters in request
    if not all([username, first_name, last_name, email, password]):
        return jsonify({
            "status": "ERROR",
            "message": "Missing fields"
        }), 400

    # User already exists in the db
    if Users.query.filter_by(username=username).first():
        return jsonify({
            "status": "ERROR",
            "message": "User already exists"
        }), 400

    try:
        # Create user
        user = Users(
            username=username,
            password=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()

        # Make request to profile-service to create profile
        profile_data = {
            "id": user.id,
            "firstName": first_name,
            "lastName": last_name,
            "email": email
        }
        response = requests.post(PROFILE_SERVICE_URL, json=profile_data)

        # Check if user successfully created
        if response.status_code != 201:
            # Remove user from users table
            db.session.delete(user)
            db.session.commit()
            return jsonify({
                "status": "ERROR",
                "message": "Failed to create profile"
            }), 500

        return jsonify({
            "status": "OK",
            "message": "User created",
        }), 201
    
    except requests.RequestException as e:
        db.session.delete(user)
        db.session.commit()
        return jsonify({
            "status": "ERROR",
            "message": "Profile service unreachable"
        }), 503

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "ERROR",
            "message": "Internal server error"
        }), 500


@routes_bp.route("/login", methods=["POST"])
def login():
    login_request = request.get_json()
    username = login_request.get("username")
    password = login_request.get("password")

    try:
        # Missing parameters in request
        if not all([username, password]):
            return jsonify({
                "status": "ERROR",
                "message": "Missing fields"
            }), 400

        # User doesn't exist in the db
        user = Users.query.filter_by(username=username).first()
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
            "access_token": generate_token(user.id),
            "token_type": "Bearer",
            "expires_in": 3600
        }), 200

    except Exception as e:
        return jsonify({
            "status": "ERROR",
            "message": "Internal server error"
        }), 500    