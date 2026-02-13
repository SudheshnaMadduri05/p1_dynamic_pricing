from datetime import datetime, timedelta

price_locks = {}

def lock_price(user_id, product_id, price):
    price_locks[(user_id, product_id)] = {
        "price": price,
        "expires": datetime.now() + timedelta(minutes=30)
    }

def get_locked_price(user_id, product_id):
    lock = price_locks.get((user_id, product_id))
    if lock and lock["expires"] > datetime.now():
        return lock["price"]
    return None
def clean_expired_locks():
    now = datetime.now()
    expired_keys = [
        key for key, value in price_locks.items()
        if value["expires"] <= now
    ]
    for key in expired_keys:
        del price_locks[key]
