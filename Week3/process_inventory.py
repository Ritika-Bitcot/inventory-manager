from pydantic import BaseModel, Field, ValidationError
import csv
import logging
from typing import List

#  Setup logging
def setup_logger(log_file: str = 'errors.log'):
    """
    Set up a logger with the given file name that logs errors to that file.
    """
    logging.basicConfig(filename=log_file, level=logging.ERROR, filemode='w')

class Product(BaseModel):
    product_id:int=(Field(...,gt=0))
    product_name:str
    quantity:int=Field(...,ge=0)
    price:float=Field(...,gt=0)

    def get_total_value(self) -> float:
        """
        Returns the total value of the product (price * quantity).
        """
        return self.price * self.quantity

class Inventory:
    def __init__(self):
        self.products:List[Product] = []
    def load_from_csv(self,csv_file: str)->None:
        """
        Load and validate products from a CSV file into the inventory.
        """
        with open(csv_file, newline='') as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader, start=2):  # start=2 to account for header
                try:
                    product = Product(
                        product_id=int(row['product_id']),
                        product_name=row['product_name'],
                        quantity=int(row['quantity']),
                        price=float(row['price'])
                    )
                    self.products.append(product)

                except (ValidationError, ValueError) as e:
                    logging.error(f"Row {idx}: {e}")
        
    def generate_low_stock_report(self, threshold: int = 10, output_file: str = 'low_stock_report.txt'):
        """
        Generate a report for products whose quantity is below the threshold.
        """
        with open(output_file, 'w') as f:
            for product in self.products:
                if product.quantity < threshold:
                    f.write(f"{product.product_name}: {product.quantity}\n")    

    def get_total_inventory_value(self) -> float:
        """
        Returns the total value of all products in the inventory.
        """
        return sum(p.get_total_value() for p in self.products)



if __name__ == '__main__':
    setup_logger()  
    inventory = Inventory()
    inventory.load_from_csv('inventory.csv')

    print(f"Total Inventory Value: ₹{inventory.get_total_inventory_value():.2f}")

    inventory.generate_low_stock_report()

