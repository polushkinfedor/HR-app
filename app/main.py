# app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os

from app.routers import departments, positions, employees

app = FastAPI(
    title="HR System",
    description="Простая система управления персоналом",
    version="1.0.0"
)

# Подключаем роутеры
app.include_router(departments.router)
app.include_router(positions.router)
app.include_router(employees.router)

# Монтируем статические файлы
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def root():
    """Главная страница"""
    # Если есть статический файл index.html - читаем его
    index_path = "static/index.html"
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    
    # Иначе показываем простую страницу
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html>
    <head>
        <title>HR System</title>
    </head>
    <body>
        <h1>HR System</h1>
        <p>Файл index.html не найден/</p>
        <p><a href="/docs">API документация</a></p>
    </body>
    </html>
    """)


@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "message": "HR System работает"
    }