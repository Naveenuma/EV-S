from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
import joblib

app = Flask(__name__, static_folder='.')

# 1. Load the Model and Dataset
model = joblib.load("ridge_ev_range_model.pkl")
df = pd.read_csv("EV-MODEL-DATASET20.csv")

# 2. Serve HTML Pages
@app.route('/')
def home():
    return send_from_directory('.', 'Homepage.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

# 3. API Endpoints for your Dashboards
@app.route('/api/login', methods=['POST'])
def driver_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    # Verify driver against the dataset (Assuming you have a 'Driver_ID' column)
    driver = df[df['Driver_ID'] == username]
    
    # Note: If you have a password column in your CSV, you can add: and driver.iloc[0]['Password'] == password
    if not driver.empty: 
        return jsonify({
            "success": True, 
            "driver_id": username, 
            "car_regno": str(driver.iloc[0].get('Car_RegNo', 'Unknown'))
        })
    return jsonify({"success": False})

@app.route('/api/admin-login', methods=['POST'])
def admin_login():
    data = request.json
    # Hardcoded admin credentials for safety
    if data.get('username') == 'admin' and data.get('password') == 'admin123': 
        return jsonify({"success": True})
    return jsonify({"success": False})

@app.route('/api/vehicles', methods=['GET'])
def get_vehicles():
    # Feeds the Admin Dashboard table
    return jsonify(df.to_dict(orient='records'))

@app.route('/api/admin', methods=['GET'])
def get_admin_stats():
    total_cars = len(df)
    running = len(df[df['Running_Status'].str.lower() == 'running']) if 'Running_Status' in df.columns else 0
    charging = len(df[df['Charging_Status'].str.lower() == 'charging']) if 'Charging_Status' in df.columns else 0
    return jsonify({"totalCars": total_cars, "runningCars": running, "chargingCars": charging, "totalRevenue": 845200})

@app.route('/api/driverdetails/<driver_id>', methods=['GET'])
def get_driver_details(driver_id):
    # Feeds the Driver Dashboard
    driver = df[df['Driver_ID'] == driver_id]
    if not driver.empty:
        return jsonify(driver.iloc[0].to_dict())
    return jsonify({"error": "Driver not found"})

@app.route('/api/predict-range', methods=['POST'])
def predict_range():
    # Connects the model to the Driver Dashboard prediction button
    data = request.json
    input_data = pd.DataFrame([data])
    prediction = model.predict(input_data)
    return jsonify({"predictedRangeKm": round(prediction[0], 2)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)