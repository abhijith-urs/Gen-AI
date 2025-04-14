def evaluate_vehicle_status(data):
    results = []
    if data["temperature"] > 100:
        results.append("⚠️ High engine temperature!")
    if data["oil_level"] < 50:
        results.append("⚠️ Oil level low.")
    if data["fuel_level"] < 25:
        results.append("⚠️ Low fuel.")
    for tire in ['FL', 'FR', 'RL', 'RR']:
        if data[f"tire_pressure_{tire}"] < 30:
            results.append(f"⚠️ Low pressure in {tire} tire.")
    if data["engine_light_on"]:
        results.append("⚠️ Check engine light is ON.")
    return results or ["✅ All systems are good."]
