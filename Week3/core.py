import csv
import logging
from typing import List
from pydantic import ValidationError
from models import Product, PRODUCT_CLASS_MAP


class Inventory:
    def __init__(self):
        """
        Initializes the Inventory with an empty list of products.
        """
        self.products: List[Product] = []

    def create_product_from_row(self, row: dict) -> Product:
        """
        Creates a Product instance based on the given row of data.
        """
        category_raw = row.get("category", "")
        category = category_raw.lower().strip() if category_raw else ""
        product_class = PRODUCT_CLASS_MAP.get(category, Product)

        base_fields = ["product_id", "product_name", "category", "quantity", "price"]

        try:
            base_data = {
                "product_id": int(row["product_id"]),
                "product_name": row["product_name"],
                "category": category_raw if category_raw else None,
                "quantity": int(row["quantity"]),
                "price": float(row["price"]),
            }

            extra_data = {
                k: v for k, v in row.items() if k not in base_fields and v != ""
            }

            return product_class(**base_data, **extra_data)
        except Exception as e:
            raise e

    def load_from_csv(self, csv_file: str) -> None:
        """
        Loads the inventory from the given CSV file.
        Logs errors for invalid rows.
        """
        with open(csv_file, newline="") as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader, start=2):
                try:
                    product = self.create_product_from_row(row)
                    self.products.append(product)
                except (ValidationError, ValueError, TypeError) as e:
                    logging.error(f"Row {idx}: {e}")

    def generate_low_stock_report(
        self, threshold: int = 10, output_file: str = "low_stock_report.txt"
    ) -> None:
        """
        Generates a report of products below the given stock threshold.
        """
        with open(output_file, "w") as f:
            for product in self.products:
                if product.quantity < threshold:
                    f.write(f"{product.product_name}: {product.quantity}\n")

    def get_total_inventory(self) -> float:
        """
        Calculates the total value of the inventory.
        """
        return sum(p.get_total_value() for p in self.products)
