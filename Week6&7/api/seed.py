# Week6/api/seed.py
import csv
import os
from datetime import date

import click
from flask import Flask
from flask.cli import with_appcontext

from api.config import BaseConfig
from api.db import db
from api.models import BookProduct, ElectronicProduct, FoodProduct

# ---------- Flask App Setup ----------
app = Flask(__name__)
app.config.from_object(BaseConfig)
db.init_app(app)

# ---------- CSV Path ----------
CSV_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "data", "products.csv"
)

CATEGORY_MAP = {
    "food": FoodProduct,
    "electronic": ElectronicProduct,
    "book": BookProduct,
}


# ---------- Helper: Create Product ----------
def create_product_from_row(
    row: dict,
) -> FoodProduct | ElectronicProduct | BookProduct | None:
    """
    Creates a Product instance based on the given row of data.

    Args:
        row (dict): A dictionary of product data from a CSV row.

    Returns:
        Product: An instance of FoodProduct, ElectronicProduct, or BookProduct.
    """
    category = row.get("category", "").strip().lower()
    model = CATEGORY_MAP.get(category)
    if not model:
        print(f"Skipping unknown category: {category}")
        return None

    try:
        if category == "food":
            mfg_date = date.fromisoformat(row["mfg_date"].strip())
            expiry_date = date.fromisoformat(row["expiry_date"].strip())
            return FoodProduct(
                product_name=row["product_name"].strip(),
                category=category,
                quantity=int(row["quantity"]),
                price=float(row["price"]),
                mfg_date=mfg_date,
                expiry_date=expiry_date,
            )
        elif category == "electronic":
            purchase_date = date.fromisoformat(row["purchase_date"].strip())
            warranty_period = int(row["warranty_period"])
            return ElectronicProduct(
                product_name=row["product_name"].strip(),
                category=category,
                quantity=int(row["quantity"]),
                price=float(row["price"]),
                purchase_date=purchase_date,
                warranty_period=warranty_period,
            )
        elif category == "book":
            return BookProduct(
                product_name=row["product_name"].strip(),
                category=category,
                quantity=int(row["quantity"]),
                price=float(row["price"]),
                author=row["author"].strip(),
                publication_year=int(row["publication_year"]),
            )
    except Exception as e:
        print(f"Error creating product from row {row}: {e}")
        return None


# ---------- Seed Database ----------
@click.command("seed-db")
@with_appcontext
def seed_db() -> None:
    """
    Read CSV and insert products into PostgreSQL database.
    """
    if not os.path.exists(CSV_FILE):
        print(f"CSV file not found: {CSV_FILE}")
        return

    db.create_all()  # Ensure tables exist

    with open(CSV_FILE, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader, start=1):
            product = create_product_from_row(row)
            if product:
                db.session.add(product)
            else:
                print(f"Skipping row {i}: {row}")

        db.session.commit()
    print("Database seeded successfully.")


# ---------- Register CLI Command ----------
app.cli.add_command(seed_db)
