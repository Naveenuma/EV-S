import joblib
import pandas as pd

# Load trained model
model = joblib.load("ridge_ev_range_model.pkl")

print("\n===================================")
print("       EV RANGE PREDICTION")
print("===================================\n")

# Get user inputs
soc = float(input("SOC Percentage (%): "))
battery = float(input("Battery Capacity (kWh): "))
max_range = float(input("Max Range (km): "))
top_speed = float(input("Top Speed (km/h): "))
acceleration = float(input("Acceleration 0 - 100 km/h (seconds): "))
motor_power = float(input("Motor Power (kW): "))
motor_torque = float(input("Motor Torque (Nm): "))
weight = float(input("EV Weight (kg): "))
passengers = int(input("Passenger Count: "))
energy = float(input("Energy Consumption (kWh/100km): "))
highway_city = input("Highway/City: ")

# Create input DataFrame
input_data = pd.DataFrame([{
    "SOC_Percentage": soc,
    "Battery_Capacity_kWh": battery,
    "Max_Range_km": max_range,
    "Top Speed": top_speed,
    "Acceleration 0 - 100 km/h": acceleration,
    "Motor_Power_kW": motor_power,
    "Motor_Torque_Nm": motor_torque,
    "EV_Weight_kg": weight,
    "Passenger_Count": passengers,
    "Energy_Consumption_kWh_per_100km": energy,
    "Highway_City": highway_city
}])

# Make prediction
prediction = model.predict(input_data)

print("\n===================================")
print(f"Predicted EV Range: {prediction[0]:.2f} km")
print("===================================\n")
