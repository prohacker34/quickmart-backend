import os
from app import create_app, db
from flask_cors import CORS   # <<<<< import CORS

app = create_app()

# Enable CORS for the whole app
CORS(app, resources={r"/*": {"origins": "*"}})  # <<<<< allow all origins
# OR limit to your frontend
# CORS(app, resources={r"/*": {"origins": "https://your-frontend-url.com"}})

with app.app_context():
    try:
        db.engine.execute("SELECT 1")
        print("Database connected successfully!")
    except Exception as e:
        print("Database connection failed:", e)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # default 5000
    app.run(host="0.0.0.0", port=port, debug=True)
