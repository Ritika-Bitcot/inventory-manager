from core import Inventory
from utils import setup_logger


def display_summary(summary: dict) -> None:
    """
    Displays inventory summary in a user-friendly format.
    """
    print("\n📊 INVENTORY SUMMARY DASHBOARD\n")
    print(f"🧾 Total Products       : {summary['total_products']}")
    print(f"📦 Total Quantity       : {summary['total_quantity']}")
    print(f"🔥 Highest Sale Product : {summary['hs_name']} (₹{summary['hs_amt']:.2f})")
    print(f"💰 Total Inventory Value: ₹{summary['total_value']:.2f}\n")


def main():
    """
    Main function to run the inventory summary process.
    """
    setup_logger()
    inventory = Inventory()
    inventory.load_from_csv("data/products.csv")

    summary = inventory.get_summary()
    display_summary(summary)

    inventory.generate_low_stock_report()

    if summary["total_products"] > 0 and summary["total_quantity"] > 0:
        print("✅ Low stock report generated for all products.\n")
    else:
        print("⚠️ Warning: No inventory data found or all quantities are zero.\n")


if __name__ == "__main__":
    setup_logger()
    inventory = Inventory()
    inventory.load_from_csv("data/products.csv")

    summary = inventory.get_summary()
    display_summary(summary)

    inventory.generate_low_stock_report()
