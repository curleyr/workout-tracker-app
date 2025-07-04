from app import db
from sqlalchemy.sql import func


class Users(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    createdDate = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<User {self.username} {self.id}>"

    @property
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "createdDate": self.createdDate
        }
