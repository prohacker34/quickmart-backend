from datetime import datetime
from app import create_app, db
from app.models import Admin, Product

app = create_app()

with app.app_context():
    # Check if admin exists
    admin = Admin.query.filter_by(username="admin").first()
    if not admin:
        admin = Admin(username="admin")
        admin.set_password("Oyaore123")  # change this later for security
        db.session.add(admin)
        db.session.commit()
        print("Admin created!")
    else:
        print("Admin already exists, skipping creation.")

    # Product data
    products = [
        {
            "name": "Wireless Headphones",
            "price": 79.99,
            "category": "Electronics",
            "image_url": "https://example.com/images/headphones.jpg",
            "featured": True,
        },
        {
            "name": "Coffee Mug",
            "price": 12.50,
            "category": "Kitchen",
            "image_url": "https://example.com/images/mug.jpg",
            "featured": False,
        },
        {
            "name": "Gaming Mouse",
            "price": 49.99,
            "category": "Electronics",
            "image_url": "https://example.com/images/mouse.jpg",
            "featured": True,
        },
    ]

    # Seed products (avoid duplicates based on name)
    for product_data in products:
        existing_product = Product.query.filter_by(name=product_data["name"]).first()
        if not existing_product:
            product = Product(
                name=product_data["name"],
                price=product_data["price"],
                category=product_data["category"],
                image_url=product_data["image_url"],
                featured=product_data["featured"],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.session.add(product)

    db.session.commit()
    print("Products seeded successfully!")
