from datetime import date
from typing import Optional, List
from pydantic import BaseModel


# Модель для отдела
class Department(BaseModel):
    name: str
    code: str  # Уникальный код, например "IT", "HR"
    description: Optional[str] = None

class DepartmentInDB(Department):
    id: str


# Модель для должности
class Position(BaseModel):
    name: str
    grade: Optional[str] = None
    description: Optional[str] = None

class PositionInDB(Position):
    id: str


# Модель для сотрудника
class EmployeeCreate(BaseModel):
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    
    department_code: str  # Код отдела
    position_name: str    # Название должности
    
    hire_date: date
    salary: int
    
    email: Optional[str] = None
    phone: Optional[str] = None


class EmployeeOut(EmployeeCreate):
    id: str
    department_name: Optional[str] = None
    position_grade: Optional[str] = None


# Модель для изменения зарплаты
class SalaryUpdate(BaseModel):
    new_salary: int
    change_date: date
    reason: Optional[str] = None


# Модель для истории зарплаты
class SalaryHistoryItem(BaseModel):
    date: date
    salary: int
    reason: Optional[str] = None


# Модель для ответа с историей
class EmployeeWithHistory(EmployeeOut):
    salary_history: List[SalaryHistoryItem] = []
