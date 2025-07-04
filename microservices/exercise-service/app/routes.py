from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import Exercise
from app.utilities import generate_token, decode_token


routes_bp = Blueprint('routes', __name__)


