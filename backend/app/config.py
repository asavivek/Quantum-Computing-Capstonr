import os

class Settings:
    PROJECT_NAME: str = "QuantumYield AI"
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "quantumyield")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "supersecretkey_for_development_only")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 days
    WEATHER_API_KEY: str = os.getenv("WEATHER_API_KEY", "dummy_weather_api_key")

settings = Settings()
