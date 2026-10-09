import httpx
import json

base_url = 'http://localhost:8000/api'
session = httpx.Client()

print("1. Testing Signup...")
res = session.post(f"{base_url}/auth/signup", json={"name": "Alice", "email": "alice@agri.com", "password": "password123"})
print(res.status_code, res.text)

print("\n2. Testing Login...")
res = session.post(f"{base_url}/auth/login", data={"username": "alice@agri.com", "password": "password123"})
print(res.status_code)
if res.status_code == 200:
    token = res.json().get("access_token")
    session.headers.update({"Authorization": f"Bearer {token}"})

    print("\n3. Testing Create Farm...")
    res = session.post(f"{base_url}/farms/", json={"name": "North Farm", "location": "Ohio", "area": 500.0, "description": "Wheat farm"})
    print(res.status_code, res.text)
    farm_id = res.json().get("id") if res.status_code == 200 else "dummy_farm"

    print("\n4. Testing Create Field...")
    res = session.post(f"{base_url}/fields/", json={"farm_id": farm_id, "name": "Field A", "crop": "Wheat", "area": 100.0, "soil_type": "Loam", "planting_date": "2024-04-01"})
    print(res.status_code, res.text)
    field_id = res.json().get("id") if res.status_code == 200 else "dummy_field"

    print("\n5. Testing Fetch Weather...")
    res = session.get(f"{base_url}/weather/")
    print(res.status_code, res.text)

    print("\n6. Testing Run Prediction...")
    payload = {
        "farm_id": farm_id,
        "field_id": field_id,
        "crop": "Wheat",
        "cultivated_area": 100.0,
        "soil_type": "Loam",
        "soil_ph": 6.5,
        "soil_moisture": 30.5,
        "soil_nutrients": 45.0,
        "temperature": 25.0,
        "rainfall": 120.0,
        "humidity": 60.0
    }
    res = session.post(f"{base_url}/predictions/", json=payload)
    print(res.status_code, res.text)
