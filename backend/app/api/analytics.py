from fastapi import APIRouter, Depends
from app.database import predictions_collection
from app.api.auth import get_current_user

router = APIRouter()

@router.get("/overview")
def get_analytics_overview(current_user: dict = Depends(get_current_user)):
    predictions = list(predictions_collection.find({"owner_id": current_user["id"]}))
    
    if not predictions:
        return {"status": "no_data"}
        
    # Group by crop
    crop_yields = {}
    for p in predictions:
        crop = p["input_features"]["crop"]
        if crop not in crop_yields:
            crop_yields[crop] = []
        crop_yields[crop].append(p["predicted_yield"])
        
    avg_yield_by_crop = {k: sum(v)/len(v) for k, v in crop_yields.items()}
    
    return {
        "status": "ok",
        "total_predictions": len(predictions),
        "average_yield_by_crop": avg_yield_by_crop
    }
