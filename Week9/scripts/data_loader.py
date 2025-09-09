# Week8/scripts/data_loader.py
import logging
import os
import sys
from typing import Dict, List

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from api.models import BookProduct, ElectronicProduct, FoodProduct, Product
from dotenv import load_dotenv
from sqlalchemy import create_engine, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def load_products(db_url: str) -> List[Dict]:
    """
    Load all products (Food, Electronic, Book) from the database
    and return a list of dicts with product_id, name, and combined description.
    """
    try:
        engine = create_engine(db_url)
        products_list: List[Dict] = []

        with Session(engine) as session:
            all_products = session.scalars(select(Product)).all()

            for p in all_products:
                description_parts = [
                    f"Category: {p.category}" if getattr(p, "category", None) else "",
                    f"Price: {p.price}" if getattr(p, "price", None) else "",
                    f"Quantity: {p.quantity}" if getattr(p, "quantity", None) else "",
                ]

                # Polymorphic fields
                if isinstance(p, FoodProduct):
                    description_parts.append(f"Expiry Date: {p.expiry_date}")
                    description_parts.append(f"MFG Date: {p.mfg_date}")
                elif isinstance(p, ElectronicProduct):
                    description_parts.append(f"Purchase Date: {p.purchase_date}")
                    description_parts.append(f"Warranty: {p.warranty_period} months")
                elif isinstance(p, BookProduct):
                    description_parts.append(f"Author: {p.author}")
                    description_parts.append(f"Publication Year: {p.publication_year}")

                description = " | ".join([part for part in description_parts if part])

                products_list.append(
                    {
                        "product_id": p.id,
                        "product_name": p.product_name,
                        "description": description,
                    }
                )

        logger.info(f"Loaded {len(products_list)} products from database.")
        return products_list

    except SQLAlchemyError as e:
        logger.error(f"Database error while loading products: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error in load_products: {e}", exc_info=True)
        return []
