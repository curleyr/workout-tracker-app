from app import build_app, db

app = build_app()

# Seed database after app context is ready
with app.app_context():
    from app.models import Exercise
    from app.data.seed_exercises import seed_exercises

    # Create tables - only runs of they don't exist
    db.create_all()

    # Seed if table is empty
    if not Exercise.query.first():
        seed_exercises()

if __name__ == '__main__':
    app.run(port=8002, debug=True)
