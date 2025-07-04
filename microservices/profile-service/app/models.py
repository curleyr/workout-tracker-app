from app import db
from sqlalchemy.sql import func


class Profiles(db.Model):
    __tablename__ = "Profiles"
    id = db.Column(db.Integer, primary_key=True)        # Key from Users table in auth_db
    firstName = db.Column(db.String(100), nullable=False)
    lastName = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    createdDate = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Profile {self.email} {self.id}>"

    @property
    def serialize(self):
        return {
            "id": self.id,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "email": self.email,
            "createdDate": self.createdDate
        }
