from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    created_at: str

class Token(BaseModel):
    access_token: str
    token_type: str

class FarmCreate(BaseModel):
    name: str
    location: str
    area: float
    description: Optional[str] = ""

class FarmResponse(FarmCreate):
    id: str
    owner_id: str
    created_at: str

class FieldCreate(BaseModel):
    farm_id: str
    name: str
    crop: str
    area: float
    soil_type: str
    planting_date: str
    notes: Optional[str] = ""

class FieldResponse(FieldCreate):
    id: str
    owner_id: str
    created_at: str

class PredictionCreate(BaseModel):
    farm_id: str
    field_id: str
    crop: str
    cultivated_area: float
    
    # Soil
    soil_type: str
    soil_ph: float
    soil_moisture: float
    soil_nutrients: float
    
    # Weather
    temperature: float
    rainfall: float
    humidity: float

class PredictionResponse(BaseModel):
    id: str
    owner_id: str
    farm_id: str
    field_id: str
    input_features: Dict[str, Any]
    model_results: List[Dict[str, Any]]
    selected_model: str
    predicted_yield: float
    metrics: Dict[str, float]
    quantum_metadata: Optional[Dict[str, Any]] = None
    created_at: str
