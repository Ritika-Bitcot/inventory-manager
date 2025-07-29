"""
SRP Violation:

def place_order(order):
    total = sum(item['price'] * item['qty'] for item in order)
    print(f"Order placed! Total: ${total}")
    print("Sending confirmation email...")
"""
def calculate_order_total(order):
    return sum(item['price'] * item['qty'] for item in order)

def order_summary(total):
    print(f"Order placed! Total: ${total}")

def send_confirmation_email():
    print("Sending confirmation email...")

order = [{'price': 100, 'qty': 2}, {'price': 50, 'qty': 1}]
total = calculate_order_total(order)
order_summary(total)
send_confirmation_email()
