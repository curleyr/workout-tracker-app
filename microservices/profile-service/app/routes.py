from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import Profiles
from app.utilities import generate_token, decode_token


routes_bp = Blueprint("routes", __name__)


@routes_bp.route("/create", methods=["POST"])
def create():
    data = request.get_json()
    
    required_fields = ["id", "firstName", "lastName", "email"]
    missing_fields = [field for field in required_fields if not data.get(field)]

    # Missing required parameters in request
    if missing_fields: 
        return jsonify({
            "status": "ERROR",
            "message": f"Missing required fields: {', '.join(missing_fields)}"
        }), 400

    try:
        # Profile already exists in the db
        if Profiles.query.filter_by(id=data["id"]).first():
            return jsonify({
                "status": "ERROR",
                "message": "Profile already exists"
            }), 400

        # Create profile
        profile = Profiles(
            id=data["id"],
            firstName=data["firstName"],
            lastName=data["lastName"],
            email=data["email"]
        )
        db.session.add(profile)
        db.session.commit()

        return jsonify({
            "status": "OK",
            "message": "Profile created",
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "ERROR",
            "message": "Internal server error"
        }), 500
