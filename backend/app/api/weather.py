from fastapi import APIRouter, Depends, HTTPException
import httpx
from app.api.auth import get_current_user

router = APIRouter()

@router.get("/")
async def get_weather(latitude: float, longitude: float, current_user: dict = Depends(get_current_user)):
    # Using Open-Meteo for free weather data
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,relative_humidity_2m,precipitation&timezone=auto"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=5.0)
            response.raise_for_status()
            data = response.json()
            
            current = data.get("current", {})
            return {
                "temperature": current.get("temperature_2m", 25.0),
                "humidity": current.get("relative_humidity_2m", 60.0),
                "precipitation": current.get("precipitation", 0.0)
            }
        except Exception as e:
            raise HTTPException(status_code=503, detail="Weather data unavailable. You can continue with manually provided values if supported by the model.")
