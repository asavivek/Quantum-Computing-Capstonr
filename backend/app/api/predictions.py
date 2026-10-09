from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas import PredictionCreate, PredictionResponse
from app.database import predictions_collection, farms_collection, fields_collection
from app.api.auth import get_current_user
from app.services.quantum_service import run_prediction
import uuid
from datetime import datetime

router = APIRouter()

@router.get("/", response_model=List[PredictionResponse])
def get_predictions(current_user: dict = Depends(get_current_user)):
    predictions = list(predictions_collection.find({"owner_id": current_user["id"]}).sort("created_at", -1))
    return predictions

@router.post("/", response_model=PredictionResponse)
def create_prediction(prediction: PredictionCreate, current_user: dict = Depends(get_current_user)):
    # Validation skipped for demo to allow manual farm_id entries
    # farm = farms_collection.find_one({"id": prediction.farm_id, "owner_id": current_user["id"]})
    # if not farm:
    #     raise HTTPException(status_code=404, detail="Farm not found")
        
    # field = fields_collection.find_one({"id": prediction.field_id, "farm_id": prediction.farm_id})
    # if not field:
    #     raise HTTPException(status_code=404, detail="Field not found")

    input_data = {
        "temperature": prediction.temperature,
        "rainfall": prediction.rainfall,
        "humidity": prediction.humidity,
        "soil_ph": prediction.soil_ph,
        "soil_moisture": prediction.soil_moisture,
        "soil_nutrients": prediction.soil_nutrients,
        "soil_type": prediction.soil_type,
        "crop": prediction.crop
    }
    
    try:
        prediction_result = run_prediction(input_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    pred_dict = {
        "id": str(uuid.uuid4()),
        "owner_id": current_user["id"],
        "farm_id": prediction.farm_id,
        "field_id": prediction.field_id,
        "input_features": input_data,
        "model_results": prediction_result["results"],
        "selected_model": prediction_result["selected_model"],
        "predicted_yield": prediction_result["predicted_yield"],
        "metrics": prediction_result["metrics"],
        "quantum_metadata": prediction_result["quantum_metadata"],
        "created_at": datetime.utcnow().isoformat()
    }
    
    predictions_collection.insert_one(pred_dict.copy())
    return pred_dict

@router.delete("/{prediction_id}")
def delete_prediction(prediction_id: str, current_user: dict = Depends(get_current_user)):
    result = predictions_collection.delete_one({"id": prediction_id, "owner_id": current_user["id"]})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return {"status": "ok"}
