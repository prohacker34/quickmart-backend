import os
from app import create_app, db

app = create_app()

with app.app_context():
    try:
        db.engine.execute("SELECT 1")
        print("Database connected successfully!")
    except Exception as e:
        print("Database connection failed:", e)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # default 5000
    app.run(host="0.0.0.0", port=port, debug=True)
