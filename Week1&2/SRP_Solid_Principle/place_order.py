"""
SRP Violation:

def place_order(order: list)->None:
    total = sum(item['price'] * item['qty'] for item in order)
    print(f"Order placed! Total: ${total}")
    print("Sending confirmation email...")
"""


def calculate_order_total(order: list) -> float:
    """
    Calculate the total of the given order.
    """
    return sum(item["price"] * item["qty"] for item in order)


def order_summary(total: float) -> None:
    """
    Print a summary of the order, including the total.
    """
    print(f"Order placed! Total: ${total}")


def send_confirmation_email() -> None:
    """
    Send a confirmation email to the customer after the order is placed.
    """
    print("Sending confirmation email...")


order = [{"price": 100, "qty": 2}, {"price": 50, "qty": 1}]
total = calculate_order_total(order)
order_summary(total)
send_confirmation_email()
