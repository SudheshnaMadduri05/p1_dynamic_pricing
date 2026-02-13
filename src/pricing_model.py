from pathlib import Path
import joblib
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "price_model.pkl"

model = joblib.load(MODEL_PATH)

def predict_price(base_price, demand, inventory, user_type, time_of_day):
    features = np.array([[base_price, demand, inventory, user_type, time_of_day]])
    return round(model.predict(features)[0], 2)
    

