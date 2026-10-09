from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas import FieldCreate, FieldResponse
from app.database import fields_collection, farms_collection
from app.api.auth import get_current_user
import uuid
from datetime import datetime

router = APIRouter()

@router.get("/", response_model=List[FieldResponse])
def get_fields(current_user: dict = Depends(get_current_user)):
    fields = list(fields_collection.find({"owner_id": current_user["id"]}))
    return fields

@router.post("/", response_model=FieldResponse)
def create_field(field: FieldCreate, current_user: dict = Depends(get_current_user)):
    farm = farms_collection.find_one({"id": field.farm_id, "owner_id": current_user["id"]})
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found or not owned by user")
        
    field_dict = field.dict()
    field_dict["id"] = str(uuid.uuid4())
    field_dict["owner_id"] = current_user["id"]
    field_dict["created_at"] = datetime.utcnow().isoformat()
    
    fields_collection.insert_one(field_dict.copy())
    return field_dict

@router.delete("/{field_id}")
def delete_field(field_id: str, current_user: dict = Depends(get_current_user)):
    result = fields_collection.delete_one({"id": field_id, "owner_id": current_user["id"]})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Field not found")
    return {"status": "ok"}
