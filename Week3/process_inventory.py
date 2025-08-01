from datetime import datetime
from pydantic import BaseModel, Field, ValidationError, model_validator
from dateutil.relativedelta import relativedelta
import csv
import logging
from typing import List, Optional


# Setup logging
def setup_logger(log_file: str = "errors.log"):
    logging.basicConfig(filename=log_file, level=logging.ERROR, filemode="w")


# Product Registry
PRODUCT_CLASS_MAP = {}


def register_product_type(category: str) -> callable:
    """
    Registers a product type with the given category.
    The category is converted to lower case to ensure that
    the mapping is case-insensitive.
    """

    def decorator(cls):
        PRODUCT_CLASS_MAP[category.lower()] = cls
        return cls

    return decorator


# Base Product
class Product(BaseModel):
    product_id: int = Field(..., gt=0)
    product_name: str = Field(..., min_length=3, max_length=50)
    category: Optional[str]
    quantity: int = Field(..., ge=0)
    price: float = Field(..., gt=0)

    def get_total_value(self) -> float:
        """
        Returns the total value of the product based on its price and quantity.
        """
        return self.price * self.quantity


# Subclasses (registered dynamically)
@register_product_type("food")
class FoodProduct(Product):
    category: str = "food"
    mfg_date: datetime
    expiry_date: datetime

    @model_validator(mode="after")
    def check_expiry_after_mfg(self) -> Product:
        """
        Checks if the expiry date is after the manufacturing date.
        """
        if self.expiry_date <= self.mfg_date:
            raise ValueError("expiry_date must be after mfg_date")
        return self


@register_product_type("electronic")
class ElectronicProduct(Product):
    category: str = "electronic"
    purchase_date: datetime
    warranty_period: int = Field(..., ge=0)

    def get_warranty_end_date(self) -> datetime:
        """
        Calculates the warranty end date based on the purchase date.
        """
        return self.purchase_date + relativedelta(months=self.warranty_period)


@register_product_type("book")
class BookProduct(Product):
    category: str = "book"
    author: str = Field(..., min_length=3)
    publication_year: int = Field(..., ge=1000, le=datetime.now().year)


# Inventory Management
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


# === Run the Program ===
if __name__ == "__main__":
    setup_logger()
    inventory = Inventory()
    inventory.load_from_csv("inventory.csv")
    print(f"Total Inventory Value: ₹{inventory.get_total_inventory():.2f}")
    inventory.generate_low_stock_report()
