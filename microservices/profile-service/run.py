from app import build_app, db

app = build_app()

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(port=8001, debug=True)
