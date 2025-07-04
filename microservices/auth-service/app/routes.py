from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import Users
from app.utilities import generate_token, decode_token
import requests


routes_bp = Blueprint("routes", __name__)
# Docker sets up internal DNS so containers can be reached by name
PROFILE_SERVICE_URL = "http://profile-service:8001/profile/create"


@routes_bp.route("/token", methods=["POST"])
def token():
    data = request.get_json()

    required_fields = ["client_id", "client_secret"]
    missing_fields = [field for field in required_fields if not data.get(field)]

    # Missing required parameters in request
    if missing_fields: 
        return jsonify({
            "status": "ERROR",
            "message": f"Missing required fields: {', '.join(missing_fields)}"
        }), 400

    try:
        # Generate and return bearer token
        token = generate_token(data.get("client_id"))

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
    data = request.get_json()

    required_fields = ["username", "firstName", "lastName", "email", "password"]
    missing_fields = [field for field in required_fields if not data.get(field)]

    # Missing required parameters in request
    if missing_fields: 
        return jsonify({
            "status": "ERROR",
            "message": f"Missing required fields: {', '.join(missing_fields)}"
        }), 400

    try:
        # User already exists in the db
        if Users.query.filter_by(username=data["username"]).first():
            return jsonify({
                "status": "ERROR",
                "message": "User already exists"
            }), 400

        # Create user
        user = Users(
            username=data["username"],
            password=generate_password_hash(data["password"])
        )
        db.session.add(user)
        db.session.commit()

        # Make request to profile-service to create profile
        profile_data = {
            "id": user.id,
            "firstName": data["firstName"],
            "lastName": data["lastName"],
            "email": data["email"]
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
    data = request.get_json()

    required_fields = ["username", "password"]
    missing_fields = [field for field in required_fields if not data.get(field)]

    # Missing required parameters in request
    if missing_fields: 
        return jsonify({
            "status": "ERROR",
            "message": f"Missing required fields: {', '.join(missing_fields)}"
        }), 400

    try:
        # User doesn't exist in the db
        user = Users.query.filter_by(username=data["username"]).first()
        if not user:
            return jsonify({
                "status": "ERROR",
                "message": "User doesn't exist"
            }), 400

        # Invalid password
        if not check_password_hash(user.password, data["password"]):
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