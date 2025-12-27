from flask import Blueprint, request, jsonify
from app.models import Product
from app import db
from app.utils.auth_middleware import admin_required

product_bp = Blueprint("products", __name__, url_prefix="/api/products")

# GET all products (protected)
@product_bp.get("/")
@admin_required
def get_products():
    products = Product.query.all()
    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "category": p.category,
            "image_url": p.image_url,
            "featured": p.featured,
            "created_at": p.created_at,
            "updated_at": p.updated_at
        }
        for p in products
    ])

# GET product by ID
@product_bp.get("/<int:id>")
@admin_required
def get_product(id):
    p = Product.query.get_or_404(id)
    return {
        "id": p.id,
        "name": p.name,
        "price": p.price,
        "category": p.category,
        "image_url": p.image_url,
        "featured": p.featured
    }

# CREATE product
@product_bp.post("/")
@admin_required
def create_product():
    data = request.json

    new_product = Product(
        name=data["name"],
        price=data["price"],
        category=data["category"],
        image_url=data.get("image_url"),
        featured=data.get("featured", False),
        admin_id=request.admin_id  # from JWT
    )

    db.session.add(new_product)
    db.session.commit()

    return {"message": "Product created successfully!"}, 201

# UPDATE product
@product_bp.put("/<int:id>")
@admin_required
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.json

    product.name = data.get("name", product.name)
    product.price = data.get("price", product.price)
    product.category = data.get("category", product.category)
    product.image_url = data.get("image_url", product.image_url)
    product.featured = data.get("featured", product.featured)

    db.session.commit()

    return {"message": "Product updated successfully!"}

# DELETE product
@product_bp.delete("/<int:id>")
@admin_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()

    return {"message": "Product deleted successfully!"}
