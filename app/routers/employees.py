from datetime import date
from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from bson import ObjectId
from app.database import db
from app.models import (
    EmployeeCreate, 
    EmployeeOut, 
    SalaryUpdate,
    EmployeeWithHistory
)

router = APIRouter(prefix="/employees", tags=["employees"])


async def get_employee_full_data(employee_data: dict) -> dict:
    """Получить полные данные сотрудника (с названиями отдела и должности)"""
    # Получаем данные отдела
    department = await db.departments.find_one({"code": employee_data.get("department_code")})
    if department:
        employee_data["department_name"] = department.get("name")
    
    # Получаем данные должности
    position = await db.positions.find_one({"name": employee_data.get("position_name")})
    if position:
        employee_data["position_grade"] = position.get("grade")
    
    return employee_data


@router.get("/", response_model=list[EmployeeOut])
async def get_employees(
    department: Optional[str] = Query(None),
    position: Optional[str] = Query(None)
):
    """Получить всех сотрудников с фильтрацией"""
    query = {}
    if department:
        query["department_code"] = department
    if position:
        query["position_name"] = position
    
    employees = []
    async for emp in db.employees.find(query):
        emp["id"] = str(emp["_id"])
        del emp["_id"]
        
        # Получаем полные данные
        emp = await get_employee_full_data(emp)
        employees.append(emp)
    
    return employees


@router.post("/", response_model=EmployeeOut)
async def create_employee(employee: EmployeeCreate):
    """Создать нового сотрудника"""
    # Проверяем отдел
    department = await db.departments.find_one({"code": employee.department_code})
    if not department:
        raise HTTPException(400, f"Отдел с кодом '{employee.department_code}' не найден")
    
    # Проверяем должность
    position = await db.positions.find_one({"name": employee.position_name})
    if not position:
        raise HTTPException(400, f"Должность '{employee.position_name}' не найдена")
    
    # Создаем сотрудника
    employee_data = employee.dict()
    
    # Добавляем начальную запись в историю зарплат
    employee_data["salary_history"] = [{
        "date": employee.hire_date.isoformat(),
        "salary": employee.salary,
        "reason": "Начальная зарплата"
    }]
    
    # Конвертируем даты в строки для MongoDB
    employee_data["hire_date"] = employee.hire_date.isoformat()
    
    result = await db.employees.insert_one(employee_data)
    employee_data["id"] = str(result.inserted_id)
    
    # Добавляем названия отдела и должности
    employee_data = await get_employee_full_data(employee_data)
    
    return employee_data


@router.get("/{employee_id}", response_model=EmployeeWithHistory)
async def get_employee(employee_id: str):
    """Получить сотрудника по ID с историей зарплат"""
    if not ObjectId.is_valid(employee_id):
        raise HTTPException(400, "Неверный ID")
    
    employee = await db.employees.find_one({"_id": ObjectId(employee_id)})
    if not employee:
        raise HTTPException(404, "Сотрудник не найден")
    
    employee["id"] = str(employee["_id"])
    del employee["_id"]
    
    # Конвертируем строки дат обратно в объекты date
    if isinstance(employee.get("hire_date"), str):
        employee["hire_date"] = date.fromisoformat(employee["hire_date"])
    
    # Конвертируем историю зарплат
    history = employee.get("salary_history", [])
    for item in history:
        if isinstance(item.get("date"), str):
            item["date"] = date.fromisoformat(item["date"])
    
    # Добавляем названия отдела и должности
    employee = await get_employee_full_data(employee)
    
    return employee


@router.put("/{employee_id}/salary", response_model=EmployeeWithHistory)
async def update_salary(employee_id: str, salary_update: SalaryUpdate):
    """Изменить зарплату сотрудника"""
    if not ObjectId.is_valid(employee_id):
        raise HTTPException(400, "Неверный ID")
    
    # Получаем текущего сотрудника
    employee = await db.employees.find_one({"_id": ObjectId(employee_id)})
    if not employee:
        raise HTTPException(404, "Сотрудник не найден")
    
    # Обновляем текущую зарплату
    await db.employees.update_one(
        {"_id": ObjectId(employee_id)},
        {"$set": {"salary": salary_update.new_salary}}
    )
    
    # Добавляем запись в историю
    history_item = {
        "date": salary_update.change_date.isoformat(),
        "salary": salary_update.new_salary,
        "reason": salary_update.reason
    }
    
    await db.employees.update_one(
        {"_id": ObjectId(employee_id)},
        {"$push": {"salary_history": history_item}}
    )
    
    # Возвращаем обновленные данные
    return await get_employee(employee_id)


@router.delete("/{employee_id}")
async def delete_employee(employee_id: str):
    """Удалить сотрудника"""
    if not ObjectId.is_valid(employee_id):
        raise HTTPException(400, "Неверный ID")
    
    result = await db.employees.delete_one({"_id": ObjectId(employee_id)})
    if result.deleted_count == 0:
        raise HTTPException(404, "Сотрудник не найден")
    
    return {"message": "Сотрудник удален"}