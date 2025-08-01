import csv
import logging
from typing import List

from pydantic import BaseModel, Field, ValidationError


#  Setup logging
def setup_logger(log_file: str = "errors.log"):
    """
    Set up a logger with the given file name that logs errors to that file.
    """
    logging.basicConfig(filename=log_file, level=logging.ERROR, filemode="w")


class Product(BaseModel):
    product_id: int = Field(..., gt=0)
    product_name: str
    quantity: int = Field(..., ge=0)
    price: float = Field(..., gt=0)


def load_and_validate_products(csv_file: str) -> List[Product]:
    """
    Reads a CSV file, validates the data
    against the Product model,
    and returns a list of valid products.
    """
    valid_products = []

    with open(csv_file, newline="") as f:
        reader = csv.DictReader(f)
        # start=2 to account for header
        for idx, row in enumerate(reader, start=2):
            try:
                product = Product(
                    product_id=int(row["product_id"]),
                    product_name=row["product_name"],
                    quantity=int(row["quantity"]),
                    price=float(row["price"]),
                )
                valid_products.append(product)
            except (ValidationError, ValueError) as e:
                logging.error(f"Row {idx}: {e}")

    return valid_products


def generate_low_stock_report(
    products: List[Product],
    threshold: int = 10,
    output_file: str = "low_stock_report.txt",
):
    """
    Generates a low stock report based
    on the given list of products
    and a threshold for quantity.
    """
    with open(output_file, "w") as f:
        for product in products:
            if product.quantity < threshold:
                f.write(f"{product.product_name}: {product.quantity}\n")


if __name__ == "__main__":
    setup_logger()
    products = load_and_validate_products("inventory.csv")
    generate_low_stock_report(products)
