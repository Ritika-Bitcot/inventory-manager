import csv
import logging
from typing import List

from models import PRODUCT_CLASS_MAP, Product
from pydantic import ValidationError


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

    def get_summary(self) -> dict:
        """
        Returns a summary of inventory including:
        - Total products
        - Total quantity
        - Highest sale (product and amount)
        - Total value
        """
        total_products = len(self.products)
        total_quantity = sum(p.quantity for p in self.products)
        total_value = self.get_total_inventory()

        if self.products:
            highest_sale = max(self.products, key=lambda p: p.get_total_value())
            hs_name = highest_sale.product_name
            hs_amt = highest_sale.get_total_value()
        else:
            hs_name = "N/A"
            hs_amt = 0.0

        return {
            "total_products": total_products,
            "total_quantity": total_quantity,
            "hs_name": hs_name,
            "hs_amt": hs_amt,
            "total_value": total_value,
        }
