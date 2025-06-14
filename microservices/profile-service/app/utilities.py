import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os


load_dotenv()
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")


def generate_token(client_id):
    payload = {
        "sub": client_id,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
        "iat": datetime.now(timezone.utc)
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")
    return token


def decode_token(token):
    return jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
