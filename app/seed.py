from app import create_app, db
from app.models import Admin

app = create_app()

with app.app_context():
    admin = Admin(username="admin")
    admin.set_password("admin123")  # change later
    db.session.add(admin)
    db.session.commit()
    print("Admin created!")
