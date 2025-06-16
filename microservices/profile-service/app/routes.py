from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import Profiles
from app.utilities import generate_token, decode_token


routes_bp = Blueprint('routes', __name__)


@routes_bp.route("/create", methods=["POST"])
def create():
    create_request = request.get_json()
    user_id = create_request.get("id")
    first_name = create_request.get("firstName")
    last_name = create_request.get("lastName")
    email = create_request.get("email")

    # Missing parameters in request
    if not all([user_id, first_name, last_name, email]):
        return jsonify({
            "status": "ERROR",
            "message": "Missing fields"
        }), 400

    # Profile already exists in the db
    if Profiles.query.filter_by(id=user_id).first():
        return jsonify({
            "status": "ERROR",
            "message": "Profile already exists"
        }), 400

    try:
        # Create profile
        profile = Profiles(
            id=user_id,
            firstName=first_name,
            lastName=last_name,
            email=email
        )
        db.session.add(profile)
        db.session.commit()

        return jsonify({
            "status": "OK",
            "message": "Profile created",
        }), 201

    except Exception as e:
        return jsonify({
            "status": "ERROR",
            "message": "Internal server error"
        }), 500