from fastapi import FastAPI
from fastapi.responses import JSONResponse
import random
from datetime import datetime, timedelta

app = FastAPI()

vehicle_ids = ["VH01", "VH02", "VH03"]

# Static Base Information for Vehicles
vehicle_info = {
    "VH01": {
        "make_year": 2017,
        "total_odometer": 65000,
        "last_service_miles": 64000,
        "last_service_date": datetime.now() - timedelta(days=90),
        "last_oil_change_date": datetime.now() - timedelta(days=100),
        "last_tire_rotation_date": datetime.now() - timedelta(days=180),
        "last_brake_inspection_date": datetime.now() - timedelta(days=200),
    },
    "VH02": {
        "make_year": 2019,
        "total_odometer": 68800,
        "last_service_miles": 67500,
        "last_service_date": datetime.now() - timedelta(days=45),
        "last_oil_change_date": datetime.now() - timedelta(days=60),
        "last_tire_rotation_date": datetime.now() - timedelta(days=120),
        "last_brake_inspection_date": datetime.now() - timedelta(days=160),
    },
    "VH03": {
        "make_year": 2021,
        "total_odometer": 70300,
        "last_service_miles": 69500,
        "last_service_date": datetime.now() - timedelta(days=30),
        "last_oil_change_date": datetime.now() - timedelta(days=40),
        "last_tire_rotation_date": datetime.now() - timedelta(days=90),
        "last_brake_inspection_date": datetime.now() - timedelta(days=100),
    },
}


def generate_vehicle_data(vehicle_id):
    info = vehicle_info[vehicle_id]

    # Simulate today's driven miles
    today_driven = random.randint(5, 50)
    info["total_odometer"] += today_driven

    # Constants
    oil_change_interval = 5000
    tire_rotation_interval = 8000
    brake_inspection_interval = 12000

    return {
        "vehicle_id":
        vehicle_id,
        "make_year":
        info["make_year"],
        "tracking_timestamp":
        datetime.now().isoformat(),
        "engine_temperature_C":
        random.randint(70, 110),
        "engine_load_percent":
        random.randint(20, 100),
        "fuel_level_percent":
        random.randint(10, 100),
        "battery_level_percent":
        random.randint(70, 100),
        "current_mpg":
        round(random.uniform(15.0, 30.0), 2),
        "average_mpg":
        round(random.uniform(20.0, 27.0), 2),
        "estimate_range_km":
        round((random.randint(10, 100) / 100) * 450, 1),
        "odometer_km":
        info["total_odometer"],
        "today_total_driven_miles":
        today_driven,
        "oil_level_percent":
        random.randint(20, 100),
        "oil_change_due_on": (info["last_oil_change_date"] +
                              timedelta(days=180)).date().isoformat(),
        "oil_change_due_miles":
        info["last_service_miles"] + oil_change_interval,
        "last_oil_change_date":
        info["last_oil_change_date"].date().isoformat(),
        "tire_rotation_due_on": (info["last_tire_rotation_date"] +
                                 timedelta(days=240)).date().isoformat(),
        "tire_rotation_due_miles":
        info["last_service_miles"] + tire_rotation_interval,
        "last_tire_rotation_date":
        info["last_tire_rotation_date"].date().isoformat(),
        "brake_inspection_due_on": (info["last_brake_inspection_date"] +
                                    timedelta(days=365)).date().isoformat(),
        "brake_inspection_due_miles":
        info["last_service_miles"] + brake_inspection_interval,
        "last_brake_inspection_date":
        info["last_brake_inspection_date"].date().isoformat(),
        "last_maintenance_service_date":
        info["last_service_date"].date().isoformat(),
        "last_maintenance_service_miles":
        info["last_service_miles"],
        "miles_after_last_service":
        info["total_odometer"] - info["last_service_miles"],
        "last_maintenance_done_at":
        f"{info['last_service_miles']} miles",
        "tire_pressure_FL":
        round(random.uniform(28, 35), 1),
        "tire_pressure_FR":
        round(random.uniform(28, 35), 1),
        "tire_pressure_RL":
        round(random.uniform(28, 35), 1),
        "tire_pressure_RR":
        round(random.uniform(28, 35), 1),
        "check_engine_light_on":
        random.random() < 0.1,
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
        return JSONResponse(content={"error": "Vehicle ID not found"},
                            status_code=404)
    return JSONResponse(content=generate_vehicle_data(vehicle_id))
