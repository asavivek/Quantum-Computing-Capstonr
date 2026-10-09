from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas import FarmCreate, FarmResponse
from app.database import farms_collection
from app.api.auth import get_current_user
import uuid
from datetime import datetime

router = APIRouter()

@router.get("/", response_model=List[FarmResponse])
def get_farms(current_user: dict = Depends(get_current_user)):
    farms = list(farms_collection.find({"owner_id": current_user["id"]}))
    return farms

@router.post("/", response_model=FarmResponse)
def create_farm(farm: FarmCreate, current_user: dict = Depends(get_current_user)):
    farm_dict = farm.dict()
    farm_dict["id"] = str(uuid.uuid4())
    farm_dict["owner_id"] = current_user["id"]
    farm_dict["created_at"] = datetime.utcnow().isoformat()
    
    farms_collection.insert_one(farm_dict.copy())
    return farm_dict

@router.get("/{farm_id}", response_model=FarmResponse)
def get_farm(farm_id: str, current_user: dict = Depends(get_current_user)):
    farm = farms_collection.find_one({"id": farm_id, "owner_id": current_user["id"]})
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")
    return farm

@router.put("/{farm_id}", response_model=FarmResponse)
def update_farm(farm_id: str, farm: FarmCreate, current_user: dict = Depends(get_current_user)):
    result = farms_collection.update_one(
        {"id": farm_id, "owner_id": current_user["id"]},
        {"$set": farm.dict()}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Farm not found")
    return farms_collection.find_one({"id": farm_id})

@router.delete("/{farm_id}")
def delete_farm(farm_id: str, current_user: dict = Depends(get_current_user)):
    result = farms_collection.delete_one({"id": farm_id, "owner_id": current_user["id"]})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Farm not found")
    return {"status": "ok"}
