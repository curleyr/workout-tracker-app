from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import Exercise
from app.utilities import generate_token, decode_token


routes_bp = Blueprint("routes", __name__)


@routes_bp.route("/create", methods=["POST"])
def create_exercise():
    data = request.get_json()

    required_fields = ["name", "level", "primaryMuscle", "category"]
    missing_fields = [field for field in required_fields if not data.get(field)]

    # Missing required parameters in request
    if missing_fields: 
        return jsonify({
            "status": "ERROR",
            "message": f"Missing required fields: {', '.join(missing_fields)}"
        }), 400
    
    try:
        # Exercise already exists in the db
        if Exercise.query.filter_by(name=data["name"]).first():
            return jsonify({
                "status": "ERROR",
                "message": "An exercise with that name already exists"
            }), 400
        
        # Create exercise
        exercise_data = {field: data[field] for field in required_fields}
        exercise = Exercise(**exercise_data)    # Unpack dictionary

        if data.get("id"):  # Optional custom ID
            exercise.id = data["id"]

        if data.get("instructions"):  # Optional instructions
            exercise.instructions = data["instructions"]

        db.session.add(exercise)
        db.session.commit()

        return jsonify({
            "status": "OK",
            "message": "Exercise created",
            "exercise": exercise.serialize
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "ERROR",
            "message": "Internal server error"
        }), 500
    

@routes_bp.route("/<int:id>", methods=["GET"])
def get_exercise_by_id(id):
    try:
        exercise = Exercise.query.get(id)

        if not exercise:
            return jsonify({
                "status": "ERROR",
                "message": f"Exercise with id {id} not found"
            }), 404
        
        return jsonify({
                "status": "OK",
                "message": "Exercise retrieved",
                "exercise": exercise.serialize
            }), 200
    
    except Exception as e:
        return jsonify({
            "status": "ERROR",
            "message": "Internal server error"
        }), 500


@routes_bp.route("/name/<string:name>", methods=["GET"])
def get_exercise_by_name(name):
    try:
        exercise = Exercise.query.filter_by(name=name).first()
        
        if not exercise:
            return jsonify({
                "status": "ERROR",
                "message": f"Exercise with name {name} not found"
            }), 404

        return jsonify({
            "status": "OK",
            "message": "Exercise retrieved",
            "exercise": exercise.serialize
        }), 200
    
    except Exception as e:
        return jsonify({
            "status": "ERROR",
            "message": "Internal server error"
        }), 500


@routes_bp.route("/", methods=["GET"])
def get_all_exercises():
    try:
        exercises = Exercise.query.all()
        
        if not exercises:
            return jsonify({
                "status": "ERROR",
                "message": "No exercises found"
            }), 404

        return jsonify({
            "status": "OK",
            "message": "Exercises retrieved",
            "exercises": [exercise.serialize for exercise in exercises]
        }), 200

    except Exception as e:
        return jsonify({
            "status": "ERROR",
            "message": "Internal server error"
        }), 500


@routes_bp.route("/<int:id>", methods=["PUT"])
def update_exercise(id):
    data = request.get_json()
    try:
        exercise = Exercise.query.get(id)

        if not exercise:
            return jsonify({
                "status": "ERROR",
                "message": f"Exercise with id {id} not found"
            }), 404
    
        for field in ["id", "name", "level", "primaryMuscle", "instructions", "category"]:
            if field in data:
                setattr(exercise, field, data[field])
        db.session.commit()
        
        return jsonify({
                "status": "OK",
                "message": "Exercise updated",
                "exercise": exercise.serialize
            }), 200
    
    except Exception as e:
        return jsonify({
            "status": "ERROR",
            "message": "Internal server error"
        }), 500


@routes_bp.route("/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    try:
        exercise = Exercise.query.get(id)

        if not exercise:
            return jsonify({
                "status": "ERROR",
                "message": f"Exercise with id {id} not found"
            }), 404
        
        db.session.delete(exercise)
        db.session.commit()
        
        return jsonify({
            "status": "OK",
            "message": "Exercise deleted"
        }), 200
    
    except Exception as e:
        return jsonify({
            "status": "ERROR",
            "message": "Internal server error"
        }), 500
