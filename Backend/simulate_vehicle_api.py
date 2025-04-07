from fastapi import FastAPI
from fastapi.responses import JSONResponse
import random
from datetime import datetime

app = FastAPI()

vehicle_ids = ["VH200001", "VH200002", "VH200003"]
base_odometer = {
    "VH200001": 65000,
    "VH200002": 68800,
    "VH200003": 70300
}

def generate_vehicle_data(vehicle_id):
    base_odometer[vehicle_id] += random.randint(1, 5)

    return {
        "vehicle_id": vehicle_id,
        "tracking_timestamp": datetime.now().isoformat(),
        "temp_engine_C": random.randint(70, 110),
        "fuel_level_percent": random.randint(10, 100),
        "oil_level_percent": random.randint(20, 100),
        "odometer_km": base_odometer[vehicle_id],
        "avg_speed_kmph": random.randint(30, 120),
        "tire_pressure_FL": round(random.uniform(28, 35), 1),
        "tire_pressure_FR": round(random.uniform(28, 35), 1),
        "tire_pressure_RL": round(random.uniform(28, 35), 1),
        "tire_pressure_RR": round(random.uniform(28, 35), 1),
        "engine_load_percent": random.randint(20, 100),
        "check_engine_light_on": random.random() < 0.1
    }

@app.get("/")
def root():
    return {
        "message": "✅ VoltAI Vehicle Simulator API is running!",
        "endpoints": ["/vehicles", "/vehicle/{vehicle_id}"]
    }

@app.get("/vehicles")
def get_all_vehicles():
    data = [generate_vehicle_data(vid) for vid in vehicle_ids]
    return JSONResponse(content=data)

@app.get("/vehicle/{vehicle_id}")
def get_vehicle(vehicle_id: str):
    if vehicle_id not in vehicle_ids:
        return JSONResponse(content={"error": "Vehicle ID not found"}, status_code=404)
    return JSONResponse(content=generate_vehicle_data(vehicle_id))