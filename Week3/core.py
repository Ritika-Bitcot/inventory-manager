import csv
import logging
from datetime import datetime
from typing import List

from pydantic import ValidationError

from Week3.models import PRODUCT_CLASS_MAP, FoodProduct, Product


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
        try:

            category_raw = row.get("category", "")
            category = category_raw.lower().strip() if category_raw else ""

            product_class = PRODUCT_CLASS_MAP.get(category, Product)

            base_fields = [
                "product_id",
                "product_name",
                "category",
                "quantity",
                "price",
            ]

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
        except KeyError as e:
            logging.error(f"Missing required field {e} in row: {row}")

        except ValidationError as e:
            logging.error(f"Validation error in row: {row} - {e}")

        except (ValueError, TypeError) as e:
            logging.error(f"Type error in row: {row} - Error: {e}")
        except Exception as e:
            logging.error(f"Unexpected error processing row: {row} - {e}")

        return None

    def load_from_csv(self, csv_file: str) -> None:
        """
        Loads the inventory from the given CSV file.
        Logs errors for invalid rows.
        """
        try:
            with open(csv_file, newline="") as f:
                reader = csv.DictReader(f)
                for idx, row in enumerate(reader, start=2):
                    product = self.create_product_from_row(row)
                    if product is not None:
                        self.products.append(product)
                    else:
                        logging.warning(f"Row {idx} skipped due to invalid data.")
        except FileNotFoundError:
            logging.error(f"CSV file '{csv_file}' not found.")
        except (ValidationError, ValueError, TypeError) as e:
            idx_info = f"Row {idx}" if "idx" in locals() else "During reading CSV"
            logging.error(f"{idx_info}: {e}")

    def generate_low_stock_report(
        self, threshold: int = 10, output_file: str = "low_stock_report.txt"
    ) -> None:
        """
        Generates a report of products below the given stock threshold.
        Excludes expired FoodProducts.
        """
        try:
            now = datetime.now()
            low_stock_items: List[Product] = [
                p
                for p in self.products
                if p.quantity < threshold
                and not (isinstance(p, FoodProduct) and p.expiry_date < now)
            ]

            with open(output_file, "w", encoding="utf-8") as f:
                if not low_stock_items:
                    logging.info("No products found below the stock threshold.")
                    f.write("✅ All products have sufficient stock levels.\n")
                else:
                    for product in low_stock_items:
                        f.write(f"{product.product_name}: {product.quantity}\n")
        except FileNotFoundError:
            logging.error(f"Output directory for file '{output_file}' not found.")
        except Exception as e:
            logging.error(f"Error writing low stock report: {e}")

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

        Expired FoodProducts are excluded from the summary.
        """
        now = datetime.now()

        valid_products = [
            p
            for p in self.products
            if not (isinstance(p, FoodProduct) and p.expiry_date < now)
        ]

        total_products = len(valid_products)

        if total_products == 0:
            logging.warning(
                "No valid (non-expired) products. Summary values will all be zero."
            )
            return {
                "total_products": 0,
                "total_quantity": 0,
                "hs_name": "N/A",
                "hs_amt": 0.0,
                "total_value": 0.0,
            }

        total_quantity = sum(p.quantity for p in valid_products)
        total_value = sum(p.get_total_value() for p in valid_products)

        if total_quantity == 0:
            logging.warning(
                "Total quantity is zero — all products may be out of stock."
            )

        try:
            highest_sale = max(valid_products, key=lambda p: p.get_total_value())
            hs_name = highest_sale.product_name
            hs_amt = highest_sale.get_total_value()
        except Exception as e:
            logging.error(f"Error calculating highest sale: {e}")
            hs_name, hs_amt = "N/A", 0.0

        return {
            "total_products": total_products,
            "total_quantity": total_quantity,
            "hs_name": hs_name,
            "hs_amt": hs_amt,
            "total_value": total_value,
        }
