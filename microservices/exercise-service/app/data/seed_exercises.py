import csv
from app import db
from app.models import Exercise
import os

CSV_FILE = os.path.join(os.path.dirname(__file__), 'exercises.csv')

def seed_exercises():
    with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Skip if already exists
            if Exercise.query.filter_by(name=row['name']).first():
                continue

            exercise = Exercise(
                id=row['id'],
                name=row['name'],
                level=row['level'],
                primaryMuscle=row['primaryMuscle'],
                instructions=row['instructions'],
                category=row['category']
            )
            db.session.add(exercise)

        db.session.commit()

if __name__ == '__main__':
    seed_exercises()
