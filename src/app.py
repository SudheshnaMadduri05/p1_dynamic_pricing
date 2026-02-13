import streamlit as st
import random
from datetime import datetime
from src.pricing_model import predict_price
from src.price_lock import lock_price, get_locked_price
from src.database import products


st.title("Dynamic Pricing System")

user_id = "user123"
cart = {}

st.header("Available Products")

for pid, product in products.items():
    qty = st.number_input(
        f"{product['name']} (Base Price: {product['base_price']})",
        min_value=0,
        step=1,
        key=pid
    )
    if qty > 0:
        cart[pid] = qty

if st.button("Checkout"):

    grand_total = 0.0

    st.subheader("Checkout Details")

    for pid, qty in cart.items():
        product = products[pid]

        dynamic_price = predict_price(
            base_price=product["base_price"],
            demand=round(random.uniform(1.0, 1.5), 2),
            inventory=product["inventory"],
            user_type=random.choice([0, 1]),
            time_of_day=datetime.now().hour
        )

        lock_price(user_id, pid, dynamic_price)
        locked_price = get_locked_price(user_id, pid)

        total_price = locked_price * qty
        grand_total += total_price

        st.write(f"{product['name']} | Qty: {qty} | Unit: {locked_price:.2f} | Total: {total_price:.2f}")

    st.success(f"Total Payable Amount: ₹ {grand_total:.2f}")
