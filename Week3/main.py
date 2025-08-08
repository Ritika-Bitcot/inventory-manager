import os

from .core import Inventory
from .utils import setup_logger


def display_summary(summary: dict) -> None:
    """
    Displays inventory summary in a user-friendly format.
    """
    print("\n📊 INVENTORY SUMMARY DASHBOARD\n")
    print(f"🧾 Total Products       : {summary['total_products']}")
    print(f"📦 Total Quantity       : {summary['total_quantity']}")
    print(f"🔥 Highest Sale Product : {summary['hs_name']} (₹{summary['hs_amt']:.2f})")
    print(f"💰 Total Inventory Value: ₹{summary['total_value']:.2f}\n")


def main() -> None:
    """
    Main function to run the inventory summary process with error handling.
    """
    setup_logger()

    try:
        inventory = Inventory()
        base_dir = os.path.dirname(__file__)
        data_path = os.path.join(base_dir, "data", "products.csv")
        print(f"Loading data from: {data_path}")
        inventory.load_from_csv(data_path)

        summary = inventory.get_summary()
        display_summary(summary)
        inventory.generate_low_stock_report()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
