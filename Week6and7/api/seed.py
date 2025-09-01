import csv
import os
from datetime import date

import click
from dotenv import load_dotenv  # 👈 new import
from flask import Flask
from flask.cli import with_appcontext

from api.config import BaseConfig
from api.db import db
from api.models import BookProduct, ElectronicProduct, FoodProduct

# ---------- Load Env ----------
load_dotenv()

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

# ---------- Default Owner ----------
DEFAULT_OWNER_ID = os.getenv("DEFAULT_OWNER_ID", "00000000-0000-0000-0000-000000000000")


# ---------- Helper: Create Product ----------
def create_product_from_row(
    row: dict,
) -> FoodProduct | ElectronicProduct | BookProduct | None:
    """
    Creates a Product instance based on the given row of data.
    Adds a default owner_id from .env so tests and
    seeding work without requiring a user.
    """
    category = row.get("category", "").strip().lower()
    model = CATEGORY_MAP.get(category)
    if not model:
        print(f"Skipping unknown category: {category}")
        return None

    try:
        base_kwargs = {
            "product_name": row["product_name"].strip(),
            "category": category,
            "quantity": int(row["quantity"]),
            "price": float(row["price"]),
            "owner_id": DEFAULT_OWNER_ID,  # 👈 pulled from env
        }

        if category == "food":
            mfg_date = date.fromisoformat(row["mfg_date"].strip())
            expiry_date = date.fromisoformat(row["expiry_date"].strip())
            return FoodProduct(
                **base_kwargs,
                mfg_date=mfg_date,
                expiry_date=expiry_date,
            )
        elif category == "electronic":
            purchase_date = date.fromisoformat(row["purchase_date"].strip())
            warranty_period = int(row["warranty_period"])
            return ElectronicProduct(
                **base_kwargs,
                purchase_date=purchase_date,
                warranty_period=warranty_period,
            )
        elif category == "book":
            return BookProduct(
                **base_kwargs,
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
