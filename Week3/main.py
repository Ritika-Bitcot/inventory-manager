from core import Inventory
from utils import setup_logger

if __name__ == "__main__":
    setup_logger()
    inventory = Inventory()
    inventory.load_from_csv("data/products.csv")
    print(f"Total Inventory Value: ₹{inventory.get_total_inventory():.2f}")
    inventory.generate_low_stock_report()
