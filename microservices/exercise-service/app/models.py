from app import db
from sqlalchemy.sql import func


class Exercise(db.Model):
    __tablename__ = "Exercises"
    id = db.Column(db.Integer, primary_key=True)        
    name = db.Column(db.String(100), nullable=False)
    level = db.Column(db.String(50), nullable=False)
    primaryMuscle = db.Column(db.String(50), nullable=False)
    instructions = db.Column(db.String(), nullable=True)
    category = db.Column(db.String(50), nullable=False)
    createdDate = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'<Exercise {self.name} {self.id}>'

    @property
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "level": self.level,
            "primaryMuscle": self.primaryMuscle,
            "instructions": self.instructions,
            "category": self.category,
            "createdDate": self.createdDate
        }
