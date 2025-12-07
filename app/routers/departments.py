from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.database import db
from app.models import Department, DepartmentInDB

router = APIRouter(prefix="/departments", tags=["departments"])


@router.get("/", response_model=list[DepartmentInDB])
async def get_departments():
    """Получить все отделы"""
    departments = []
    async for dept in db.departments.find():
        dept["id"] = str(dept["_id"])
        del dept["_id"]
        departments.append(dept)
    return departments


@router.post("/", response_model=DepartmentInDB)
async def create_department(department: Department):
    """Создать новый отдел"""
    # Проверяем, нет ли отдела с таким кодом
    existing = await db.departments.find_one({"code": department.code})
    if existing:
        raise HTTPException(400, f"Отдел с кодом '{department.code}' уже существует")
    
    result = await db.departments.insert_one(department.dict())
    department_data = department.dict()
    department_data["id"] = str(result.inserted_id)
    return department_data


@router.delete("/{department_id}")
async def delete_department(department_id: str):
    """Удалить отдел"""
    # Проверяем, есть ли сотрудники в отделе
    employee_count = await db.employees.count_documents({"department_code": department_id})
    if employee_count > 0:
        raise HTTPException(400, "Нельзя удалить отдел с сотрудниками")
    
    result = await db.departments.delete_one({"_id": ObjectId(department_id)})
    if result.deleted_count == 0:
        raise HTTPException(404, "Отдел не найден")
    
    return {"message": "Отдел удален"}