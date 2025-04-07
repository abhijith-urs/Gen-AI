# Gen-AI
Applied GenAI course final project repo.

# BACKEND:
# 🚘 VoltAI Vehicle Simulator API

A mock real-time vehicle telemetry API built using FastAPI. This project simulates data from internal combustion (IC) vehicles and serves it via RESTful endpoints.

## ✨ Features

- Randomized but realistic vehicle data
- Simulates:
  - Engine temperature
  - Fuel and oil levels
  - Tire pressure (all 4 tires)
  - Engine load
  - Check engine light
- Simulated odometer that increases with each API call
- JSON responses suitable for AI/ML or analytics pipelines

---

## 🚀 Getting Started

1. Clone the Repo
```bash
git clone https://github.com/your-username/vehicle-simulator.git
cd vehicle-simulator

2. Install Dependencies
pip install -r requirements.txt

3. Run API Server
uvicorn simulate_vehicle_api:app --reload

4. Access the Endpoints
	•	Root: http://127.0.0.1:8000/
	•	All vehicles: http://127.0.0.1:8000/vehicles
	•	Single vehicle: http://127.0.0.1:8000/vehicle/VH200001