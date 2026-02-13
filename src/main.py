import random
from datetime import datetime
from src.pricing_model import predict_price
from src.price_lock import lock_price, get_locked_price
from src.database import products


def main():
    user_id = "user123"
    cart = {}

    print("\n========== AVAILABLE PRODUCTS ==========\n")

    for pid, product in products.items():
        print(f"{pid}. {product['name']} (Base Price: {product['base_price']})")

    print("\nEnter quantity for each product (0 to skip):\n")

    # 🛒 Take user input
    for pid, product in products.items():
        qty = int(input(f"Quantity for {product['name']}: "))
        if qty > 0:
            cart[pid] = qty

    # 🧮 Dynamic pricing + Lock price
    for pid in cart:
        product = products[pid]

        dynamic_price = predict_price(
            base_price=product["base_price"],
            demand=round(random.uniform(1.0, 1.5), 2),
            inventory=product["inventory"],
            user_type=random.choice([0, 1]),
            time_of_day=datetime.now().hour
        )

        lock_price(user_id, pid, dynamic_price)

    # 🧾 Checkout
    print("\n========== CHECKOUT ==========\n")
    print("ID   Product Name        Qty     Unit Price     Total")
    print("---------------------------------------------------------")

    grand_total = 0.0

    for pid, qty in cart.items():
        locked_price = get_locked_price(user_id, pid)

        if locked_price is None:
            print(f"{pid:<4} {products[pid]['name']:<18} EXPIRED")
            continue

        total_price = locked_price * qty
        grand_total += total_price

        print(f"{pid:<4} {products[pid]['name']:<18} {qty:<7} {locked_price:>10.2f} {total_price:>12.2f}")

    print("---------------------------------------------------------")
    print(f"TOTAL PAYABLE AMOUNT: {grand_total:>20.2f}")
    print("=========================================================")


if __name__ == "__main__":
    main()
