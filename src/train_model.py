import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

df = pd.read_csv("data/pricing_data.csv")

X = df.drop("final_price", axis=1)
y = df["final_price"]

model = LinearRegression()
model.fit(X, y)

joblib.dump(model, "models/price_model.pkl")
print("Model trained and saved.")
