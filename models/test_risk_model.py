# test_risk_model.py
import joblib
import pandas as pd

# Load model
model = joblib.load("models/risk_classifier.joblib")

# Example input
test_data = pd.DataFrame([{
    "weather_code": 1,         # rainy
    "task_type_code": 2,       # welding
    "experience_level": 2,     # 2 years
    "hazard_proximity": 1.4    # meters
}])

# Predict risk
prediction = model.predict(test_data)[0]
print("Predicted Risk Level:", "High" if prediction == 1 else "Low")
