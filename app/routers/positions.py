from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.database import db
from app.models import Position, PositionInDB

router = APIRouter(prefix="/positions", tags=["positions"])


@router.get("/", response_model=list[PositionInDB])
async def get_positions():
    """Получить все должности"""
    positions = []
    async for pos in db.positions.find():
        pos["id"] = str(pos["_id"])
        del pos["_id"]
        positions.append(pos)
    return positions


@router.post("/", response_model=PositionInDB)
async def create_position(position: Position):
    """Создать новую должность"""
    result = await db.positions.insert_one(position.dict())
    position_data = position.dict()
    position_data["id"] = str(result.inserted_id)
    return position_data


@router.delete("/{position_id}")
async def delete_position(position_id: str):
    """Удалить должность"""
    # Проверяем, есть ли сотрудники на этой должности
    employee_count = await db.employees.count_documents({"position_id": position_id})
    if employee_count > 0:
        raise HTTPException(400, "Нельзя удалить должность с сотрудниками")
    
    result = await db.positions.delete_one({"_id": ObjectId(position_id)})
    if result.deleted_count == 0:
        raise HTTPException(404, "Должность не найдена")
    
    return {"message": "Должность удалена"}