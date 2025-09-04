import logging
from typing import List

from api.models import Product


class ProductDataLoader:
    """Handles loading of product data from the database."""

    def __init__(self, app, db) -> None:
        self.app = app
        self.db = db

    def load(self) -> List[str]:
        """Load product data (name + category) from database."""
        try:
            with self.app.app_context():
                products = Product.query.all()
                if not products:
                    raise ValueError("No products found in database")

                text_entries = [
                    f"{p.product_name.strip()} {p.category.strip()}".strip()
                    for p in products
                    if p.product_name
                ]

                if not text_entries:
                    raise ValueError("No valid product entries found in database")

                return text_entries
        except Exception as e:
            logging.error("Error loading product data from DB: %s", str(e))
            raise
